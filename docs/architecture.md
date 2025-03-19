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
