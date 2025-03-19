#include "Portal.h"
#include "../utils/Logger.h"
#include "../utils/Math.h"
#include "DynamicObject.h"
#include <cmath>

Portal::Portal(int id, PortalColor color) 
    : GameEntity(id, EntityType::PORTAL), 
      color(color), 
      width(1.0f), 
      height(2.0f), 
      isPlaced(false) {
    
    // Set texture based on color
    if (color == PortalColor::BLUE) {
        setTextureName("blue_portal");
    } else {
        setTextureName("orange_portal");
    }
}

Portal::~Portal() {
    // Body disposal is handled by the physics world
}

void Portal::initialize(b2World* world, float x, float y, float angle) {
    if (!world) {
        LOG_ERROR("Cannot initialize portal, world is null");
        return;
    }
    
    // Define the static body for the portal
    b2BodyDef bodyDef;
    bodyDef.type = b2_staticBody;
    bodyDef.position.Set(x, y);
    bodyDef.angle = angle;
    bodyDef.userData = this;
    body = world->CreateBody(&bodyDef);
    
    // Create a sensor fixture for the portal
    b2PolygonShape portalShape;
    portalShape.SetAsBox(width / 2.0f, height / 2.0f);
    
    b2FixtureDef fixtureDef;
    fixtureDef.shape = &portalShape;
    fixtureDef.isSensor = true;  // Important: portal is a sensor
    
    body->CreateFixture(&fixtureDef);
    isPlaced = true;
    
    LOG_DEBUG("Initialized portal " + std::to_string(id) + " at position (" + 
              std::to_string(x) + ", " + std::to_string(y) + ") with angle " + 
              std::to_string(angle));
}

void Portal::setSize(float newWidth, float newHeight) {
    if (body) {
        LOG_WARNING("Cannot change size of portal after initialization");
        return;
    }
    
    width = newWidth;
    height = newHeight;
}

void Portal::linkTo(std::shared_ptr<Portal> otherPortal) {
    if (otherPortal && otherPortal->getId() != this->getId()) {
        linkedPortal = otherPortal;
        LOG_DEBUG("Portal " + std::to_string(id) + " linked to portal " + 
                  std::to_string(otherPortal->getId()));
    } else {
        LOG_WARNING("Invalid portal linking attempt");
    }
}

std::shared_ptr<Portal> Portal::getLinkedPortal() const {
    return linkedPortal.lock();
}

bool Portal::hasLinkedPortal() const {
    return !linkedPortal.expired();
}

bool Portal::canTeleport() const {
    // Check if this portal is placed and linked to another portal
    return isPlaced && hasLinkedPortal() && getLinkedPortal()->getIsPlaced();
}

void Portal::teleportEntity(GameEntity* entity) {
    if (!canTeleport() || !entity || entity->getType() != EntityType::DYNAMIC) {
        return;
    }
    
    DynamicObject* dynamicObj = static_cast<DynamicObject*>(entity);
    std::shared_ptr<Portal> exitPortal = getLinkedPortal();
    
    if (!dynamicObj->getBody() || !exitPortal->getBody()) {
        return;
    }
    
    // Get entry and exit properties
    b2Vec2 entryPos = getPosition();
    float entryAngle = getAngle();
    b2Vec2 exitPos = exitPortal->getPosition();
    float exitAngle = exitPortal->getAngle();
    
    // Get object properties
    b2Vec2 objPos = dynamicObj->getPosition();
    b2Vec2 objVel = dynamicObj->getVelocity();
    float objAngle = dynamicObj->getAngle();
    
    // Transform position, velocity, and orientation
    b2Vec2 newPos = Math::transformPosition(objPos, entryPos, exitPos, entryAngle, exitAngle);
    b2Vec2 newVel = Math::transformVelocity(objVel, entryAngle, exitAngle);
    float newAngle = Math::transformAngle(objAngle, entryAngle, exitAngle);
    
    // Apply transformations to the object
    dynamicObj->getBody()->SetTransform(newPos, newAngle);
    dynamicObj->setVelocity(newVel);
    
    LOG_DEBUG("Teleported entity " + std::to_string(entity->getId()) + 
              " from portal " + std::to_string(id) + 
              " to portal " + std::to_string(exitPortal->getId()));
}

void Portal::update(float deltaTime) {
    // Portal logic updates (if any)
}

void Portal::render() {
    // Rendering is handled by the Renderer/PortalRenderer
    // This method is left empty as a placeholder
}
