# Portals

## Overview

Portals enable objects to teleport between linked locations while conserving momentum and orientation. They introduce unique gameplay dynamics and require careful implementation to ensure realism and consistency.

## Rules and Behavior

### 1. **Portal Pairs**
- Portals are created in pairs, each with a unique color.
- Entering one portal results in exiting through its linked portal.

### 2. **Portal Creation**
- Press **P** to create the first portal of a pair.
- Press **P** again to create the second portal.
- Additional presses create new portal pairs with different colors.

### 3. **Teleportation Mechanics**
- **Entry Detection:** Objects entering a portal's sensor are teleported.
- **Exit Calculation:** Position and velocity are transformed based on the linked portal's orientation.
- **Directional Indicators:** Arrows on portals show the exit direction.
- **Animations:**
  - Objects shrink and fade out when entering a portal.
  - Objects grow and fade in when exiting a portal.

### 4. **Placement Rules**
- Portals can only be placed on valid surfaces (walls, floors, ceilings).
- Overlapping portals are disallowed or adjusted automatically.

### 5. **Adjustments**
- **Size and Rotation:**
  - Use sliders to adjust portal size (scale from 0.5x to 2.0x).
  - Use sliders to rotate portals (0° to 360°).

## Advanced Features

### Momentum and Orientation
- Velocity and rotation are adjusted to ensure momentum conservation and proper orientation upon exiting.

### Edge Cases
- **Blocked Exits:** Teleportation is delayed or adjusted to avoid collisions.
- **Object Too Large:** Objects too large to fit are rejected.
- **Portal Closure:** Objects are pushed back or handled gracefully if a portal closes during traversal.

## Implementation Summary

| Feature              | Implementation Strategy                              |
|----------------------|----------------------------------------------------|
| Portal Entry & Exit  | Box2D sensors detect intersections, apply transformations |
| Physics Preservation | Velocity and rotation adjustments ensure realism   |
| Placement Rules      | Constraints prevent invalid or overlapping portals |
| Directional Indicators | Arrows show exit direction for better clarity    |
| Animations           | Smooth shrinking, fading, and particle effects     |

---
