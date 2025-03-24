# Physics

## Overview

The physics system is built on Box2D to provide realistic 2D physics simulation. It handles object interactions, collisions, gravity, and portal transitions while maintaining performance on low-spec hardware.

## Key Features

### 1. **Gravity**
- Affects all dynamic objects globally.
- Can be toggled on or off via user input.

### 2. **Collisions**
- Handles object-to-object and object-to-portal interactions.
- Ensures stability during high-speed interactions.

### 3. **Portal Transitions**
- Objects entering a portal are teleported to the linked portal's exit.
- Position and velocity are recalculated to ensure seamless transitions.

### 4. **Object Manipulation**
- Users can drag and throw objects with momentum.
- Right-clicking opens a context menu for resizing and rotating objects.

## Implementation Details

### Fixed Time Step
- Ensures determinism and stability in physics updates.

### Object Management
- Dynamic objects and portals are represented as Box2D bodies.

### Optimization
- Spatial partitioning for efficient collision detection.
- Object pools reduce memory allocation overhead.

---
