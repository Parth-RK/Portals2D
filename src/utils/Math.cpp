#include "Math.h"

namespace Math {
    b2Vec2 rotateVector(const b2Vec2& vector, float angle) {
        float sin_val = sin(angle);
        float cos_val = cos(angle);
        
        return b2Vec2(
            vector.x * cos_val - vector.y * sin_val,
            vector.x * sin_val + vector.y * cos_val
        );
    }
    
    float radToDeg(float radians) {
        return radians * 180.0f / M_PI;
    }
    
    float degToRad(float degrees) {
        return degrees * M_PI / 180.0f;
    }
    
    float distance(const b2Vec2& a, const b2Vec2& b) {
        float dx = b.x - a.x;
        float dy = b.y - a.y;
        return sqrt(dx * dx + dy * dy);
    }
    
    b2Vec2 transformPosition(const b2Vec2& position,
                           const b2Vec2& portalEntryPos,
                           const b2Vec2& portalExitPos,
                           float portalEntryAngle,
                           float portalExitAngle) {
        // Calculate position relative to entry portal
        b2Vec2 relativePos = position - portalEntryPos;
        
        // Rotate position based on the difference in portal orientations
        float angleDiff = portalExitAngle - portalEntryAngle;
        b2Vec2 rotatedPos = rotateVector(relativePos, angleDiff);
        
        // Offset from exit portal position
        return portalExitPos + rotatedPos;
    }
    
    b2Vec2 transformVelocity(const b2Vec2& velocity,
                           float portalEntryAngle,
                           float portalExitAngle) {
        // Rotate velocity vector by the difference in portal orientations
        float angleDiff = portalExitAngle - portalEntryAngle;
        return rotateVector(velocity, angleDiff);
    }
    
    float transformAngle(float objectAngle,
                       float portalEntryAngle,
                       float portalExitAngle) {
        // Adjust the object angle by the difference in portal orientations
        float angleDiff = portalExitAngle - portalEntryAngle;
        return objectAngle + angleDiff;
    }
}
