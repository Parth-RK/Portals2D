#pragma once

#include <Box2D/Box2D.h>
#include <memory>

class PhysicsEngine;
class Portal;
class GameEntity;

class PortalPhysics {
private:
    PhysicsEngine* physicsEngine;

public:
    PortalPhysics(PhysicsEngine* engine);
    ~PortalPhysics();
    
    // Portal creation and placement
    bool placePortal(std::shared_ptr<Portal> portal, float x, float y, float angle);
    bool canPlacePortalAt(float x, float y, float angle, float width, float height);
    
    // Portal-related physics checks
    bool checkPortalOverlap(float x, float y, float angle, float width, float height);
    bool checkExitBlocked(std::shared_ptr<Portal> portal);
    
    // Handle the physics of partial teleportation
    void handlePartialOverlap(GameEntity* entity, Portal* entryPortal);
    
    // Portal rays for placement
    b2Vec2 castRay(const b2Vec2& start, const b2Vec2& direction, float maxDistance);
    float findPlacementAngle(const b2Vec2& position, const b2Vec2& normal);
};
