# Portals

## Overview

Portals are a core mechanic of the game, enabling objects to teleport between linked locations while conserving momentum and orientation. They introduce unique gameplay dynamics and require careful implementation to ensure realism and consistency.

## Rules and Behavior

### 1. **Portal Linking**
- Portals are always created in pairs (entry and exit).
- Each portal has a unique identifier and a reference to its linked portal.

### 2. **Teleportation**
- Objects entering a portal gradually appear on the other side as they pass through.
- For example, if a human-shaped figure inserts its hand into the portal, only the hand will appear on the other side. As the figure moves further into the portal, the rest of the body will appear correspondingly.
- The object's position and velocity are transformed based on the relative orientation of the portals.

### 3. **Momentum Conservation**
- Velocity vectors are adjusted to preserve momentum during teleportation.
- The direction and magnitude of the velocity are recalculated based on the exit portal's orientation.

### 4. **Orientation Changes**
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

## Testing and Validation
- Extensive testing is performed to ensure smooth transitions at various angles and speeds.
- Edge cases such as rapid successive portal entries and high-speed interactions are thoroughly validated.
