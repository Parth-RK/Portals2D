#pragma once

#include <Box2D/Box2D.h>
#include <cmath>

namespace Math {
    // Vector rotation
    b2Vec2 rotateVector(const b2Vec2& vector, float angle);
    
    // Angle calculations
    float radToDeg(float radians);
    float degToRad(float degrees);
    
    // Distance calculations
    float distance(const b2Vec2& a, const b2Vec2& b);
    
    // Portal transformation calculations
    b2Vec2 transformPosition(const b2Vec2& position, 
                             const b2Vec2& portalEntryPos, 
                             const b2Vec2& portalExitPos, 
                             float portalEntryAngle, 
                             float portalExitAngle);
                             
    b2Vec2 transformVelocity(const b2Vec2& velocity,
                             float portalEntryAngle, 
                             float portalExitAngle);
                             
    float transformAngle(float objectAngle,
                         float portalEntryAngle, 
                         float portalExitAngle);
}
