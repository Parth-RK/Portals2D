#include "CollisionHandler.h"
#include "../entities/Portal.h"
#include "../entities/GameEntity.h"
#include "../utils/Logger.h"

CollisionHandler::CollisionHandler() {
    LOG_DEBUG("Collision handler initialized");
}

CollisionHandler::~CollisionHandler() {
}

void CollisionHandler::BeginContact(b2Contact* contact) {
    Portal* portal = nullptr;
    GameEntity* entity = nullptr;
    
    // Check if this is a portal contact
    if (isPortalContact(contact, &portal, &entity)) {
        // Store for later processing
        portalCollisions.push_back(std::make_pair(portal, entity));
        LOG_DEBUG("Portal collision detected between portal " + 
                  std::to_string(portal->getId()) + " and entity " + 
                  std::to_string(entity->getId()));
    }
}

void CollisionHandler::EndContact(b2Contact* contact) {
    // Not used in this implementation
}

void CollisionHandler::PreSolve(b2Contact* contact, const b2Manifold* oldManifold) {
    // Not used in this implementation
}

void CollisionHandler::PostSolve(b2Contact* contact, const b2ContactImpulse* impulse) {
    // Not used in this implementation
}

void CollisionHandler::processCollisions() {
    // Process portal collisions
    for (auto& collision : portalCollisions) {
        handlePortalContact(collision.first, collision.second);
    }
    
    // Clear the collision list
    portalCollisions.clear();
}

bool CollisionHandler::isPortalContact(b2Contact* contact, Portal** outPortal, GameEntity** outEntity) {
    // Get fixtures and their user data
    b2Fixture* fixtureA = contact->GetFixtureA();
    b2Fixture* fixtureB = contact->GetFixtureB();
    
    if (!fixtureA || !fixtureB) {
        return false;
    }
    
    b2Body* bodyA = fixtureA->GetBody();
    b2Body* bodyB = fixtureB->GetBody();
    
    if (!bodyA || !bodyB) {
        return false;
    }
    
    void* userData1 = bodyA->GetUserData();
    void* userData2 = bodyB->GetUserData();
    
    if (!userData1 || !userData2) {
        return false;
    }
    
    // Check if one is a portal and one is a dynamic entity
    GameEntity* entity1 = static_cast<GameEntity*>(userData1);
    GameEntity* entity2 = static_cast<GameEntity*>(userData2);
    
    // Case 1: A is portal, B is entity
    if (entity1->getType() == EntityType::PORTAL && entity2->getType() == EntityType::DYNAMIC) {
        *outPortal = static_cast<Portal*>(entity1);
        *outEntity = entity2;
        return true;
    }
    
    // Case 2: B is portal, A is entity
    if (entity2->getType() == EntityType::PORTAL && entity1->getType() == EntityType::DYNAMIC) {
        *outPortal = static_cast<Portal*>(entity2);
        *outEntity = entity1;
        return true;
    }
    
    return false;
}

void CollisionHandler::handlePortalContact(Portal* portal, GameEntity* entity) {
    if (portal && entity && portal->canTeleport()) {
        portal->teleportEntity(entity);
    }
}
