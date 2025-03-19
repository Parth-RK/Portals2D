# Physics

## Overview

The physics system is built on Box2D to provide realistic 2D physics simulation. It handles object interactions, collisions, gravity, and portal transitions while maintaining performance on low-spec hardware.

## Key Features

### 1. **Gravity**
- A global gravity vector affects all dynamic objects.
- Can be toggled on or off via user input.
- Smoothly adapts ongoing simulations to changes in gravity.

### 2. **Collisions**
- Uses Box2D's collision detection and response mechanisms.
- Handles object-to-object and object-to-portal interactions.
- Ensures stability and realism during high-speed interactions.

### 3. **Momentum Conservation**
- Objects retain their momentum when passing through portals.
- Velocity vectors are transformed based on the orientation of the entry and exit portals.

### 4. **Portal Transitions**
- Objects entering a portal are teleported to the linked portal's exit.
- Position and velocity are recalculated to ensure seamless transitions.
- Handles edge cases such as partial overlaps and blocked exits.

## Implementation Details

### Fixed Time Step
- Physics updates use a fixed time step to ensure determinism and stability.
- Prevents inconsistencies caused by variable frame rates.

### Object Management
- Dynamic objects and portals are represented as Box2D bodies.
- Changes to object properties (e.g., size, position) are reflected in the physics engine.

### Edge Case Handling
- **Overlapping Portals:** Prevent placement or resolve overlaps by snapping portals apart.
- **Blocked Exits:** Delay teleportation or adjust object positions to avoid collisions.
- **High Object Density:** Limit the number of active objects to maintain performance.

## Optimization
- Spatial partitioning (e.g., quad-trees) for efficient collision detection.
- Preallocated object pools to reduce memory allocation overhead.
- Simplified physics calculations for non-critical objects.
