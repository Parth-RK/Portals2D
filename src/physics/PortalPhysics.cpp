#include "PortalPhysics.h"
#include "PhysicsEngine.h"
#include "../entities/Portal.h"
#include "../utils/Logger.h"
#include "../utils/Math.h"
#include <cmath>

// Ray cast callback for portal placement
class PortalRayCastCallback : public b2RayCastCallback {
public:
    b2Vec2 point;
    b2Vec2 normal;
    bool hit = false;
    
    float ReportFixture(b2Fixture* fixture, const b2Vec2& p, const b2Vec2& n, float fraction) override {
        // Ignore sensors (like other portals)
        if (fixture->IsSensor()) {
            return -1.0f; // Continue
        }
        
        hit = true;
        point = p;
        normal = n;
        return fraction; // Return the fraction to get the closest hit
    }
};

PortalPhysics::PortalPhysics(PhysicsEngine* engine) : physicsEngine(engine) {
    LOG_DEBUG("Portal physics initialized");
}

PortalPhysics::~PortalPhysics() {
}

bool PortalPhysics::placePortal(std::shared_ptr<Portal> portal, float x, float y, float angle) {
    if (!portal || !physicsEngine || !physicsEngine->getWorld()) {
        LOG_ERROR("Cannot place portal, invalid arguments");
        return false;
    }
    
    // Check if we can place the portal at this location
    if (!canPlacePortalAt(x, y, angle, portal->getWidth(), portal->getHeight())) {
        LOG_WARNING("Cannot place portal at location: overlap detected");
        return false;
    }
    
    // Initialize the portal
    portal->initialize(physicsEngine->getWorld(), x, y, angle);
    portal->setIsPlaced(true);
    
    LOG_INFO("Placed portal " + std::to_string(portal->getId()) + 
             " at position (" + std::to_string(x) + ", " + std::to_string(y) + 
             ") with angle " + std::to_string(angle));
    
    return true;
}

bool PortalPhysics::canPlacePortalAt(float x, float y, float angle, float width, float height) {
    // Check for overlapping portals or other objects
    return !checkPortalOverlap(x, y, angle, width, height);
}

bool PortalPhysics::checkPortalOverlap(float x, float y, float angle, float width, float height) {
    // Use Box2D's shape querying to check if the proposed portal location overlaps with anything
    if (!physicsEngine || !physicsEngine->getWorld()) {
        return true;  // Assume overlap if we can't check
    }
    
    // Create a shape for the potential portal location
    b2PolygonShape portalShape;
    portalShape.SetAsBox(width / 2.0f, height / 2.0f);
    
    // Setup a transform for the proposed position and angle
    b2Transform transform;
    transform.Set(b2Vec2(x, y), angle);
    
    // Use Box2D AABB query for collision check
    b2AABB aabb;
    const int vertexCount = 4;  // Box shape has 4 vertices
    b2Vec2 vertices[vertexCount];
    portalShape.GetVertices(vertices, vertexCount);
    
    // Initialize AABB with the first vertex
    b2Vec2 v = b2Mul(transform, vertices[0]);
    aabb.lowerBound = aabb.upperBound = v;
    
    // Expand AABB with remaining vertices
    for (int i = 1; i < vertexCount; ++i) {
        b2Vec2 v = b2Mul(transform, vertices[i]);
        aabb.lowerBound = b2Min(aabb.lowerBound, v);
        aabb.upperBound = b2Max(aabb.upperBound, v);
    }
    
    // Query the world for overlaps
    bool foundOverlap = false;
    
    class OverlapCallback : public b2QueryCallback {
    public:
        bool overlap = false;
        b2PolygonShape* shape;
        b2Transform* transform;
        
        bool ReportFixture(b2Fixture* fixture) override {
            // Ignore sensors (other portals)
            if (fixture->IsSensor()) {
                return true;  // Continue the query
            }
            
            // Check for actual overlap
            b2Shape* fixtureShape = fixture->GetShape();
            if (b2TestOverlap(shape, 0, fixtureShape, 0, *transform, fixture->GetBody()->GetTransform())) {
                overlap = true;
                return false;  // Stop the query
            }
            
            return true;  // Continue the query
        }
    };
    
    OverlapCallback callback;
    callback.shape = &portalShape;
    callback.transform = &transform;
    
    physicsEngine->getWorld()->QueryAABB(&callback, aabb);
    
    return callback.overlap;
}

