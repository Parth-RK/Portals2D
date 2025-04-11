# API Reference

## Modules

### `game.py`
- **Class `Game`**: Main game class orchestrating initialization, game loop, and managers.

### `input.py`
- **Class `InputManager`**: Handles user input and events.

### `physics.py`
- **Class `PhysicsManager`**: Manages the physics world and interactions.
- **Class `PortalContactListener`**: Listens for collisions involving portals.

### `objects.py`
- **Class `GameObject`**: Base class for all game objects.
- **Class `Circle`**: Represents circular objects.
- **Class `Box`**: Represents box-shaped objects.
- **Class `ObjectManager`**: Manages all game objects.

### `portals.py`
- **Class `Portal`**: Represents a single portal.
- **Class `PortalManager`**: Manages portal pairs and teleportation.

### `renderer.py`
- **Class `Renderer`**: Handles rendering of all game elements.

### `ui.py`
- **Class `Button`**: Represents a clickable button.
- **Class `UIManager`**: Manages UI elements.

### `utils.py`
- Utility functions for coordinate conversion, text rendering, and more.






# Core Systems Deep Dive

This document provides a more detailed look into the implementation and logic of the key systems within Portals2D.

## Physics (`PhysicsManager`, Box2D)

*   **Engine:** Uses the `Box2D-py` library for 2D rigid body simulation.
*   **World:** The `PhysicsManager` manages a `Box2D.b2World` instance, configured with gravity and simulation parameters from `settings.py`.
*   **Coordinate System:** Box2D uses meters, kilograms, and seconds (MKS) with a Y-up coordinate system. Pygame uses pixels with a Y-down system. The `settings.PPM` (Pixels Per Meter) constant and the `to_pygame`/`to_box2d` functions are crucial for conversion.
*   **Bodies (`b2Body`):**
    *   **Dynamic:** For movable objects (`Circle`, `Box`). Affected by forces, gravity, collisions. Created via `PhysicsManager.add_object`.
    *   **Static:** For immovable elements like boundaries and the ground anchor for the mouse joint. Created via `PhysicsManager.add_boundaries` or internally. Portals also use static bodies but with sensor fixtures.
    *   **UserData:** Each body's `userData` attribute stores a dictionary linking back to the corresponding `GameObject` or `Portal` instance and its type (`USER_DATA_OBJECT`, `USER_DATA_PORTAL`).
*   **Fixtures (`b2Fixture`):** Define the shape, physical properties (density, friction, restitution), and collision filtering for a part of a body.
    *   **Sensors:** Portal fixtures are marked as `isSensor=True`. Sensors detect collisions but don't generate physical responses (objects pass through them). Used to trigger portal entry detection. The `utils.is_sensor()` function provides a safe way to check this status.
*   **Simulation Step:** `PhysicsManager.update()` calls `world.Step()` each frame, advancing the simulation using `settings.TIME_STEP`, `VELOCITY_ITERATIONS`, and `POSITION_ITERATIONS`.
*   **Contact Listener (`PortalContactListener`):** Attached to the `world`, this listener's `BeginContact` method is called by Box2D when fixtures start touching. It specifically checks for contacts between dynamic `USER_DATA_OBJECT` fixtures and sensor `USER_DATA_PORTAL` fixtures. If an object enters a portal correctly (moving towards it, not on cooldown, not just exited the partner), it queues the object for teleportation via `PortalManager.queue_teleportation()`.
*   **Body Management:** Bodies scheduled for deletion are added to a `bodies_to_destroy` list in `PhysicsManager` and removed safely at the start of the next `update` cycle, avoiding modification during physics callbacks.

## Game Objects (`ObjectManager`, `GameObject`, `Circle`, `Box`)

*   **Hierarchy:** `GameObject` is the base class, holding common properties (ID, position, angle, color, physics body reference, deletion flag). `Circle` and `Box` inherit from `GameObject`, adding shape-specific properties (radius, size).
*   **Lifecycle:**
    *   Created via `ObjectManager.create_object()`, which instantiates the `GameObject` and requests physics body creation from `PhysicsManager`.
    *   Managed in the `ObjectManager.objects` list.
    *   Deleted via `ObjectManager.delete_object()`, which schedules the object and its physics body for removal. Actual list removal happens in `ObjectManager.cleanup_deleted_objects()`.
