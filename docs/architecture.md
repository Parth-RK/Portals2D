# Architecture

## Overview

The 2D Portals Game is designed with a modular architecture to ensure maintainability, scalability, and performance on low-spec hardware. The system is divided into several core components, each responsible for a specific aspect of the game.

## Core Components

### 1. **Game Loop**
- The central driver of the game.
- Handles the sequence of input processing, physics updates, game logic, and rendering.
- Ensures a consistent frame rate by using a fixed time step for updates.
- **Files:**
  - `src/core/game_loop.py`

### 2. **Input Manager**
- Captures and processes user inputs (keyboard and mouse).
- Maps inputs to game actions such as adding/deleting objects, resizing, toggling gravity, and creating portals.
- **Files:**
  - `src/core/input_manager.py`

### 3. **Object Manager**
- Maintains a list of all game objects and portals.
- Handles creation, deletion, and updates of objects.
- Ensures consistency between the game state and the physics engine.
- **Files:**
  - `src/core/object_manager.py`

### 4. **Physics Engine Integration**
- Uses PyBox2D for realistic 2D physics simulation.
- Manages gravity, collisions, and momentum conservation.
- Provides a wrapper for applying forces and handling portal interactions.
- **Files:**
  - `src/physics/physics_engine.py`

### 5. **Rendering Module**
- Uses Pygame for rendering objects, portals, and UI elements.
- Optimized for low-spec hardware by minimizing overdraw and culling off-screen objects.
- **Files:**
  - `src/rendering/renderer.py`

### 6. **UI Manager**
- Handles in-game controls for object manipulation, gravity toggling, and portal creation.
- Provides a simple and lightweight interface for user interactions.
- **Files:**
  - `src/ui/ui_manager.py`

### 7. **Error and Logging System**
- Centralized logging for debugging and error tracking.
- Ensures graceful recovery from runtime errors.
- **Files:**
  - `src/utils/logger.py`

## Module Interactions

- The **Game Loop** orchestrates the flow of data between the **Input Manager**, **Physics Engine**, and **Rendering Module**.
- The **Object Manager** acts as the central repository for game entities, ensuring synchronization across modules.
- The **UI Manager** interacts with the **Input Manager** to process user commands and update the game state.

## Design Goals

- **Performance:** Optimized for low-spec hardware with efficient rendering and physics updates.
- **Modularity:** Clear separation of concerns to facilitate maintenance and future enhancements.
- **Scalability:** Designed to handle increasing complexity, such as additional object types, advanced physics features, and multiple portal pairs.

## Portal System Architecture

### Overview
The portal system is designed to allow seamless teleportation of objects between linked portals while conserving momentum and orientation. The system relies on Box2D for collision detection and physics simulation.

### Components

#### 1. **Portal Class**
- Represents a single portal in the game.
- Stores properties such as position, orientation, color, and a reference to its linked portal.
- Contains logic for detecting collisions with objects and teleporting them to the linked portal.

#### 2. **Portal Pairing**
- Portals are created in pairs, with each pair sharing the same color.
- The `ObjectManager` maintains a dictionary of portal pairs, allowing efficient lookup and linking.

#### 3. **Collision Detection**
- Each portal has a Box2D sensor that detects when an object enters its area.
- The sensor triggers the teleportation logic when a collision is detected.

#### 4. **Teleportation Logic**
- **Entry Detection:** When an object collides with a portal's sensor, the portal checks if it is linked to another portal.
- **Position Transformation:** The object's position is recalculated relative to the linked portal's position and orientation.
- **Velocity Transformation:** The object's velocity is rotated and scaled to match the linked portal's frame of reference.
- **Cooldown Mechanism:** The object is marked as "recently teleported" to prevent immediate re-entry into the same portal.

#### 5. **Momentum and Orientation**
- The object's velocity and rotation are adjusted to ensure momentum conservation and proper orientation upon exiting the linked portal.

### Workflow

1. **Portal Creation**
   - The player presses **P** to create a portal.
   - The first press creates the entry portal, and the second press creates the exit portal.
   - The portals are linked automatically by the `ObjectManager`.

2. **Object Teleportation**
   - When an object enters a portal's sensor:
     - The portal checks if it is linked to another portal.
     - The object's position and velocity are transformed based on the linked portal's properties.
     - The object is teleported to the linked portal's exit.

3. **Cooldown Mechanism**
   - After teleportation, the object is added to a "recently teleported" list.
   - The object cannot re-enter the same portal until the cooldown period expires.

### Data Flow

1. **Input Manager**
   - Detects player input for creating portals.

2. **Object Manager**
   - Manages the creation and linking of portals.
   - Updates portal states and handles teleportation logic.

3. **Physics Engine**
   - Detects collisions between objects and portal sensors.
   - Updates object positions and velocities during teleportation.

4. **Renderer**
   - Draws portals and objects on the screen.
   - Visualizes the teleportation process.

### Key Classes and Methods

#### **Portal Class**
- `link_portal(other_portal)`: Links this portal to another portal.
- `check_collision(game_object)`: Checks if an object is colliding with the portal.
- `teleport_object(game_object)`: Teleports an object to the linked portal.

#### **ObjectManager**
- `create_portal(color, portal_id, x, y, angle)`: Creates a new portal or updates an existing one.
- `update(dt)`: Updates all portals and handles teleportation logic.

#### **PhysicsEngine**
- `create_portal_sensor(portal)`: Creates a Box2D sensor for a portal.
- `update(dt)`: Steps the physics simulation and processes collisions.

---

This detailed architecture ensures that the portal system is modular, efficient, and easy to maintain. It also provides a clear roadmap for debugging and extending the system in the future.
