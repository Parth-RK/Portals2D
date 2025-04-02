import pygame
import os
import sys
from settings import (WIDTH, HEIGHT, FPS, PPM, COLOR_BACKGROUND, DEFAULT_FONT_NAME,
                      UI_FONT_SIZE, HUD_FONT_SIZE)
from input import InputManager
from physics import PhysicsManager
from objects import ObjectManager
from portals import PortalManager
from renderer import Renderer
from ui import UIManager

class Game:
    """Main game class orchestrating initialization, game loop, and managers."""
    def __init__(self):
        self.screen = None # Pygame screen
        self.clock = None
        self.running = False
        self.debug_mode = False
        self.assets = {} # Game assets (fonts, sounds)

        self.input_manager = None
        self.physics_manager = None
        self.object_manager = None
        self.portal_manager = None
        self.ui_manager = None
        self.renderer = None

        if not self.init_pygame(): return
        if not self._load_assets(): return
        if not self._init_managers(): return
        self._setup_scene()
        self._create_ui()

        self.running = True


    def init_pygame(self):
        """Initializes Pygame modules, screen, and clock."""
        try:
            pygame.init()
            try:
                pygame.mixer.init()
                print("Pygame mixer initialized.")
            except pygame.error as e:
                print(f"Warning: Pygame mixer could not be initialized - {e}")

            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Portals2D - Minimalist Physics Sandbox")
            self.clock = pygame.time.Clock()
            print("Pygame initialized successfully.")
            return True
        except pygame.error as e:
            print(f"FATAL: Pygame initialization failed: {e}")
            return False
        except Exception as e:
            print(f"FATAL: An unexpected error occurred during Pygame initialization: {e}")
            return False


    def _load_assets(self):
        """Loads fonts and potentially sounds, storing them in self.assets."""
        print("Loading assets...")
        font_dir = os.path.join('assets', 'fonts')
        font_path = os.path.join(font_dir, DEFAULT_FONT_NAME)
        loaded_font = False
        try:
            self.assets['ui_font'] = pygame.font.Font(font_path, UI_FONT_SIZE)
            self.assets['hud_font'] = pygame.font.Font(font_path, HUD_FONT_SIZE)
            self.assets['debug_font'] = pygame.font.Font(font_path, HUD_FONT_SIZE - 2)
            print(f"Loaded font: {font_path}")
            loaded_font = True
        except FileNotFoundError:
            print(f"Warning: Font file not found at '{font_path}'.")
        except pygame.error as e:
             print(f"Warning: Failed to load font '{font_path}' using Pygame: {e}.")
        except Exception as e:
            print(f"Warning: Unexpected error loading font '{font_path}': {e}")

        if not loaded_font:
            print("Using system default font as fallback.")
            try:
                self.assets['ui_font'] = pygame.font.SysFont(None, UI_FONT_SIZE)
                self.assets['hud_font'] = pygame.font.SysFont(None, HUD_FONT_SIZE)
                self.assets['debug_font'] = pygame.font.SysFont("monospace", HUD_FONT_SIZE - 1)
            except Exception as e:
                 print(f"FATAL: Failed to load system default font: {e}")
                 return False

        print("Assets loaded.")
        return True


    def _init_managers(self):
        """Initializes all the game managers in the correct order."""
        print("Initializing managers...")
        try:
            self.object_manager = ObjectManager(None)
            self.portal_manager = PortalManager(None)
            self.physics_manager = PhysicsManager(self.object_manager, self.portal_manager)
            self.object_manager.set_physics_manager(self.physics_manager)
            self.portal_manager.set_physics_manager(self.physics_manager)

            self.ui_manager = UIManager(self.assets)
            self.renderer = Renderer(self.screen, self.assets)
            self.input_manager = InputManager(self)
            print("Managers initialized successfully.")
            return True
        except Exception as e:
            print(f"FATAL: Failed to initialize managers: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _setup_scene(self):
        """Initial setup of the game world (boundaries, initial objects)."""
        print("Setting up scene...")
        try:
            width_m = WIDTH / PPM
            height_m = HEIGHT / PPM
            self.physics_manager.add_boundaries(width_m, height_m)

            self.object_manager.create_object('box', (WIDTH * 0.5, HEIGHT * 0.3))
            self.object_manager.create_object('circle', (WIDTH * 0.6, HEIGHT * 0.5))
            self.object_manager.create_object('circle', (WIDTH * 0.4, HEIGHT * 0.5))
            print("Scene setup complete.")
        except Exception as e:
            print(f"Error during scene setup: {e}")


    def _create_ui(self):
         """Create initial UI elements like buttons."""
         print("Creating UI...")
         try:
             button_width, button_height = 160, 35
             button_margin = 15
             button_x = WIDTH - button_width - button_margin
             button_y = HEIGHT - button_height - button_margin
             self.ui_manager.create_button(
                 (button_x, button_y, button_width, button_height),
                 "Toggle Gravity (G)",
                 self.physics_manager.toggle_gravity,
                 border_radius=4
             )
             print("UI created.")
         except Exception as e:
            print(f"Error during UI creation: {e}")


    def run(self):
        """Main game loop."""
        if not self.running:
             print("Game cannot run, initialization failed.")
             return

        print("Starting game loop...")
        while self.running:
            dt = min(self.clock.tick(FPS) / 1000.0, 0.1)

            try:
                self.input_manager.process_inputs()
            except Exception as e:
                 print(f"Error during input processing: {e}")
                 self.running = False

            if not self.running: break

            try:
                self.update(dt)
            except Exception as e:
                 print(f"Error during game update: {e}")
                 import traceback; traceback.print_exc()
                 self.running = False

            try:
                self.render()
            except Exception as e:
                 print(f"Error during rendering: {e}")
                 import traceback; traceback.print_exc()
                 self.running = False

        print("Game loop finished.")
        self.cleanup()


    def update(self, dt):
        """Update all relevant game components based on delta time."""
        self.physics_manager.update(dt)
        self.portal_manager.update(dt)
        self.object_manager.update(dt)
        self.ui_manager.update(dt)


    def render(self):
        """Gather current game state and pass it to the renderer."""
        if not self.renderer: return

        game_state = {
            'objects': self.object_manager.get_objects(),
            'portals': self.portal_manager.get_all_portals(),
            'ui_elements': self.ui_manager.get_elements(),
            'hud_info': {
                'fps': self.clock.get_fps(),
                'obj_count': self.object_manager.get_count(),
                'portal_count': self.portal_manager.get_portal_count(),
                'gravity_on': self.physics_manager.get_gravity_state(),
            },
            'debug_mode': self.debug_mode,
            'physics_world': self.physics_manager.world if self.debug_mode else None,
            'debug_info': self._get_debug_info() if self.debug_mode else {},
            'portal_preview_line': self.portal_manager.get_creation_preview_line()
        }
        self.renderer.render_all(game_state)


    def _get_debug_info(self):
        """Collects various pieces of information for the debug overlay text."""
        info = {
            "Mouse Pos": self.input_manager.mouse_pos,
            "Mouse Vel": self.input_manager.mouse_rel,
            "Bodies": len(self.physics_manager.world.bodies) if self.physics_manager.world else 'N/A',
            "Joints": len(self.physics_manager.world.joints) if self.physics_manager.world else 'N/A',
            "Contacts": self.physics_manager.world.contactCount if self.physics_manager.world else 'N/A',
            "Dragging": self.object_manager.selected_object.id if self.object_manager.selected_object else "None",
            "Portal Creating": self.portal_manager.creation_state['active'],
            "Teleport Queue": len(self.portal_manager.teleport_queue),
        }
        return info

    def cleanup(self):
        """Perform cleanup operations when the game exits."""
        print("Cleaning up...")
        pygame.mixer.quit()
        pygame.quit()
        print("Cleanup complete. Exiting.")