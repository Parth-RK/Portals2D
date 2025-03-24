# Architecture

## Overview

The 2D Portals Game is designed with a modular architecture to ensure maintainability, scalability, and performance on low-spec hardware. The system is divided into several core components, each responsible for a specific aspect of the game.

## Core Components

### 1. **Game Loop**
- Central driver of the game, orchestrating input processing, physics updates, game logic, and rendering.
- Uses a fixed time step for consistent updates.
- **Files:** `src/core/game_loop.py`

### 2. **Input Manager**
- Captures and processes user inputs (keyboard and mouse).
- Maps inputs to game actions such as object manipulation, gravity toggling, and portal creation.
- **Files:** `src/core/input_manager.py`

### 3. **Object Manager**
- Maintains and updates all game objects and portals.
- Handles creation, deletion, and linking of portals.
- **Files:** `src/core/object_manager.py`

### 4. **Physics Engine Integration**
- Provides realistic 2D physics simulation using PyBox2D.
- Manages gravity, collisions, and portal-related physics transformations.
- **Files:** `src/physics/physics_engine.py`

### 5. **Rendering Module**
- Uses Pygame for rendering objects, portals, and UI elements.
- Optimized for low-spec hardware by minimizing overdraw and culling off-screen objects.
- **Files:** `src/rendering/renderer.py`

### 6. **UI Manager**
- Handles in-game controls and user interactions.
- Provides a lightweight interface for object manipulation and portal creation.
- **Files:** `src/ui/ui_manager.py`

### 7. **Error and Logging System**
- Centralized logging for debugging and error tracking.
- Ensures graceful recovery from runtime errors.
- **Files:** `src/utils/logger.py`

## Module Interactions

- The **Game Loop** coordinates data flow between the **Input Manager**, **Physics Engine**, and **Rendering Module**.
- The **Object Manager** ensures synchronization of game entities across modules.
- The **UI Manager** processes user commands and updates the game state.

## Design Goals

- **Performance:** Optimized for low-spec hardware with efficient rendering and physics updates.
- **Modularity:** Clear separation of concerns to facilitate maintenance and future enhancements.
- **Scalability:** Designed to handle increasing complexity, such as additional object types and advanced physics features.

---
