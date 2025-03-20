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
- **Object Duplication:** During teleportation, two instances of the object exist momentarily - one fading out at the entry portal and another appearing at the exit portal.
- **Portal Movement:** Portals attached to moving platforms will move with their platform, maintaining their relative position.

## Testing and Validation
- Extensive testing is performed to ensure smooth transitions at various angles and speeds.
- Edge cases such as rapid successive portal entries and high-speed interactions are thoroughly validated.
- Specific tests for objects of different sizes ensure proper handling of partial and complete teleportation.
- Stress tests validate performance under conditions with multiple active portal pairs and objects.

## Portal Architecture

### Core Concept
A portal in our 2D game is a **connected pair of spatial discontinuities** that allow objects to enter one portal and exit through the other while maintaining momentum, orientation, and physical interactions. Each portal in a pair has:
- **Entry Boundary:** The line or shape defining the active area of the portal.
- **Exit Point:** The corresponding location in space where objects reappear after entering.
- **Orientation:** Each portal has a facing direction, which determines how objects are transformed upon exiting.

### Spatial Representation
- Each portal is represented as a **rectangular doorway** with a clearly defined boundary.
- The game engine maintains a **mapping between linked portals**, ensuring that entering one results in exiting the other seamlessly.

## Advanced Portal Behaviors

### Placement Rules
- **Surface Constraints:** Portals can only be placed on valid surfaces (walls, floors, ceilings).
- **Size Limits:** Portals have a predefined size to maintain game balance.
- **Overlap Handling:** If a portal overlaps an existing object, the placement is adjusted to avoid clipping or rejected with feedback to the player.

### Physics Preservation
- **Momentum is Preserved:** Objects maintain their velocity when passing through portals, adjusted for the new orientation.
- **Gravity Considerations:** Objects retain their relationship with gravity after passing through portals.
- **Angular Momentum:** Rotational states persist during portal transitions.
- **Energy Conservation:** Objects neither gain nor lose energy when transitioning through portals.

## Edge Cases & Error Handling

### Object Stuck in a Portal
- If an object gets stuck between two portals:
  - A **small push force** is applied to prevent indefinite oscillation.
  - If still stuck after a threshold time, the object is teleported to a safe location.

### Object Too Large for Portal
- If an object is too large to pass through a portal:
  - The object is prevented from entering (rejected).
  - Partial teleportation mechanics handle objects that are partially inside the portal.

### Portal Closure During Traversal
- If a portal closes while an object is passing through:
  - The object is either pushed back to the entry side.
  - Or handled according to game mechanics (respawn, damage, etc.).

### High-Speed Entry
- For objects entering portals at extremely high velocity:
  - The physics engine ensures proper tracking and transfer without frame skipping.
  - A smooth transition effect prevents sudden visual snapping.

## Technical Implementation Summary

| Feature | Implementation Strategy |
|---------|------------------------|
| Portal Entry & Exit | Box2D sensors detect intersections, apply position/velocity transformations |
| Physics Preservation | Vector calculations maintain velocity, gravity effects, and rotation |
| Portal Closing Rules | Objects are ejected when portals close on invalid surfaces |
| Object Duplication | Temporary duplicate objects manage transition visual effects |
| Edge Case Handling | Push forces, size limits, and recursion prevention mechanisms |

These implementation strategies ensure a **smooth, realistic, and error-free** portal system that maintains gameplay integrity while providing the unique spatial manipulation that makes portal mechanics engaging.
