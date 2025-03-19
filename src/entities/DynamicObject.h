#pragma once

#include "GameEntity.h"

enum class ObjectShape {
    CIRCLE,
    RECTANGLE,
    POLYGON
};

class DynamicObject : public GameEntity {
private:
    ObjectShape shape;
    float width;
    float height;
    float radius;  // Used for circular objects
    float density;
    float friction;
    float restitution;
    
public:
    DynamicObject(int id, ObjectShape shape);
    ~DynamicObject();
    
    // Initialize with physics body
    void initialize(b2World* world, float x, float y);
    
    // Shape getters and setters
    ObjectShape getShape() const { return shape; }
    void setSize(float width, float height);
    void setRadius(float radius);
    float getWidth() const { return width; }
    float getHeight() const { return height; }
    float getRadius() const { return radius; }
    
    // Physics properties
    void setDensity(float density);
    void setFriction(float friction);
    void setRestitution(float restitution);
    float getDensity() const { return density; }
    float getFriction() const { return friction; }
    float getRestitution() const { return restitution; }
    
    // Movement
    void applyForce(const b2Vec2& force);
    void applyImpulse(const b2Vec2& impulse);
    void setVelocity(const b2Vec2& velocity);
    b2Vec2 getVelocity() const;
    
    // GameEntity methods
    void update(float deltaTime) override;
    void render() override;
};
