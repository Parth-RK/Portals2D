#include "DynamicObject.h"
#include "../utils/Logger.h"

DynamicObject::DynamicObject(int id, ObjectShape shape) 
    : GameEntity(id, EntityType::DYNAMIC), 
      shape(shape), 
      width(1.0f), 
      height(1.0f), 
      radius(0.5f), 
      density(1.0f), 
      friction(0.3f), 
      restitution(0.5f) {
}

DynamicObject::~DynamicObject() {
    // Body disposal is handled by the physics world
}

void DynamicObject::initialize(b2World* world, float x, float y) {
    if (!world) {
        LOG_ERROR("Cannot initialize dynamic object, world is null");
        return;
    }
    
    // Define the dynamic body
    b2BodyDef bodyDef;
    bodyDef.type = b2_dynamicBody;
    bodyDef.position.Set(x, y);
    bodyDef.userData = this;
    body = world->CreateBody(&bodyDef);
    
    // Create shape
    b2FixtureDef fixtureDef;
    
    switch (shape) {
        case ObjectShape::CIRCLE: {
            b2CircleShape circleShape;
            circleShape.m_radius = radius;
            fixtureDef.shape = &circleShape;
            break;
        }
        case ObjectShape::RECTANGLE: {
            b2PolygonShape boxShape;
            boxShape.SetAsBox(width / 2.0f, height / 2.0f);
            fixtureDef.shape = &boxShape;
            break;
        }
        case ObjectShape::POLYGON: {
            // For simplicity, we'll create a triangular shape
            b2PolygonShape polygonShape;
            b2Vec2 vertices[3];
            vertices[0].Set(-width/2, -height/2);
            vertices[1].Set(width/2, -height/2);
            vertices[2].Set(0, height/2);
            polygonShape.Set(vertices, 3);
            fixtureDef.shape = &polygonShape;
            break;
        }
    }
    
    // Set physics properties
    fixtureDef.density = density;
    fixtureDef.friction = friction;
    fixtureDef.restitution = restitution;
    
    body->CreateFixture(&fixtureDef);
    
    LOG_DEBUG("Initialized dynamic object " + std::to_string(id) + " at position (" + 
              std::to_string(x) + ", " + std::to_string(y) + ")");
}

void DynamicObject::setSize(float newWidth, float newHeight) {
    if (body) {
        LOG_WARNING("Cannot change size of object after initialization");
        return;
    }
    
    width = newWidth;
    height = newHeight;
}

void DynamicObject::setRadius(float newRadius) {
    if (body) {
        LOG_WARNING("Cannot change radius of object after initialization");
        return;
    }
    
    radius = newRadius;
}

void DynamicObject::setDensity(float newDensity) {
    density = newDensity;
    
    // Update fixture if body exists
    if (body && body->GetFixtureList()) {
        body->GetFixtureList()->SetDensity(density);
        body->ResetMassData();
    }
}

void DynamicObject::setFriction(float newFriction) {
    friction = newFriction;
    
    // Update fixture if body exists
    if (body && body->GetFixtureList()) {
        body->GetFixtureList()->SetFriction(friction);
    }
}

void DynamicObject::setRestitution(float newRestitution) {
    restitution = newRestitution;
    
    // Update fixture if body exists
    if (body && body->GetFixtureList()) {
        body->GetFixtureList()->SetRestitution(restitution);
    }
}

void DynamicObject::applyForce(const b2Vec2& force) {
    if (body) {
        body->ApplyForceToCenter(force, true);
    }
}

void DynamicObject::applyImpulse(const b2Vec2& impulse) {
    if (body) {
        body->ApplyLinearImpulseToCenter(impulse, true);
    }
}

void DynamicObject::setVelocity(const b2Vec2& velocity) {
    if (body) {
        body->SetLinearVelocity(velocity);
    }
}

b2Vec2 DynamicObject::getVelocity() const {
    if (body) {
        return body->GetLinearVelocity();
    }
    return b2Vec2(0.0f, 0.0f);
}

void DynamicObject::update(float deltaTime) {
    // Most of the physics is handled by Box2D
    // This can be extended for additional behavior
}

void DynamicObject::render() {
    // Rendering is handled by the Renderer class
    // This method is left empty as a placeholder
}
