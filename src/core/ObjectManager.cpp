#include "ObjectManager.h"
#include "../physics/PhysicsEngine.h"
#include "../utils/Config.h"
#include "../utils/Logger.h"

ObjectManager::ObjectManager(PhysicsEngine* physics) : 
    physicsEngine(physics),
    nextEntityId(1) {
    
    LOG_INFO("Object manager initialized");
}

ObjectManager::~ObjectManager() {
    // Clear all objects
    entities.clear();
    portals.clear();
    dynamicObjects.clear();
    
    LOG_INFO("Object manager destroyed");
}

std::shared_ptr<DynamicObject> ObjectManager::createDynamicObject(ObjectShape shape, float x, float y) {
    if (!physicsEngine || !physicsEngine->getWorld()) {
        LOG_ERROR("Cannot create object: physics engine not initialized");
        return nullptr;
    }
    
    // Check if we're at the object limit
    Config* config = Config::getInstance();
    int maxObjects = config->getInt("max_dynamic_objects", 100);
    
    if (dynamicObjects.size() >= maxObjects) {
        LOG_WARNING("Maximum object limit reached (" + std::to_string(maxObjects) + ")");
        return nullptr;
    }
    
    // Create the object
    auto object = std::make_shared<DynamicObject>(nextEntityId++, shape);
    object->initialize(physicsEngine->getWorld(), x, y);
    
    // Store in collections
    entities[object->getId()] = object;
    dynamicObjects.push_back(object);
    
    LOG_INFO("Created dynamic object " + std::to_string(object->getId()) + 
             " at (" + std::to_string(x) + ", " + std::to_string(y) + ")");
    
    return object;
}

std::shared_ptr<Portal> ObjectManager::createPortal(PortalColor color, float x, float y, float angle) {
    if (!physicsEngine || !physicsEngine->getWorld()) {
        LOG_ERROR("Cannot create portal: physics engine not initialized");
        return nullptr;
    }
    
    // Check if we're at the portal limit
    Config* config = Config::getInstance();
    int maxPortals = config->getInt("max_portals", 2);
    
    if (portals.size() >= maxPortals) {
        LOG_WARNING("Maximum portal limit reached (" + std::to_string(maxPortals) + ")");
        return nullptr;
    }
    
    // Create the portal
    auto portal = std::make_shared<Portal>(nextEntityId++, color);
    portal->initialize(physicsEngine->getWorld(), x, y, angle);
    
    // Store in collections
    entities[portal->getId()] = portal;
    portals.push_back(portal);
    
    LOG_INFO("Created portal " + std::to_string(portal->getId()) + 
             " at (" + std::to_string(x) + ", " + std::to_string(y) + ")");
    
    return portal;
}

void ObjectManager::destroyEntity(int entityId) {
    auto it = entities.find(entityId);
    if (it == entities.end()) {
        LOG_WARNING("Attempted to destroy non-existent entity with ID " + std::to_string(entityId));
        return;
    }
    
    auto entity = it->second;
    
    // Remove from physics world if it has a body
    if (entity->getBody() && physicsEngine) {
        physicsEngine->removeBody(entity->getBody());
    }
    
    // Remove from appropriate collection
    if (entity->getType() == EntityType::DYNAMIC) {
        auto dynamicIt = std::find_if(dynamicObjects.begin(), dynamicObjects.end(),
            [entityId](const std::shared_ptr<DynamicObject>& obj) {
                return obj->getId() == entityId;
            });
            
        if (dynamicIt != dynamicObjects.end()) {
            dynamicObjects.erase(dynamicIt);
        }
    }
    else if (entity->getType() == EntityType::PORTAL) {
        auto portalIt = std::find_if(portals.begin(), portals.end(),
            [entityId](const std::shared_ptr<Portal>& p) {
                return p->getId() == entityId;
            });
            
        if (portalIt != portals.end()) {
            portals.erase(portalIt);
        }
    }
    
    // Remove from main entities map
    entities.erase(it);
    
    LOG_INFO("Destroyed entity " + std::to_string(entityId));
}

std::shared_ptr<GameEntity> ObjectManager::getEntity(int entityId) {
    auto it = entities.find(entityId);
    if (it != entities.end()) {
        return it->second;
    }
    return nullptr;
}

void ObjectManager::linkPortals(std::shared_ptr<Portal> portal1, std::shared_ptr<Portal> portal2) {
    if (!portal1 || !portal2 || portal1 == portal2) {
        LOG_WARNING("Invalid portal linking attempt");
        return;
    }
    
    portal1->linkTo(portal2);
    portal2->linkTo(portal1);
    
    LOG_INFO("Linked portals " + std::to_string(portal1->getId()) + 
             " and " + std::to_string(portal2->getId()));
}

void ObjectManager::update(float deltaTime) {
    // Update all entities
    for (auto& pair : entities) {
        if (pair.second && pair.second->getIsActive()) {
            pair.second->update(deltaTime);
        }
    }
}

const std::vector<std::shared_ptr<Portal>>& ObjectManager::getPortals() const {
    return portals;
}

const std::vector<std::shared_ptr<DynamicObject>>& ObjectManager::getDynamicObjects() const {
    return dynamicObjects;
}
