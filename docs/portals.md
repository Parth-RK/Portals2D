# Portals

## Overview

Portals are a core mechanic of the game, enabling objects to teleport between linked locations while conserving momentum and orientation. They introduce unique gameplay dynamics and require careful implementation to ensure realism and consistency.

## Rules and Behavior

### 1. **Portal Pairs**
- Portals come in pairs of the same color.
- Entering any portal of a color results in exiting through the other portal of the same color.
- Multiple portal pairs can exist simultaneously, each with a unique color.

### 2. **Portal Creation**
- Press **P** to create the first portal of a pair.
- Press **P** again to create the second portal of the pair.
- Press **P** a third time to start creating a new portal pair with a different color.
- Portal colors are automatically assigned in sequence (e.g., Blue, Orange, Green, etc.).

### 3. **Teleportation Mechanics**
- **Entry Detection:** When an object collides with a portal's sensor, it is considered to have entered the portal.
- **Exit Calculation:** The object's position and velocity are transformed based on the relative orientation and position of the linked portal.
- **Momentum Conservation:** The object's velocity is adjusted to preserve momentum during teleportation.
- **Orientation Adjustment:** The object's rotation is recalculated to match the exit portal's orientation.

### 4. **Momentum Conservation**
- Velocity vectors are adjusted to preserve momentum during teleportation.
- The direction and magnitude of the velocity are recalculated based on the exit portal's orientation.

### 5. **Orientation Changes**
- Objects maintain their relative orientation when passing through portals.
- Rotational adjustments are applied to ensure seamless transitions.

## Edge Cases

### Partial Overlaps
- Teleportation is triggered progressively as the object crosses the portal threshold.
- Prevents unintended behavior for objects partially intersecting the portal.

### Blocked Exits
- If the exit portal is obstructed, teleportation is delayed or the object is slightly repositioned to avoid collisions.

### Overlapping Portals
- Placement of overlapping portals is disallowed.
- If portals overlap due to user actions, they are automatically adjusted to resolve the conflict.

## Implementation Details

- **Collision Detection:** Portals use Box2D sensors to detect objects entering their area.
- **Position Transformation:** Entry and exit positions are calculated using the portals' relative positions and orientations.
- **Velocity Transformation:** Velocity vectors are rotated and scaled to match the exit portal's frame of reference.
- **Cooldown Mechanism:** Objects are temporarily marked as "recently teleported" to prevent immediate re-entry into the same portal.

## Testing and Validation
- Extensive testing is performed to ensure smooth transitions at various angles and speeds.
- Edge cases such as rapid successive portal entries and high-speed interactions are thoroughly validated.
