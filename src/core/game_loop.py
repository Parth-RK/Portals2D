import pygame
import time
from src.core.input_manager import InputManager
from src.core.object_manager import ObjectManager
from src.physics.physics_engine import PhysicsEngine
from src.rendering.renderer import Renderer
from src.ui.ui_manager import UIManager
from src.utils.logger import Logger

class GameLoop:
    def __init__(self):
        self.logger = Logger()
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("2D Portals Game")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize core components
        self.input_manager = InputManager()
        self.object_manager = ObjectManager()
        self.physics_engine = PhysicsEngine(self.object_manager)
        self.renderer = Renderer(self.screen, self.object_manager)
        self.ui_manager = UIManager(self.screen)
        
        # Fixed time step for physics (60 updates per second)
        self.fixed_time_step = 1/60
        self.accumulated_time = 0
        
        self.logger.info("Game loop initialized")
        
    def process_input(self):
        """Process user input."""
        # Process pygame events once and distribute to both managers
        events = pygame.event.get()
        
        # Handle UI events first (they might consume events)
        for event in events:
            if self.ui_manager.handle_mouse_event(event):
                # Event was consumed by UI, don't process further
                continue
                
        # Process remaining events through input manager
        commands = self.input_manager.process_events(events)
        
        for cmd in commands:
            if cmd == "QUIT":
                self.running = False
            elif cmd == "TOGGLE_GRAVITY":
                self.physics_engine.toggle_gravity()
            elif cmd.startswith("CREATE_OBJECT"):
                obj_type, pos_x, pos_y = cmd.split(":")[1:]
                self.object_manager.create_object(obj_type, float(pos_x), float(pos_y))
            elif cmd.startswith("CREATE_PORTAL"):
                color, portal_id, pos_x, pos_y, angle = cmd.split(":")[1:]
                self.object_manager.create_portal(
                    color, portal_id, float(pos_x), float(pos_y), float(angle))
            elif cmd.startswith("TRY_GRAB_OBJECT"):
                pos_x, pos_y = cmd.split(":")[1:]
                obj = self.object_manager.get_object_at_position(float(pos_x), float(pos_y))
                if obj:
                    # Check if it's a regular game object or a portal
                    if hasattr(obj, 'obj_type'):  # It's a regular game object
                        self.input_manager.set_dragged_object(obj.id)
                        # Temporarily make object kinematic while dragged
                        self.physics_engine.set_object_kinematic(obj.id, True)
                    else:  # It's a portal, which can also be dragged
                        self.input_manager.set_dragged_object(obj.id)
            elif cmd.startswith("DRAG_OBJECT"):
                obj_id, pos_x, pos_y = cmd.split(":")[1:]
                self.object_manager.move_object_to(obj_id, float(pos_x), float(pos_y))
            elif cmd.startswith("THROW_OBJECT"):
                obj_id, vel_x, vel_y = cmd.split(":")[1:]
                # Only apply velocity to regular game objects, not portals
                for obj in self.object_manager.get_objects():
                    if obj.id == obj_id:
                        self.physics_engine.set_object_kinematic(obj_id, False)
                        self.object_manager.set_object_velocity(obj_id, float(vel_x), float(vel_y))
                        break
            elif cmd.startswith("TRY_OPEN_CONTEXT_MENU"):
                pos_x, pos_y = cmd.split(":")[1:]
                obj = self.object_manager.get_object_at_position(float(pos_x), float(pos_y))
                if obj:
                    self.ui_manager.open_context_menu(obj, float(pos_x), float(pos_y))
                    self.input_manager.set_context_menu_open(True, obj.id)
            elif cmd.startswith("CONTEXT_MENU_SELECT"):
                pos_x, pos_y = cmd.split(":")[1:]
                action = self.ui_manager.handle_context_menu_click(float(pos_x), float(pos_y))
                if action:
                    if action.startswith("RESIZE"):
                        _, obj_id, scale = action.split(":")
                        self.object_manager.resize_object(obj_id, float(scale))
                    elif action.startswith("ROTATE"):
                        _, obj_id, angle = action.split(":")
                        self.object_manager.rotate_object(obj_id, float(angle))
            elif cmd == "CLOSE_CONTEXT_MENU":
                self.ui_manager.close_context_menu()
                self.input_manager.set_context_menu_open(False)
                
    def update(self, dt):
        """Update game state with fixed time step."""
        self.accumulated_time += dt
        
        # Run physics updates at fixed intervals
        while self.accumulated_time >= self.fixed_time_step:
            self.physics_engine.update(self.fixed_time_step)
            self.accumulated_time -= self.fixed_time_step
        
        # Update other game components
        self.object_manager.update(dt)
        self.ui_manager.update(dt)
        
    def render(self):
        """Render the current game state."""
        self.renderer.clear()
        self.renderer.draw_objects()
        # Pass both object_manager and physics_engine to the UI manager
        self.ui_manager.draw(self.object_manager, self.physics_engine, self.clock)
        pygame.display.flip()
        
    def run(self):
        """Main game loop."""
        last_time = time.time()
        
        while self.running:
            # Calculate delta time
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            # Main loop steps
            self.process_input()
            self.update(dt)
            self.render()
            
            # Cap frame rate
            self.clock.tick(60)
