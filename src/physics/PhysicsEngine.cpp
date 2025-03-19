#include "PhysicsEngine.h"
#include "CollisionHandler.h"
#include "../utils/Config.h"
#include "../utils/Logger.h"

PhysicsEngine::PhysicsEngine() : 
    gravity(0.0f, 9.8f),
    timeStep(1.0f / 60.0f),
    velocityIterations(8),
    positionIterations(3),
    gravityEnabled(true) {
    
    // Load settings from config
    Config* config = Config::getInstance();
    gravity.x = config->getFloat("physics_gravity_x", 0.0f);
    gravity.y = config->getFloat("physics_gravity_y", 9.8f);
    timeStep = config->getFloat("physics_time_step", 1.0f / 60.0f);
    velocityIterations = config->getInt("physics_velocity_iterations", 8);
    positionIterations = config->getInt("physics_position_iterations", 3);
}

PhysicsEngine::~PhysicsEngine() {
    // Box2D world will clean up all bodies and fixtures
}

void PhysicsEngine::initialize() {
    // Create the Box2D world with the configured gravity
    world = std::make_unique<b2World>(gravity);
    
    // Create and set the collision handler
    collisionHandler = std::make_unique<CollisionHandler>();
    world->SetContactListener(collisionHandler.get());
    
    LOG_INFO("Physics engine initialized with gravity (" + 
             std::to_string(gravity.x) + ", " + 
             std::to_string(gravity.y) + ")");
}

void PhysicsEngine::update(float deltaTime) {
    if (world) {
        // Use fixed time step for stability
        world->Step(timeStep, velocityIterations, positionIterations);
    }
}

void PhysicsEngine::setGravity(float x, float y) {
    gravity.Set(x, y);
    if (world) {
        world->SetGravity(gravity);
    }
    
    LOG_DEBUG("Gravity set to (" + std::to_string(x) + ", " + std::to_string(y) + ")");
}

b2Vec2 PhysicsEngine::getGravity() const {
    return gravity;
}

void PhysicsEngine::toggleGravity() {
    gravityEnabled = !gravityEnabled;
    
    if (gravityEnabled) {
        if (world) {
            world->SetGravity(gravity);
        }
        LOG_DEBUG("Gravity enabled");
    } else {
        if (world) {
            world->SetGravity(b2Vec2(0.0f, 0.0f));
        }
        LOG_DEBUG("Gravity disabled");
    }
}

bool PhysicsEngine::isGravityEnabled() const {
    return gravityEnabled;
}

b2World* PhysicsEngine::getWorld() {
    return world.get();
}

b2Body* PhysicsEngine::createStaticBody(float x, float y, float angle) {
    if (!world) {
        LOG_ERROR("Cannot create static body, physics world is not initialized");
        return nullptr;
    }
    
    b2BodyDef bodyDef;
    bodyDef.type = b2_staticBody;
    bodyDef.position.Set(x, y);
    bodyDef.angle = angle;
    
    return world->CreateBody(&bodyDef);
}

b2Body* PhysicsEngine::createDynamicBody(float x, float y, float angle) {
    if (!world) {
        LOG_ERROR("Cannot create dynamic body, physics world is not initialized");
        return nullptr;
    }
    
    b2BodyDef bodyDef;
    bodyDef.type = b2_dynamicBody;
    bodyDef.position.Set(x, y);
    bodyDef.angle = angle;
    
    return world->CreateBody(&bodyDef);
}

b2Fixture* PhysicsEngine::createBoxFixture(b2Body* body, float width, float height, 
                                         float density, float friction, 
                                         float restitution, bool isSensor) {
    if (!body) {
        LOG_ERROR("Cannot create box fixture, body is null");
        return nullptr;
    }
    
    b2PolygonShape boxShape;
    boxShape.SetAsBox(width / 2.0f, height / 2.0f);
    
    b2FixtureDef fixtureDef;
    fixtureDef.shape = &boxShape;
    fixtureDef.density = density;
    fixtureDef.friction = friction;
    fixtureDef.restitution = restitution;
    fixtureDef.isSensor = isSensor;
    
    return body->CreateFixture(&fixtureDef);
}

b2Fixture* PhysicsEngine::createCircleFixture(b2Body* body, float radius, 
                                            float density, float friction, 
                                            float restitution, bool isSensor) {
    if (!body) {
        LOG_ERROR("Cannot create circle fixture, body is null");
        return nullptr;
    }
    
    b2CircleShape circleShape;
    circleShape.m_radius = radius;
    
    b2FixtureDef fixtureDef;
    fixtureDef.shape = &circleShape;
    fixtureDef.density = density;
    fixtureDef.friction = friction;
    fixtureDef.restitution = restitution;
    fixtureDef.isSensor = isSensor;
    
    return body->CreateFixture(&fixtureDef);
}

void PhysicsEngine::removeBody(b2Body* body) {
    if (world && body) {
        world->DestroyBody(body);
    }
}

CollisionHandler* PhysicsEngine::getCollisionHandler() {
    return collisionHandler.get();
}
