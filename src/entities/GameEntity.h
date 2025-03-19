#pragma once

#include <Box2D/Box2D.h>
#include <string>

enum class EntityType {
    STATIC,
    DYNAMIC,
    PORTAL
};

class GameEntity {
protected:
    int id;
    EntityType type;
    b2Body* body;
    bool isActive;
    std::string textureName;
    
public:
    GameEntity(int id, EntityType type);
    virtual ~GameEntity();
    
    // Basic getters
    int getId() const { return id; }
    EntityType getType() const { return type; }
    b2Body* getBody() const { return body; }
    bool getIsActive() const { return isActive; }
    std::string getTextureName() const { return textureName; }
    
    // Position and rotation
    b2Vec2 getPosition() const;
    float getAngle() const;
    
    // Basic setters
    void setIsActive(bool active) { isActive = active; }
    void setTextureName(const std::string& name) { textureName = name; }
    
    // Virtual methods for entity behavior
    virtual void update(float deltaTime) = 0;
    virtual void render() = 0;
};
