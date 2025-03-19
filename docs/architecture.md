# Architecture

## Overview

The 2D Portals Game is designed with a modular architecture to ensure maintainability, scalability, and performance on low-spec hardware. The system is divided into several core components, each responsible for a specific aspect of the game.

## Core Components

### 1. **Game Loop**
- The central driver of the game.
- Handles the sequence of input processing, physics updates, game logic, and rendering.
- Ensures a consistent frame rate by using a fixed time step for updates.
- **Files:**
  - `src/core/GameLoop.h`
  - `src/core/GameLoop.cpp`

### 2. **Input Manager**
- Captures and processes user inputs (keyboard and mouse).
- Maps inputs to game actions such as adding/deleting objects, resizing, and toggling gravity.
- **Files:**
  - `src/core/InputManager.h`
  - `src/core/InputManager.cpp`

### 3. **Object Manager**
- Maintains a list of all game objects and portals.
- Handles creation, deletion, and updates of objects.
- Ensures consistency between the game state and the physics engine.
- **Files:**
  - `src/core/ObjectManager.h`
  - `src/core/ObjectManager.cpp`

### 4. **Physics Engine Integration**
- Uses Box2D for realistic 2D physics simulation.
- Manages gravity, collisions, and momentum conservation.
- Provides a wrapper for applying forces and handling portal interactions.
- **Files:**
  - `src/physics/PhysicsEngine.h`
  - `src/physics/PhysicsEngine.cpp`
  - `src/physics/PortalPhysics.h`
  - `src/physics/PortalPhysics.cpp`
  - `src/physics/CollisionHandler.h`
  - `src/physics/CollisionHandler.cpp`

### 5. **Rendering Module**
- Uses SDL2 for rendering objects, portals, and UI elements.
- Optimized for low-spec hardware by minimizing overdraw and culling off-screen objects.
- **Files:**
  - `src/rendering/Renderer.h`
  - `src/rendering/Renderer.cpp`
  - `src/rendering/TextureManager.h`
  - `src/rendering/TextureManager.cpp`
  - `src/rendering/PortalRenderer.h`
  - `src/rendering/PortalRenderer.cpp`

### 6. **UI Manager**
- Handles in-game controls for object manipulation and gravity toggling.
- Provides a simple and lightweight interface for user interactions.
- **Files:**
  - `src/ui/UIManager.h`
  - `src/ui/UIManager.cpp`
  - `src/ui/Button.h`
  - `src/ui/Button.cpp`
  - `src/ui/Slider.h`
  - `src/ui/Slider.cpp`

### 7. **Error and Logging System**
- Centralized logging for debugging and error tracking.
- Ensures graceful recovery from runtime errors.
- **Files:**
  - `src/utils/Logger.h`
  - `src/utils/Logger.cpp`

## Module Interactions

- The **Game Loop** orchestrates the flow of data between the **Input Manager**, **Physics Engine**, and **Rendering Module**.
- The **Object Manager** acts as the central repository for game entities, ensuring synchronization across modules.
- The **UI Manager** interacts with the **Input Manager** to process user commands and update the game state.

## Design Goals

- **Performance:** Optimized for low-spec hardware with efficient rendering and physics updates.
- **Modularity:** Clear separation of concerns to facilitate maintenance and future enhancements.
- **Scalability:** Designed to handle increasing complexity, such as additional object types or advanced physics features.