*   **State Synchronization:** After each physics step, `GameObject.update_from_physics()` copies the position and angle from the `b2Body` back to the `GameObject` instance, ensuring the object's data matches the simulation.
*   **Dragging:** `ObjectManager` handles dragging:
    *   `start_drag`: Creates a `b2MouseJoint` connecting the clicked object's body to an invisible anchor point controlled by the mouse.
    *   `update_drag`: Updates the mouse joint's target position.
    *   `stop_drag`: Destroys the mouse joint. Optionally applies an impulse (`apply_impulse_to_object`) based on mouse velocity for a "throw" effect.

## Portals (`PortalManager`, `Portal`)

*   **Structure:** A `Portal` instance represents one end. `PortalManager` stores them in `portal_pairs` (dictionary mapping `pair_id` to `[portalA, portalB]`). Each `Portal` instance holds a reference to its `linked_portal`.
*   **Physics:** Each `Portal` has a static `b2Body` with a sensor fixture (`PhysicsManager.add_portal`).
*   **Creation:** `PortalManager` handles the drag-create process initiated by `InputManager`:
    *   `start_portal_creation`: Records starting position.
    *   `finish_portal_creation`: Records end position, creates two `Portal` instances, links them, requests physics bodies, and stores the pair.
    *   A preview line is drawn by the `Renderer` during creation.
*   **Teleportation Logic:**
    1.  **Detection:** `PortalContactListener` detects an object entering a portal sensor (`BeginContact`).
    2.  **Queueing:** `PortalManager.queue_teleportation()` checks cooldowns and other conditions, then adds `(object, entry_portal)` to `teleport_queue`.
    3.  **Processing:** *After* the physics step, `PortalManager.process_teleportation_queue()` iterates the queue:
        *   Calculates the exit state using `entry_portal.get_exit_transform()`. This involves rotating the object's relative position and velocity based on the angle difference between the exit and entry portals (+180 degrees).
        *   Directly sets the object's `b2Body` transform (position, angle) and velocities using `body.transform = ...`, `body.linearVelocity = ...`.
        *   Applies a small offset to prevent immediate re-entry.
        *   Starts the cooldown on *both* portals in the pair via `exit_portal.start_cooldown()`.
        *   Updates the object's `GameObject` state and `last_exit_pos` tracking.
*   **Cooldown:** Each `Portal` tracks `cooldown_end_times` per object ID. `start_cooldown` sets the timer on both linked portals. `can_teleport` checks this timer before queueing.

## Rendering (`Renderer`)

*   **Goal:** Draw the current game state each frame.
*   **Process:** Called by `Game.render()`, receives `game_state` dictionary.
*   **Layers (Order):**
    1.  Fill Background (`COLOR_BACKGROUND`)
    2.  Draw Grid (`_draw_grid`)
    3.  Draw Portals (Iterates `game_state['portals']`, calls `portal.draw()`)
    4.  Draw Portal Creation Preview Line (if active)
    5.  Draw Objects (Iterates `game_state['objects']`, calls `obj.draw()`)
    6.  Draw UI (Iterates `game_state['ui_elements']`, calls `element.draw()`) & HUD (`_draw_hud`)
    7.  Draw Debug Info (if `debug_mode`, calls `_draw_physics_debug`, `_draw_debug_info`)
    8.  `pygame.display.flip()`
*   **Drawing Primitives:** Uses methods like `draw_circle`, `draw_polygon`, `draw_portal` which handle coordinate conversion and drawing details (e.g., orientation lines on circles).
*   **Delegation:** Objects, Portals, and UI Elements implement their own `draw(surface, renderer)` methods, allowing the `Renderer` to simply call these without needing to know the specific type.
*   **Debug Drawing:** `_draw_physics_debug` iterates through the `b2World`'s bodies and fixtures, converting their shapes to Pygame coordinates and drawing wireframes. Uses `utils.is_sensor` to color sensors differently.

## Input (`InputManager`)

*   **Event Loop:** Processes `pygame.event.get()` each frame.
*   **Priority:** Checks for Quit events first. Then delegates events to `UIManager.handle_event()`. If the UI doesn't consume the event, game world interactions are processed.
*   **Mapping:** Translates key presses (`K_c`, `K_b`, `K_g`, `K_d`) and mouse actions (clicks, drags) into calls to the appropriate manager methods (e.g., `ObjectManager.create_object`, `PortalManager.start_portal_creation`, `PhysicsManager.toggle_gravity`).
*   **State Tracking:** Maintains current mouse position (`mouse_pos`), relative movement (`mouse_rel`), and button state (`mouse_pressed`).

