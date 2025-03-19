#pragma once

#include <Box2D/Box2D.h>
#include <memory>
#include "../entities/GameEntity.h"

class CollisionHandler;

class PhysicsEngine {
private:
    std::unique_ptr<b2World> world;
    std::unique_ptr<CollisionHandler> collisionHandler;
    
    b2Vec2 gravity;
    float timeStep;
    int velocityIterations;
    int positionIterations;
    bool gravityEnabled;
    
public:
    PhysicsEngine();
    ~PhysicsEngine();
    
    void initialize();
    void update(float deltaTime);
    
    // Gravity control
    void setGravity(float x, float y);
    b2Vec2 getGravity() const;
    void toggleGravity();
    bool isGravityEnabled() const;
    
    // World management
    b2World* getWorld();
    
    // Body creation helpers
    b2Body* createStaticBody(float x, float y, float angle = 0.0f);
    b2Body* createDynamicBody(float x, float y, float angle = 0.0f);
    
    // Shape and fixture helpers
    b2Fixture* createBoxFixture(b2Body* body, float width, float height, 
                               float density = 1.0f, float friction = 0.3f, 
                               float restitution = 0.5f, bool isSensor = false);
    
    b2Fixture* createCircleFixture(b2Body* body, float radius, 
                                  float density = 1.0f, float friction = 0.3f, 
                                  float restitution = 0.5f, bool isSensor = false);
    
    // Object removal
    void removeBody(b2Body* body);
    
    // Contact listening
    CollisionHandler* getCollisionHandler();
};
