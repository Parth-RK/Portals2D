#include "GameEntity.h"
#include "../utils/Logger.h"

GameEntity::GameEntity(int id, EntityType type) 
    : id(id), type(type), body(nullptr), isActive(true), textureName("") {
    LOG_DEBUG("Created entity with ID: " + std::to_string(id));
}

GameEntity::~GameEntity() {
    LOG_DEBUG("Deleted entity with ID: " + std::to_string(id));
    // Note: Body deletion should be handled by the physics engine
}

b2Vec2 GameEntity::getPosition() const {
    if (body) {
        return body->GetPosition();
    }
    return b2Vec2(0.0f, 0.0f);
}

float GameEntity::getAngle() const {
    if (body) {
        return body->GetAngle();
    }
    return 0.0f;
}
