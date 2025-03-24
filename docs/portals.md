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
- **Cooldown Mechanism:** Prevents immediate re-entry into the same portal.

### 4. **Placement Rules**
- Portals can only be placed on valid surfaces (walls, floors, ceilings).
- Overlapping portals are disallowed or adjusted automatically.

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

---
