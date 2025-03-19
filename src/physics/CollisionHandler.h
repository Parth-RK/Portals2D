#pragma once

#include <Box2D/Box2D.h>
#include <vector>
#include <utility>

class Portal;
class GameEntity;

class CollisionHandler : public b2ContactListener {
private:
    // Store portal-object collision pairs for handling in the next physics step
    std::vector<std::pair<Portal*, GameEntity*>> portalCollisions;

public:
    CollisionHandler();
    ~CollisionHandler();
    
    // Box2D contact callback methods
    void BeginContact(b2Contact* contact) override;
    void EndContact(b2Contact* contact) override;
    void PreSolve(b2Contact* contact, const b2Manifold* oldManifold) override;
    void PostSolve(b2Contact* contact, const b2ContactImpulse* impulse) override;
    
    // Process teleportations and other collision events
    void processCollisions();
    
    // Helper methods
    bool isPortalContact(b2Contact* contact, Portal** portal, GameEntity** entity);
    void handlePortalContact(Portal* portal, GameEntity* entity);
};
