# Architecture Overview

Portals2D is designed with a modular approach, separating responsibilities into distinct manager classes orchestrated by a main `Game` class. This makes the codebase easier to understand, maintain, and potentially extend.

## Core Components

1.  **`Game` (`game.py`): The Orchestrator**
    *   Initializes Pygame and all manager classes.
    *   Loads assets (fonts).
    *   Runs the main game loop (`input -> update -> render`).
    *   Holds references to all other managers.
    *   Manages global game state like `debug_mode`.

2.  **`InputManager` (`input.py`): User Interaction**
    *   Processes Pygame events (keyboard, mouse).
    *   Translates raw input into game actions (e.g., "create object", "start drag", "toggle gravity").
    *   Delegates actions to the appropriate managers (`ObjectManager`, `PortalManager`, `PhysicsManager`, `UIManager`).
    *   Tracks mouse state (position, relative movement, button presses).

3.  **`PhysicsManager` (`physics.py`): The Laws of Physics**
    *   Manages the `Box2D.b2World` instance.
    *   Creates and destroys physics bodies (`b2Body`) for objects and portals.
    *   Configures fixtures (shape, density, friction, sensor status).
    *   Steps the physics simulation forward in time.
    *   Handles collision detection via a `PortalContactListener`.
    *   Provides physics utility functions (applying forces/impulses, querying bodies).
    *   Manages global physics settings like gravity.

4.  **`ObjectManager` (`objects.py`): The Things in the World**
    *   Manages the lifecycle of all `GameObject` instances (`Circle`, `Box`).
    *   Handles creation and deletion requests (coordinating with `PhysicsManager`).
    *   Tracks the currently selected object for dragging.
    *   Manages the Box2D `b2MouseJoint` for drag-and-drop interaction.
    *   Provides ways to query objects (e.g., `get_object_at`).

5.  **`PortalManager` (`portals.py`): The Magic Doors**
    *   Manages the lifecycle of `Portal` instances, grouped into pairs.
    *   Handles user input for creating portal pairs (drag-and-drop on background).
    *   Links portal pairs together.
    *   Manages the teleportation queue and logic, including calculating exit transforms (position, angle, velocity).
    *   Implements the teleport cooldown mechanism.
    *   Coordinates with `PhysicsManager` for portal body creation and the `PortalContactListener`.

6.  **`UIManager` (`ui.py`): Buttons and Displays**
    *   Manages UI elements (currently `Button`).
    *   Provides methods to create UI elements.
    *   Handles input events specifically for UI elements (giving them priority over game world interactions).
    *   Provides the list of UI elements to the `Renderer`.

7.  **`Renderer` (`renderer.py`): Making it Visible**
    *   Handles all drawing onto the Pygame screen.
    *   Draws the background, grid, portals, objects, UI elements, and HUD in the correct order.
    *   Includes logic for debug rendering (physics shapes).
    *   Uses helper functions for drawing specific primitives (circles, polygons).

8.  **`Settings` (`settings.py`): The Rulebook**
    *   Centralizes configuration constants (screen size, FPS, physics parameters, colors, fonts, default object/portal sizes, cooldowns).
    *   Provides essential coordinate conversion functions (`to_pygame`, `to_box2d`).

9.  **`Utils` (`utils.py`): Helpers**
    *   Contains general utility functions used across different modules (e.g., `draw_text`, `get_body_vertices_pygame`, `is_sensor`).

## Main Loop Flow

The `Game.run()` method executes the core loop:

1.  **Calculate Delta Time (`dt`):** Determine time elapsed since the last frame.
2.  **Process Input (`InputManager`):** Handle keyboard/mouse events. This might trigger actions in other managers or change game state.
3.  **Update Game State (`Game.update` -> Manager `update` methods):**
    *   `PhysicsManager.update()`: Steps the Box2D world, resolves collisions, updates body positions.
    *   `PortalManager.update()`: Processes the teleport queue, updates cooldowns.
    *   `ObjectManager.update()`: Cleans up deleted objects, syncs `GameObject` state with `b2Body` state (via `PhysicsManager`).
    *   `UIManager.update()`: Updates any time-dependent UI elements.
4.  **Render Frame (`Game.render` -> `Renderer.render_all`):**
    *   `Renderer` gathers data from managers and draws everything to the back buffer.
5.  **Flip Display:** Show the newly rendered frame on the screen.

This cycle repeats until the user quits.