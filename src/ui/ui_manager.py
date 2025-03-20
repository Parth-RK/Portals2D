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
        self.title_font = pygame.font.SysFont('Arial', 22, bold=True)
        
        # Define themes with improved colors
        self.themes = {
            "dark": {
                "bg_color": (30, 30, 35),
                "text_color": (230, 230, 230),
                "ui_element_color": (60, 60, 70),
                "ui_highlight_color": (80, 80, 120),
                "ui_border_color": (100, 100, 130),
                "menu_icon_color": (200, 200, 210),
                "menu_text_color": (230, 230, 230),
                "accent_color": (100, 140, 230)
            },
            "light": {
                "bg_color": (245, 245, 248),
                "text_color": (40, 40, 45),
                "ui_element_color": (220, 220, 225),
                "ui_highlight_color": (190, 190, 210),
                "ui_border_color": (180, 180, 190),
                "menu_icon_color": (80, 80, 90),
                "menu_text_color": (40, 40, 45),
                "accent_color": (70, 110, 200)
            },
            "dusk": {
                "bg_color": (50, 55, 80),
                "text_color": (220, 225, 255),
                "ui_element_color": (80, 85, 120),
                "ui_highlight_color": (100, 105, 160),
                "ui_border_color": (120, 125, 180),
                "menu_icon_color": (200, 205, 255),
                "menu_text_color": (220, 225, 255),
                "accent_color": (130, 160, 255)
            },
            "cream": {
                "bg_color": (250, 245, 230),
                "text_color": (60, 50, 40),
                "ui_element_color": (240, 230, 210),
                "ui_highlight_color": (225, 215, 190),
                "ui_border_color": (200, 190, 165),
                "menu_icon_color": (120, 110, 90),
                "menu_text_color": (60, 50, 40),
                "accent_color": (180, 130, 90)
            }
        }
        
        # Current theme
        self.current_theme = "dark"
        
        # Menu state
        self.show_menu = False
        self.show_help = False
        self.show_theme_selector = False
        
        # Menu items
        self.menu_items = [
            {"label": "Themes", "action": "SHOW_THEME_SELECTOR"},
            {"label": "Help", "action": "SHOW_HELP"}
        ]
        
        # Help text
        self.help_text = [
            "Controls:",
            "ESC - Quit game",
            "G - Toggle gravity",
            "B - Create box at cursor",
            "C - Create circle at cursor",
            "P - Create portals (press twice for a pair)",
            "T - Toggle theme",
            "Left click - Grab and drag objects",
            "Right click - Open object properties menu"
        ]
        
        # Context menu
        self.context_menu_open = False
        self.context_menu_object = None
        self.context_menu_pos = (0, 0)
        self.context_menu_items = []
        
        # Menu icon (three dashes)
        self.menu_icon_rect = pygame.Rect(self.width - 40, 10, 30, 30)
        
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
        
        # Draw menu icon (three dashes)
        self.draw_menu_icon()
        
        # Draw main menu if visible
        if self.show_menu:
            self.draw_main_menu()
            
        # Draw help menu if visible
        if self.show_help:
            self.draw_help_menu()
            
        # Draw theme selector if visible
        if self.show_theme_selector:
            self.draw_theme_selector()
            
        # Draw context menu if open
        if self.context_menu_open:
            self.draw_context_menu()
        
    def draw_debug_info(self, object_manager, physics_engine, clock):
        """Draw debug information."""
        fps = int(clock.get_fps())
        object_count = len(object_manager.get_objects())
        portal_count = len(object_manager.get_portals())
        gravity_state = "ON" if physics_engine.gravity_on else "OFF"
        
        # Render FPS, object count, portal count, and gravity state
        debug_text = [
            f"FPS: {fps}",
            f"Objects: {object_count}",
            f"Portals: {portal_count}",
            f"Gravity: {gravity_state}",
            f"Theme: {self.current_theme.capitalize()}"
        ]
        
        theme = self.themes[self.current_theme]
        y_offset = 10
        for line in debug_text:
            text_surface = self.font.render(line, True, theme["text_color"])
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25
        
    def draw_menu_icon(self):
        """Draw the menu icon (three dashes)."""
        theme = self.themes[self.current_theme]
        pygame.draw.rect(self.screen, theme["ui_element_color"], self.menu_icon_rect, border_radius=4)
        
        # Draw three dashes
        dash_width = 15
        dash_height = 2
        dash_spacing = 5
        
        total_height = (dash_height * 3) + (dash_spacing * 2)
        start_y = self.menu_icon_rect.centery - (total_height // 2)
        
        for i in range(3):
            dash_y = start_y + (i * (dash_height + dash_spacing))
            dash_rect = pygame.Rect(
                self.menu_icon_rect.centerx - (dash_width // 2),
                dash_y,
                dash_width,
                dash_height
            )
            pygame.draw.rect(self.screen, theme["menu_icon_color"], dash_rect)
        
        # Draw border
        pygame.draw.rect(self.screen, theme["ui_border_color"], self.menu_icon_rect, 1, border_radius=4)
        
    def draw_main_menu(self):
        """Draw the main menu."""
        theme = self.themes[self.current_theme]
        menu_width = 150
        item_height = 35
        menu_height = len(self.menu_items) * item_height + 10
        
        # Position below the menu icon
        menu_x = self.menu_icon_rect.x - menu_width + self.menu_icon_rect.width
        menu_y = self.menu_icon_rect.y + self.menu_icon_rect.height + 5
        
        # Ensure menu stays on screen
        if menu_y + menu_height > self.height:
            menu_y = self.height - menu_height - 5
        
        # Draw menu background with rounded corners
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(self.screen, theme["ui_element_color"], menu_rect, border_radius=6)
        pygame.draw.rect(self.screen, theme["ui_border_color"], menu_rect, 1, border_radius=6)
        
        # Draw menu items
        mouse_pos = pygame.mouse.get_pos()
        for i, item in enumerate(self.menu_items):
            item_rect = pygame.Rect(
                menu_x + 5,
                menu_y + 5 + i * item_height,
                menu_width - 10,
                item_height - 5
            )
            
            # Highlight on hover
            hover = item_rect.collidepoint(mouse_pos)
            if hover:
                pygame.draw.rect(self.screen, theme["ui_highlight_color"], item_rect, border_radius=4)
            
            # Draw menu text
            text_surface = self.font.render(item["label"], True, theme["menu_text_color"])
            text_rect = text_surface.get_rect(midleft=(item_rect.x + 10, item_rect.centery))
            self.screen.blit(text_surface, text_rect)
        
    def draw_help_menu(self):
        """Draw the help menu."""
        theme = self.themes[self.current_theme]
        menu_width = 350
        menu_height = len(self.help_text) * 25 + 45  # Extra space for title
        menu_x = (self.width - menu_width) // 2
        menu_y = (self.height - menu_height) // 2
        
        # Draw menu background with rounded corners
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(self.screen, theme["ui_element_color"], menu_rect, border_radius=8)
        pygame.draw.rect(self.screen, theme["ui_border_color"], menu_rect, 2, border_radius=8)
        
        # Draw title
        title_surface = self.title_font.render("Game Controls", True, theme["accent_color"])
        title_rect = title_surface.get_rect(midtop=(menu_x + menu_width // 2, menu_y + 10))
        self.screen.blit(title_surface, title_rect)
        
        # Draw help text
        y_offset = menu_y + 40  # Start below title
        for line in self.help_text:
            text_surface = self.font.render(line, True, theme["menu_text_color"])
            self.screen.blit(text_surface, (menu_x + 15, y_offset))
            y_offset += 25
            
    def draw_theme_selector(self):
        """Draw the theme selection menu."""
        theme = self.themes[self.current_theme]
        theme_options = list(self.themes.keys())
        
        menu_width = 180
        item_height = 35
        title_height = 30
        menu_height = len(theme_options) * item_height + title_height + 15
        
        # Center on screen
        menu_x = (self.width - menu_width) // 2
        menu_y = (self.height - menu_height) // 2
        
        # Draw menu background with rounded corners
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(self.screen, theme["ui_element_color"], menu_rect, border_radius=8)
        pygame.draw.rect(self.screen, theme["ui_border_color"], menu_rect, 2, border_radius=8)
        
        # Draw title
        title_surface = self.title_font.render("Select Theme", True, theme["accent_color"])
        title_rect = title_surface.get_rect(midtop=(menu_x + menu_width // 2, menu_y + 10))
        self.screen.blit(title_surface, title_rect)
        
        # Draw theme options
        mouse_pos = pygame.mouse.get_pos()
        for i, option in enumerate(theme_options):
            item_rect = pygame.Rect(
                menu_x + 15,
                menu_y + title_height + 10 + i * item_height,
                menu_width - 30,
                item_height - 5
            )
            
            # Highlight current theme and hover
            is_current = option == self.current_theme
            hover = item_rect.collidepoint(mouse_pos)
            
            if is_current:
                pygame.draw.rect(self.screen, theme["accent_color"], item_rect, border_radius=4)
                text_color = theme["ui_element_color"]  # Contrast with accent color
            elif hover:
                pygame.draw.rect(self.screen, theme["ui_highlight_color"], item_rect, border_radius=4)
                text_color = theme["menu_text_color"]
            else:
                text_color = theme["menu_text_color"]
            
            # Draw theme name
            text_surface = self.font.render(option.capitalize(), True, text_color)
            text_rect = text_surface.get_rect(midleft=(item_rect.x + 10, item_rect.centery))
            self.screen.blit(text_surface, text_rect)
            
    def handle_mouse_event(self, event):
        """Handle mouse events for UI elements."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.menu_icon_rect.collidepoint(event.pos):
                # Toggle main menu when icon is clicked
                self.show_menu = not self.show_menu
                # Close other menus
                self.show_help = False
                self.show_theme_selector = False
                self.logger.info(f"Main menu {'opened' if self.show_menu else 'closed'}")
                return True
                
            elif self.show_menu:
                # Check if clicked on a menu item
                menu_width = 150
                item_height = 35
                
                # Calculate menu position
                menu_x = self.menu_icon_rect.x - menu_width + self.menu_icon_rect.width
                menu_y = self.menu_icon_rect.y + self.menu_icon_rect.height + 5
                
                # Ensure menu stays on screen
                if menu_y + (len(self.menu_items) * item_height + 10) > self.height:
                    menu_y = self.height - (len(self.menu_items) * item_height + 10) - 5
                
                # Check each menu item
                for i, item in enumerate(self.menu_items):
                    item_rect = pygame.Rect(
                        menu_x + 5,
                        menu_y + 5 + i * item_height,
                        menu_width - 10,
                        item_height - 5
                    )
                    if item_rect.collidepoint(event.pos):
                        # Handle menu item action
                        if item["action"] == "SHOW_HELP":
                            self.show_help = True
                            self.show_theme_selector = False
                        elif item["action"] == "SHOW_THEME_SELECTOR":
                            self.show_theme_selector = True
                            self.show_help = False
                        
                        self.show_menu = False
                        self.logger.info(f"Selected menu item: {item['label']}")
                        return True
                
                # Close menu if clicked outside
                self.show_menu = False
                return True
                
            elif self.show_help:
                # Close help menu if clicked elsewhere
                self.show_help = False
                return True
                
            elif self.show_theme_selector:
                # Check if clicked on a theme option
                theme_options = list(self.themes.keys())
                menu_width = 180
                item_height = 35
                title_height = 30
                menu_height = len(theme_options) * item_height + title_height + 15
                
                # Center on screen
                menu_x = (self.width - menu_width) // 2
                menu_y = (self.height - menu_height) // 2
                
                # Check each theme option
                for i, option in enumerate(theme_options):
                    item_rect = pygame.Rect(
                        menu_x + 15,
                        menu_y + title_height + 10 + i * item_height,
                        menu_width - 30,
                        item_height - 5
                    )
                    if item_rect.collidepoint(event.pos):
                        old_theme = self.current_theme
                        self.current_theme = option
                        self.logger.info(f"Changed theme to {option}")
                        self.show_theme_selector = False
                        # Return a command to update the renderer background
                        if old_theme != option:
                            return "THEME_CHANGED"
                        return True
                
                # Close theme selector if clicked outside
                self.show_theme_selector = False
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
            
        theme = self.themes[self.current_theme]
        # Menu dimensions
        menu_width = 170
        item_height = 30
        menu_height = len(self.context_menu_items) * item_height + 10
        
        # Menu position (ensure it stays on screen)
        menu_x = min(self.context_menu_pos[0], self.width - menu_width - 10)
        menu_y = min(self.context_menu_pos[1], self.height - menu_height - 10)
        
        # Draw menu background with rounded corners
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(self.screen, theme["ui_element_color"], menu_rect, border_radius=6)
        pygame.draw.rect(self.screen, theme["ui_border_color"], menu_rect, 1, border_radius=6)
        
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
                pygame.draw.rect(self.screen, theme["ui_highlight_color"], item_rect, border_radius=4)
            
            # Draw item text
            text_surface = self.font.render(item["label"], True, theme["menu_text_color"])
            text_rect = text_surface.get_rect(midleft=(item_rect.x + 10, item_rect.centery))
            self.screen.blit(text_surface, text_rect)
            
    def handle_context_menu_click(self, x, y):
        """Handle clicks on the context menu."""
        if not self.context_menu_open:
            return None
            
        # Check if the click is within the menu
        menu_width = 170
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
        
    def get_background_color(self):
        """Get the current theme's background color."""
        return self.themes[self.current_theme]["bg_color"]
    
    def toggle_theme(self):
        """Cycle to the next theme."""
        theme_options = list(self.themes.keys())
        current_index = theme_options.index(self.current_theme)
        next_index = (current_index + 1) % len(theme_options)
        self.current_theme = theme_options[next_index]
        self.logger.info(f"Changed theme to {self.current_theme}")
        return self.current_theme
