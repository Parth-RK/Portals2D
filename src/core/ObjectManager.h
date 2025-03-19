#pragma once

#include <vector>
#include <memory>
#include <unordered_map>
#include "../entities/GameEntity.h"
#include "../entities/DynamicObject.h"
#include "../entities/Portal.h"

class PhysicsEngine;

class ObjectManager {
private:
    PhysicsEngine* physicsEngine;
    int nextEntityId;
    
    // Collections of game entities
    std::unordered_map<int, std::shared_ptr<GameEntity>> entities;
    std::vector<std::shared_ptr<Portal>> portals;
    std::vector<std::shared_ptr<DynamicObject>> dynamicObjects;
    
public:
    ObjectManager(PhysicsEngine* physics);
    ~ObjectManager();
    
    // Object creation
    std::shared_ptr<DynamicObject> createDynamicObject(ObjectShape shape, float x, float y);
    std::shared_ptr<Portal> createPortal(PortalColor color, float x, float y, float angle);
    
    // Object management
    void destroyEntity(int entityId);
    std::shared_ptr<GameEntity> getEntity(int entityId);
    
    // Portal pair management
    void linkPortals(std::shared_ptr<Portal> portal1, std::shared_ptr<Portal> portal2);
    
    // Update entities
    void update(float deltaTime);
    
    // Getters for collections
    const std::vector<std::shared_ptr<Portal>>& getPortals() const;
    const std::vector<std::shared_ptr<DynamicObject>>& getDynamicObjects() const;
};
