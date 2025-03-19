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
        commands = self.input_manager.process_events()
        for cmd in commands:
            if cmd == "QUIT":
                self.running = False
            elif cmd == "TOGGLE_GRAVITY":
                self.physics_engine.toggle_gravity()
            elif cmd.startswith("CREATE_OBJECT"):
                obj_type, pos_x, pos_y = cmd.split(":")[1:]
                self.object_manager.create_object(obj_type, float(pos_x), float(pos_y))
            elif cmd.startswith("CREATE_PORTAL"):
                portal_id, pos_x, pos_y, angle = cmd.split(":")[1:]
                self.object_manager.create_portal(
                    portal_id, float(pos_x), float(pos_y), float(angle))
                
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
        self.ui_manager.draw()
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