## UI (`UIManager`, `Button`)

*   **Elements:** `UIManager` holds a list of UI elements (currently only `Button`).
*   **Button:** A simple clickable element with 'normal', 'hover', 'pressed' states, visual feedback, and a `callback` function executed on click. Handles its own events via `Button.handle_event()`.
*   **Event Handling:** `UIManager.handle_event` iterates elements *in reverse* (topmost first) and passes the event. If an element handles it, processing stops for that event. This ensures UI clicks don't accidentally interact with the game world underneath.
*   **Rendering:** `UIManager.get_elements()` provides the list to the `Renderer`, which calls each element's `draw()` method.
---

**File: `docs/Configuration.md`**

# Configuration (`settings.py`)

The `settings.py` file is the central place for configuring the appearance, physics, and behavior of the Portals2D sandbox.

## Key Settings

### Screen & Display
*   `WIDTH`, `HEIGHT`: Dimensions of the game window in pixels.
*   `FPS`: Target frames per second. Affects smoothness and the physics time step.

### Physics Engine
*   `PPM`: **Pixels Per Meter**. This is a critical scaling factor. It defines how many pixels represent one meter in the Box2D physics world. Adjusting this will change the perceived size and speed of objects relative to gravity and forces. A common range is 20-50.
*   `TIME_STEP`: Calculated as `1.0 / FPS`. The fixed time duration for each physics simulation step.
*   `VELOCITY_ITERATIONS`, `POSITION_ITERATIONS`: Solver iterations for Box2D. Higher values increase accuracy (reducing jitter or tunneling) but use more CPU. 8 and 3 are generally good defaults.
*   `GRAVITY`: Tuple `(x, y)` defining the global gravity vector in m/s². `(0, -9.8)` simulates Earth-like gravity pulling downwards. `(0, 0)` disables gravity.

### Colors
A set of `pygame.Color` objects defining the palette:
*   `COLOR_BACKGROUND`, `COLOR_TEXT`, `COLOR_DEBUG`, `COLOR_GRID`
*   `COLOR_CIRCLE`, `COLOR_SQUARE` (Object colors)
*   `PORTAL_COLORS` (List of colors used cyclically for portal pairs)
*   `COLOR_UI_ACCENT`, `COLOR_BUTTON_NORMAL`, `COLOR_BUTTON_HOVER`, `COLOR_BUTTON_PRESSED` (UI colors)
*   `COLOR_PORTAL_PREVIEW` (Color of the line when placing portals)

### Fonts
*   `DEFAULT_FONT_NAME`: Filename of the preferred font (e.g., 'Roboto-Regular.ttf'). The application looks for this in `assets/fonts/`. If not found, it falls back to system defaults.
*   `UI_FONT_SIZE`, `HUD_FONT_SIZE`: Font sizes for UI elements and the heads-up display.

### Object Defaults (in Meters)
*   `DEFAULT_CIRCLE_RADIUS`: Initial radius for spawned circles.
*   `DEFAULT_BOX_SIZE`: Initial `(width, height)` for spawned boxes.

### Portal Defaults (in Meters)
*   `DEFAULT_PORTAL_HEIGHT`, `DEFAULT_PORTAL_WIDTH`: Dimensions of the portal sensor shapes.
*   `PORTAL_COOLDOWN`: Time in seconds an object must wait before using the same portal pair again after teleporting.

### User Data Identifiers
*   `USER_DATA_OBJECT`, `USER_DATA_PORTAL`, `USER_DATA_WALL`: String constants stored in Box2D body `userData` to identify body types during interactions (like collision checks).

## Coordinate Conversion Utilities

The file also defines essential functions for converting between Pygame's pixel coordinates (Y-down origin top-left) and Box2D's meter coordinates (Y-up origin bottom-left, assuming standard Pygame setup):

*   `to_pygame(coords)`: Converts Box2D meters `(x, y)` to Pygame pixels `(px, py)`.
*   `to_box2d(coords)`: Converts Pygame pixels `(px, py)` to Box2D meters `(x, y)`.
*   `scalar_to_pygame(scalar)`: Converts a scalar distance/size in meters to pixels.
*   `scalar_to_box2d(scalar)`: Converts a scalar distance/size in pixels to meters.

---
