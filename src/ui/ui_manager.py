import pygame
from src.utils.logger import Logger

class UIManager:
    def __init__(self, screen):
        self.logger = Logger()
        self.screen = screen
        self.width, self.height = screen.get_size()
        
        # Initialize font
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 20)
        
        # Help menu state
        self.show_help = False
        self.help_text = [
            "Controls:",
            "ESC - Quit game",
            "G - Toggle gravity",
            "B - Create box at cursor",
            "C - Create circle at cursor",
            "P - Create portals (press twice for a pair)",
            "Left click - Grab and drag objects",
            "Right click - Open object properties menu"
        ]
        
        # Context menu
        self.context_menu_open = False
        self.context_menu_object = None
        self.context_menu_pos = (0, 0)
        self.context_menu_items = []
        
        # Help icon
        self.help_icon_rect = pygame.Rect(self.width - 40, 10, 30, 30)  # Positioned at the top-right corner
        
        # Button container
        self.buttons = {}
        
        self.logger.info("UI Manager initialized")
        
    def update(self, dt):
        """Update UI elements."""
        pass
        
    def draw(self, object_manager, physics_engine, clock):
        """Draw UI elements with access to object manager and physics engine."""
        # Draw FPS, object count, portal count, and gravity state
        self.draw_debug_info(object_manager, physics_engine, clock)
        
        # Draw help icon
        self.draw_help_icon()
        
        # Draw help menu if visible
        if self.show_help:
            self.draw_help_menu()
            
        # Draw context menu if open
        if self.context_menu_open:
            self.draw_context_menu()
        
    def draw_debug_info(self, object_manager, physics_engine, clock):
        """Draw debug information."""
        fps = int(clock.get_fps())  # Use the clock to get FPS
        object_count = len(object_manager.get_objects())
        portal_count = len(object_manager.get_portals())
        gravity_state = "ON" if physics_engine.gravity_on else "OFF"
        
        # Render FPS, object count, portal count, and gravity state
        debug_text = [
            f"FPS: {fps}",
            f"Objects: {object_count}",
            f"Portals: {portal_count}",
            f"Gravity: {gravity_state}"
        ]
        
        y_offset = 10
        for line in debug_text:
            text_surface = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25
        
    def draw_help_icon(self):
        """Draw the help icon."""
        pygame.draw.rect(self.screen, (200, 200, 200), self.help_icon_rect)  # Draw the icon background
        text_surface = self.font.render("?", True, (0, 0, 0))  # Draw the "?" symbol
        text_rect = text_surface.get_rect(center=self.help_icon_rect.center)
        self.screen.blit(text_surface, text_rect)
        
    def draw_help_menu(self):
        """Draw the help menu."""
        menu_width = 330
        menu_height = len(self.help_text) * 25 + 20
        menu_x = (self.width - menu_width) // 2
        menu_y = (self.height - menu_height) // 2
        
        # Draw menu background
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(self.screen, (50, 50, 50), menu_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), menu_rect, 2)
        
        # Draw help text
        y_offset = menu_y + 10
        for line in self.help_text:
            text_surface = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (menu_x + 10, y_offset))
            y_offset += 25
            
    def handle_mouse_event(self, event):
        """Handle mouse events for UI elements."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.help_icon_rect.collidepoint(event.pos):
                # Toggle help menu when the help icon is clicked
                self.show_help = not self.show_help
                self.logger.info(f"Help menu {'opened' if self.show_help else 'closed'}")
                return True
            elif self.show_help:
                # Close help menu if clicked elsewhere
                self.show_help = False
                return True
            
            # Check for context menu clicks
            if self.context_menu_open:
                # Handle context menu item selection
                menu_width = 150
                item_height = 30
                menu_height = len(self.context_menu_items) * item_height + 10
                
                menu_x = min(self.context_menu_pos[0], self.width - menu_width - 10)
                menu_y = min(self.context_menu_pos[1], self.height - menu_height - 10)
                
                menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
                
                if not menu_rect.collidepoint(event.pos):
                    # Close menu if clicked outside
                    self.close_context_menu()
                    return True
                
                # Check if clicked on a menu item
                for i, item in enumerate(self.context_menu_items):
                    item_rect = pygame.Rect(
                        menu_x + 5,
                        menu_y + 5 + i * item_height,
                        menu_width - 10,
                        item_height - 5
                    )
                    if item_rect.collidepoint(event.pos):
                        self.logger.info(f"Selected menu item: {item['label']}")
                        # Return the action associated with this menu item
                        return item['action']
                return True
                
        return False
        
    def open_context_menu(self, obj, x, y):
        """Open a context menu for manipulating an object."""
        self.context_menu_open = True
        self.context_menu_object = obj
        self.context_menu_pos = (x, y)
        
        # Create menu items based on object type
        if hasattr(obj, 'obj_type'):  # It's a GameObject
            self.context_menu_items = [
                {"label": "Increase Size", "action": f"RESIZE:{obj.id}:1.2"},
                {"label": "Decrease Size", "action": f"RESIZE:{obj.id}:0.8"},
                {"label": "Rotate 45° CW", "action": f"ROTATE:{obj.id}:45"},
                {"label": "Rotate 45° CCW", "action": f"ROTATE:{obj.id}:-45"}
            ]
        else:  # It's a Portal
            self.context_menu_items = [
                {"label": "Increase Size", "action": f"RESIZE:{obj.id}:1.2"},
                {"label": "Decrease Size", "action": f"RESIZE:{obj.id}:0.8"},
                {"label": "Rotate 45° CW", "action": f"ROTATE:{obj.id}:45"},
                {"label": "Rotate 45° CCW", "action": f"ROTATE:{obj.id}:-45"},
                {"label": "Rotate 90° CW", "action": f"ROTATE:{obj.id}:90"},
                {"label": "Rotate 90° CCW", "action": f"ROTATE:{obj.id}:-90"}
            ]
        
        self.logger.info(f"Opened context menu for object {obj.id}")
        
    def close_context_menu(self):
        """Close the context menu."""
        self.context_menu_open = False
        self.context_menu_object = None
        self.context_menu_items = []
        self.logger.info("Closed context menu")
        
    def draw_context_menu(self):
        """Draw the context menu."""
        if not self.context_menu_open:
            return
            
        # Menu dimensions
        menu_width = 150
        item_height = 30
        menu_height = len(self.context_menu_items) * item_height + 10
        
        # Menu position (ensure it stays on screen)
        menu_x = min(self.context_menu_pos[0], self.width - menu_width - 10)
        menu_y = min(self.context_menu_pos[1], self.height - menu_height - 10)
        
        # Draw menu background
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(self.screen, (70, 70, 70), menu_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), menu_rect, 2)
        
        # Draw menu items
        for i, item in enumerate(self.context_menu_items):
            item_rect = pygame.Rect(
                menu_x + 5,
                menu_y + 5 + i * item_height,
                menu_width - 10,
                item_height - 5
            )
            
            # Check if mouse is hovering over item
            mouse_pos = pygame.mouse.get_pos()
            hover = item_rect.collidepoint(mouse_pos)
            
            # Draw item background
            if hover:
                pygame.draw.rect(self.screen, (100, 100, 120), item_rect)
            
            # Draw item text
            text_surface = self.font.render(item["label"], True, (255, 255, 255))
            self.screen.blit(text_surface, (item_rect.x + 5, item_rect.y + 5))
            
    def handle_context_menu_click(self, x, y):
        """Handle clicks on the context menu."""
        if not self.context_menu_open:
            return None
            
        # Check if the click is within the menu
        menu_width = 150
        item_height = 30
        menu_height = len(self.context_menu_items) * item_height + 10
        
        menu_x = min(self.context_menu_pos[0], self.width - menu_width - 10)
        menu_y = min(self.context_menu_pos[1], self.height - menu_height - 10)
        
        # Check each menu item
        for i, item in enumerate(self.context_menu_items):
            item_rect = pygame.Rect(
                menu_x + 5,
                menu_y + 5 + i * item_height,
                menu_width - 10,
                item_height - 5
            )
            if item_rect.collidepoint(x, y):
                self.close_context_menu()
                return item["action"]
                
        return None