bool PortalPhysics::checkExitBlocked(std::shared_ptr<Portal> portal) {
    if (!portal || !portal->hasLinkedPortal()) {
        return true;  // Consider it blocked if there's no linked portal
    }
    
    std::shared_ptr<Portal> exitPortal = portal->getLinkedPortal();
    if (!exitPortal || !exitPortal->getIsPlaced()) {
        return true;
    }
    
    // Check if there's anything blocking the exit portal
    // Simplified implementation: consider a small area in front of the exit portal
    b2Vec2 portalPos = exitPortal->getPosition();
    float portalAngle = exitPortal->getAngle();
    
    // Direction vector normal to the portal surface
    b2Vec2 normalDir = Math::rotateVector(b2Vec2(0.0f, 1.0f), portalAngle);
    
    // Check a small area in front of the portal
    b2Vec2 checkPos = portalPos + 0.5f * normalDir;
    float checkRadius = exitPortal->getWidth() / 2.0f;
    
    // Use a query to check if anything is blocking the exit
    b2AABB aabb;
    aabb.lowerBound = checkPos - b2Vec2(checkRadius, checkRadius);
    aabb.upperBound = checkPos + b2Vec2(checkRadius, checkRadius);
    
    class BlockedCallback : public b2QueryCallback {
    public:
        bool blocked = false;
        
        bool ReportFixture(b2Fixture* fixture) override {
            // Ignore sensors
            if (fixture->IsSensor()) {
                return true;
            }
            
            // Something is blocking the exit
            blocked = true;
            return false;  // Stop the query
        }
    };
    
    BlockedCallback callback;
    physicsEngine->getWorld()->QueryAABB(&callback, aabb);
    
    return callback.blocked;
}

void PortalPhysics::handlePartialOverlap(GameEntity* entity, Portal* entryPortal) {
    // This is a complex feature that would involve:
    // 1. Determining what percentage of the object is through the portal
    // 2. Rendering part of the object at the entry and part at the exit
    // 3. Deciding when to fully teleport the object
    
    // For simplicity, we'll just log that this would need additional implementation
    LOG_DEBUG("Partial overlap handling needed for entity " + std::to_string(entity->getId()) +
              " with portal " + std::to_string(entryPortal->getId()));
}

b2Vec2 PortalPhysics::castRay(const b2Vec2& start, const b2Vec2& direction, float maxDistance) {
    if (!physicsEngine || !physicsEngine->getWorld()) {
        return start;  // Return starting point if we can't cast
    }
    
    // Normalize direction and scale by max distance
    float length = direction.Length();
    if (length < 0.001f) {
        return start;  // Direction vector too small
    }
    
    b2Vec2 normalizedDir = direction / length;
    b2Vec2 end = start + maxDistance * normalizedDir;
    
    // Perform the ray cast
    PortalRayCastCallback callback;
    physicsEngine->getWorld()->RayCast(&callback, start, end);
    
    if (callback.hit) {
        return callback.point;
    }
    
    // No hit, return the end point of the ray
    return end;
}

float PortalPhysics::findPlacementAngle(const b2Vec2& position, const b2Vec2& normal) {
    // Calculate angle from normal vector
    // The normal points outward from the surface, we want the portal to face that direction
    float angle = atan2(normal.y, normal.x) - M_PI / 2.0f;
    
    // Snap to nearest 45 degrees for simplicity
    const float snapAngle = M_PI / 4.0f;
    return floor(angle / snapAngle + 0.5f) * snapAngle;
}
