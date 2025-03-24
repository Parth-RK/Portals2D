import pygame
import math
from src.utils.logger import Logger

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.handle_width = 10
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False
        self.update_handle_position()
        self.last_value = initial_val  # Store last value to detect changes
        self.preview_callback = None  # Callback function for preview updates
        
    def update_handle_position(self):
        """Update the handle position based on the current value."""
        normalized = (self.value - self.min_val) / (self.max_val - self.min_val)
        handle_x = self.rect.x + int(normalized * (self.rect.width - self.handle_width))
        self.handle_rect = pygame.Rect(handle_x, self.rect.y, self.handle_width, self.rect.height)
        
    def draw(self, surface, theme):
        """Draw the slider."""
        # Draw background track
        pygame.draw.rect(surface, theme["ui_border_color"], self.rect, border_radius=3)
        
        # Draw filled portion
        fill_width = self.handle_rect.x - self.rect.x
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(surface, theme["accent_color"], fill_rect, border_radius=3)
        
        # Draw handle
        pygame.draw.rect(surface, theme["ui_highlight_color"], self.handle_rect, border_radius=2)
        pygame.draw.rect(surface, theme["ui_border_color"], self.handle_rect, 1, border_radius=2)
        
        # Draw label and value with better positioning
        font = pygame.font.SysFont('Arial', 16)
        # Display one decimal place for readability
        if self.label == "Angle":
            label_text = font.render(f"{self.label}: {int(self.value)}°", True, theme["text_color"])
        else:
            label_text = font.render(f"{self.label}: {self.value:.1f}", True, theme["text_color"])
        # Position label above the slider instead of potentially overlapping
        label_rect = label_text.get_rect(bottomleft=(self.rect.x, self.rect.y - 5))
        surface.blit(label_text, label_rect)
        
    def handle_event(self, event):
        """Handle mouse events for the slider."""
        old_value = self.value  # Store current value to detect changes
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
                return True
            elif self.rect.collidepoint(event.pos):
                # Allow clicking anywhere on the slider to move the handle
                normalized = (event.pos[0] - self.rect.x) / (self.rect.width - self.handle_width)
                self.value = self.min_val + normalized * (self.max_val - self.min_val)
                self.update_handle_position()
                self.dragging = True
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Update value based on mouse position
            normalized = max(0, min(1, (event.pos[0] - self.rect.x) / (self.rect.width - self.handle_width)))
            self.value = self.min_val + normalized * (self.max_val - self.min_val)
            self.update_handle_position()
            
            # Call the preview callback if value changed and callback exists
            if self.preview_callback and self.value != old_value:
                self.preview_callback(self.value)
                
            return True
        return False
        
    def get_value(self):
        """Get the current value of the slider."""
        return self.value

    def set_preview_callback(self, callback):
        """Set a callback function that will be called when slider value changes."""
        self.preview_callback = callback

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
                "accent_color": (100, 140, 230),
                # Game object colors for dark theme
                "box_color": (200, 200, 220),      # Light gray with blue tint
                "circle_color": (255, 220, 60),    # Bright yellow
                "triangle_color": (0, 200, 200),   # Cyan
                "portal_tint": 1.2                 # Brighten portals slightly
            },
            "light": {
                "bg_color": (245, 245, 248),
                "text_color": (40, 40, 45),
                "ui_element_color": (220, 220, 225),
                "ui_highlight_color": (190, 190, 210),
                "ui_border_color": (180, 180, 190),
                "menu_icon_color": (80, 80, 90),
                "menu_text_color": (40, 40, 45),
                "accent_color": (70, 110, 200),
                # Game object colors for light theme
                "box_color": (80, 90, 120),        # Darker blue-gray
                "circle_color": (220, 160, 20),    # Darker yellow
                "triangle_color": (0, 150, 150),   # Darker cyan
                "portal_tint": 0.9                 # Slightly darken portals
            },
            "dusk": {
                "bg_color": (50, 55, 80),
                "text_color": (220, 225, 255),
                "ui_element_color": (80, 85, 120),
                "ui_highlight_color": (100, 105, 160),
                "ui_border_color": (120, 125, 180),
                "menu_icon_color": (200, 205, 255),
                "menu_text_color": (220, 225, 255),
                "accent_color": (130, 160, 255),
                # Game object colors for dusk theme
                "box_color": (180, 190, 255),      # Light blue with purple tint
                "circle_color": (255, 190, 80),    # Soft orange
                "triangle_color": (100, 220, 220), # Light cyan
                "portal_tint": 1.1                 # Slightly brighten portals
            },
            "cream": {
                "bg_color": (250, 245, 230),
                "text_color": (60, 50, 40),
                "ui_element_color": (240, 230, 210),
                "ui_highlight_color": (225, 215, 190),
                "ui_border_color": (200, 190, 165),
                "menu_icon_color": (120, 110, 90),
                "menu_text_color": (60, 50, 40),
                "accent_color": (180, 130, 90),
                # Game object colors for cream theme
                "box_color": (120, 90, 60),        # Brown
                "circle_color": (180, 120, 10),    # Dark orange-brown
                "triangle_color": (0, 150, 120),   # Teal
                "portal_tint": 0.85                # Darken portals for contrast
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
        
        # Help text - Update to reflect swapped T/Shift+T controls
        self.help_text = [
            "Controls:",
            "ESC - Quit game",
            "G - Toggle gravity",
            "B - Create box at cursor",
            "C - Create circle at cursor",
            "T - Create triangle at cursor",
            "Shift+T - Toggle theme",
            "P - Create portals (press twice for a pair)",
            "Left click - Grab and drag objects",
            "Right click - Open object properties menu"
        ]
        
        # Context menu
        self.context_menu_open = False
        self.context_menu_object = None
        self.context_menu_pos = (0, 0)
        self.context_menu_items = []
        self.context_menu_sliders = []
        
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
        # Handle slider events if context menu is open
        if self.context_menu_open:
            for slider in self.context_menu_sliders:
                if slider.handle_event(event):
                    return True
        
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
                        # Return a command to update the renderer and objects
                        if old_theme != option:
                            return "THEME_CHANGED"
                        return True
                
                # Close theme selector if clicked outside
                self.show_theme_selector = False
                return True
            
            # Check for context menu clicks
            if self.context_menu_open:
                # Handle context menu item selection
                menu_width = 220  # Wider for slider menu
                item_height = 30
                slider_spacing = 60  # Space for each slider
                menu_height = len(self.context_menu_items) * item_height + len(self.context_menu_sliders) * slider_spacing + 20
                
                menu_x = min(self.context_menu_pos[0], self.width - menu_width - 10)
                menu_y = min(self.context_menu_pos[1], self.height - menu_height - 10)
                
                menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
                
                if not menu_rect.collidepoint(event.pos):
                    # Close menu if clicked outside
                    self.close_context_menu()
                    return True
                
                # Calculate y-offset for items
                y_offset = menu_y + 30 + len(self.context_menu_sliders) * slider_spacing
                
                # Check each menu item
                for i, item in enumerate(self.context_menu_items):
                    item_rect = pygame.Rect(
                        menu_x + 10,
                        y_offset + i * item_height,
                        menu_width - 20,
                        item_height - 5
                    )
                    if item_rect.collidepoint(event.pos):
                        # Handle menu item action
                        if item["action"].startswith("APPLY_CHANGES"):
                            # Apply changes from sliders
                            obj_id = item["action"].split(":")[1]
                            
                            # Get values from sliders
                            if len(self.context_menu_sliders) >= 1:
                                size_value = self.context_menu_sliders[0].get_value()
                                angle_value = self.context_menu_sliders[1].get_value()
                                
                                # Close menu
                                self.close_context_menu()
                                
                                # Return combined action
                                return f"RESIZE_AND_ROTATE:{obj_id}:{size_value}:{angle_value}"
                        elif item["action"].startswith("DELETE"):
                            self.close_context_menu()
                            return item["action"]
                        self.close_context_menu()
                        return item["action"]
                return True
                
        return False
        
    def open_context_menu(self, obj, x, y):
        """Open a context menu for manipulating an object."""
        self.context_menu_open = True
        self.context_menu_object = obj
        self.context_menu_pos = (x, y)
        
        # Create menu items and sliders based on object type
        self.context_menu_items = []
        self.context_menu_sliders = []
        
        # Calculate menu dimensions first to ensure proper positioning
        menu_width = 280  # Increased width to prevent overflow
        slider_spacing = 70  # Increase spacing for sliders
        
        if hasattr(obj, 'obj_type'):  # It's a GameObject
            # Add size slider
            if obj.obj_type == "CIRCLE":
                current_size = obj.radius
                min_size = current_size * 0.5
                max_size = current_size * 2.0
                size_slider = Slider(x + 20, y + 50, menu_width - 40, 20, min_size, max_size, current_size, "Size")
                size_slider.set_preview_callback(lambda val: self.preview_object_size(obj, val))
                self.context_menu_sliders.append(size_slider)
            elif obj.obj_type == "TRIANGLE":
                current_size = obj.side_length
                min_size = current_size * 0.5
                max_size = current_size * 2.0
                size_slider = Slider(x + 20, y + 50, menu_width - 40, 20, min_size, max_size, current_size, "Size")
                size_slider.set_preview_callback(lambda val: self.preview_object_size(obj, val))
                self.context_menu_sliders.append(size_slider)
            else:  # BOX
                current_size = max(obj.width, obj.height)
                min_size = current_size * 0.5
                max_size = current_size * 2.0
                size_slider = Slider(x + 20, y + 50, menu_width - 40, 20, min_size, max_size, current_size, "Size")
                size_slider.set_preview_callback(lambda val: self.preview_object_size(obj, val))
                self.context_menu_sliders.append(size_slider)
            
            # Add rotation slider
            current_angle = math.degrees(obj.angle) % 360
            angle_slider = Slider(x + 20, y + 50 + slider_spacing, menu_width - 40, 20, 0, 360, current_angle, "Angle")
            angle_slider.set_preview_callback(lambda val: self.preview_object_rotation(obj, val))
            self.context_menu_sliders.append(angle_slider)
            
            # Store original values for cancel functionality
            obj.original_size = current_size
            obj.original_angle = obj.angle
            
            # Add buttons
            self.context_menu_items = [
                {"label": "Apply Changes", "action": f"APPLY_CHANGES:{obj.id}"},
                {"label": "Delete", "action": f"DELETE:{obj.id}"}
            ]
        else:  # It's a Portal
            # Add size slider
            current_size = obj.height
            min_size = current_size * 0.5
            max_size = current_size * 2.0
            size_slider = Slider(x + 20, y + 50, menu_width - 40, 20, min_size, max_size, current_size, "Size")
            size_slider.set_preview_callback(lambda val: self.preview_portal_size(obj, val))
            self.context_menu_sliders.append(size_slider)
            
            # Add rotation slider
            current_angle = math.degrees(obj.angle) % 360
            angle_slider = Slider(x + 20, y + 50 + slider_spacing, menu_width - 40, 20, 0, 360, current_angle, "Angle")
            angle_slider.set_preview_callback(lambda val: self.preview_portal_rotation(obj, val))
            self.context_menu_sliders.append(angle_slider)
            
            # Store original values
            obj.original_size = current_size
            obj.original_angle = obj.angle
            
            # Add buttons
            self.context_menu_items = [
                {"label": "Apply Changes", "action": f"APPLY_CHANGES:{obj.id}"},
                {"label": "Delete", "action": f"DELETE:{obj.id}"}
            ]
        
        self.logger.info(f"Opened context menu with sliders for object {obj.id}")
    
    def preview_object_size(self, obj, value):
        """Preview object size change without permanently applying it."""
        # Temporarily update object size for preview
        if obj.obj_type == "CIRCLE":
            obj.radius = value
        elif obj.obj_type == "TRIANGLE":
            obj.side_length = value
        else:  # BOX
            obj.width = value
            obj.height = value
            
    def preview_object_rotation(self, obj, value):
        """Preview object rotation without permanently applying it."""
        # Convert degrees to radians for preview
        radian_value = math.radians(value)
        obj.angle = radian_value
        # If object has a body, update its angle too for physics preview
        if hasattr(obj, 'body') and obj.body:
            obj.body.angle = radian_value
        
    def preview_portal_size(self, portal, value):
        """Preview portal size change."""
        # Keep width/height ratio for portals
        ratio = portal.width / portal.height
        portal.height = value
        portal.width = value * ratio
        
    def preview_portal_rotation(self, portal, value):
        """Preview portal rotation."""
        radian_value = math.radians(value)
        portal.angle = radian_value
        # If portal has a sensor, update its angle too
        if hasattr(portal, 'sensor') and portal.sensor:
            portal.sensor.angle = radian_value
            
    def close_context_menu(self):
        """Close the context menu."""
        # Reset any temporary changes if not applied
        if self.context_menu_object:
            if hasattr(self.context_menu_object, 'original_size'):
                # Restore original values if needed
                if hasattr(self.context_menu_object, 'obj_type'):  # Game object
                    if self.context_menu_object.obj_type == "CIRCLE":
                        self.context_menu_object.radius = self.context_menu_object.original_size
                    elif self.context_menu_object.obj_type == "TRIANGLE":
                        self.context_menu_object.side_length = self.context_menu_object.original_size
                    else:  # BOX
                        self.context_menu_object.width = self.context_menu_object.original_size
                        self.context_menu_object.height = self.context_menu_object.original_size
                else:  # Portal
                    ratio = self.context_menu_object.width / self.context_menu_object.height
                    self.context_menu_object.height = self.context_menu_object.original_size
                    self.context_menu_object.width = self.context_menu_object.original_size * ratio
                    
                # Restore original angle
                if hasattr(self.context_menu_object, 'original_angle'):
                    self.context_menu_object.angle = self.context_menu_object.original_angle
                
                # Remove temporary attributes
                delattr(self.context_menu_object, 'original_size')
                if hasattr(self.context_menu_object, 'original_angle'):
                    delattr(self.context_menu_object, 'original_angle')
                    
        self.context_menu_open = False
        self.context_menu_object = None
        self.context_menu_items = []
        self.context_menu_sliders = []
        self.logger.info("Closed context menu")
        
    def draw_context_menu(self):
        """Draw the context menu with sliders."""
        if not self.context_menu_open:
            return
            
        theme = self.themes[self.current_theme]
        
        # Calculate menu dimensions (account for sliders) - increase width to prevent overflow
        menu_width = 280  # Increased width to prevent slider overflow
        item_height = 30
        slider_spacing = 70  # Increased spacing for sliders
        menu_height = len(self.context_menu_items) * item_height + len(self.context_menu_sliders) * slider_spacing + 40  # More padding
        
        # Menu position (ensure it stays on screen)
        menu_x = min(self.context_menu_pos[0], self.width - menu_width - 10)
        menu_y = min(self.context_menu_pos[1], self.height - menu_height - 10)
        
        # Draw menu background with rounded corners
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        pygame.draw.rect(self.screen, theme["ui_element_color"], menu_rect, border_radius=6)
        pygame.draw.rect(self.screen, theme["ui_border_color"], menu_rect, 1, border_radius=6)
        
        # Draw menu title - positioned higher to avoid overlap
        title_text = "Object Properties"
        title_surface = self.title_font.render(title_text, True, theme["accent_color"])
        title_rect = title_surface.get_rect(midtop=(menu_x + menu_width // 2, menu_y + 10))
        self.screen.blit(title_surface, title_rect)
        
        # Update slider positions - adjust width to fit in menu
        y_offset = menu_y + 50  # Increased to avoid overlap with title
        for slider in self.context_menu_sliders:
            slider.rect.x = menu_x + 20
            slider.rect.y = y_offset
            slider.rect.width = menu_width - 40  # Adjust slider width to fit menu
            slider.update_handle_position()  # Important: update handle after changing dimensions
            slider.draw(self.screen, theme)
            y_offset += slider_spacing
        
        # Draw menu items
        for i, item in enumerate(self.context_menu_items):
            item_rect = pygame.Rect(
                menu_x + 10,
                y_offset + i * item_height,
                menu_width - 20,
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
            text_rect = text_surface.get_rect(center=item_rect.center)
            self.screen.blit(text_surface, text_rect)
            
    def handle_context_menu_click(self, x, y):
        """Handle clicks on the context menu."""
        if not self.context_menu_open:
            return None
            
        # Calculate menu dimensions - MUST MATCH values used in draw_context_menu
        menu_width = 280  # Match width with draw_context_menu
        item_height = 30
        slider_spacing = 70  # Match with draw_context_menu
        menu_height = len(self.context_menu_items) * item_height + len(self.context_menu_sliders) * slider_spacing + 40
        
        menu_x = min(self.context_menu_pos[0], self.width - menu_width - 10)
        menu_y = min(self.context_menu_pos[1], self.height - menu_height - 10)
        
        # Calculate y-offset for items - must match draw_context_menu
        y_offset = menu_y + 50 + len(self.context_menu_sliders) * slider_spacing
        
        # Check each menu item
        for i, item in enumerate(self.context_menu_items):
            item_rect = pygame.Rect(
                menu_x + 10,
                y_offset + i * item_height,
                menu_width - 20,
                item_height - 5
            )
            if item_rect.collidepoint(x, y):
                if item["action"].startswith("APPLY_CHANGES"):
                    # When applying changes, make preview changes permanent
                    obj_id = item["action"].split(":")[1]
                    
                    # Get values from sliders
                    if len(self.context_menu_sliders) >= 2:
                        size_value = self.context_menu_sliders[0].get_value()
                        angle_value = self.context_menu_sliders[1].get_value()
                        
                        # Ensure we have the latest values applied to the object
                        if hasattr(self.context_menu_object, 'obj_type'):  # Game object
                            self.preview_object_size(self.context_menu_object, size_value)
                            self.preview_object_rotation(self.context_menu_object, angle_value)
                        else:  # Portal
                            self.preview_portal_size(self.context_menu_object, size_value)
                            self.preview_portal_rotation(self.context_menu_object, angle_value)
                        
                        # Save original values to prevent them from being reset
                        if self.context_menu_object:
                            self.context_menu_object.original_size = size_value
                            self.context_menu_object.original_angle = math.radians(angle_value)
                        
                        # Log the action for debugging
                        self.logger.info(f"Applying changes: size={size_value}, angle={angle_value}")
                        
                        # Close menu
                        self.context_menu_open = False
                        
                        # Return combined action with the actual object ID
                        return f"RESIZE_AND_ROTATE:{obj_id}:{size_value}:{angle_value}"
                elif item["action"].startswith("DELETE"):
                    self.close_context_menu()
                    return item["action"]
                
        # Close context menu if clicked outside
        menu_rect = pygame.Rect(menu_x, menu_y, menu_width, menu_height)
        if not menu_rect.collidepoint(x, y):
            self.close_context_menu()
            
        return None

    def update_object_original_values(self, obj_id, size_value, angle_value):
        """Update the original values of an object after applying changes."""
        # This method is called from game_loop.py after changes are applied
        self.logger.info(f"Setting permanent values for {obj_id}: size={size_value}, angle={angle_value}")
        
        # Find the object in the game by ID (needed if context_menu_object is already None)
        if self.context_menu_object and self.context_menu_object.id == obj_id:
            obj = self.context_menu_object
        else:
            # We don't have direct access to objects here
            # But we don't need it since original values are already saved before menu closes
            return
            
        # Update the object's permanent values
        if hasattr(obj, 'obj_type'):  # Game object
            if obj.obj_type == "CIRCLE":
                obj.radius = size_value
            elif obj.obj_type == "TRIANGLE":
                obj.side_length = size_value
            else:  # BOX
                obj.width = size_value
                obj.height = size_value
        else:  # Portal
            ratio = obj.width / obj.height
            obj.height = size_value
            obj.width = size_value * ratio
            
        # Set the angle (in radians)
        obj.angle = math.radians(angle_value)
    
    def get_background_color(self):
        """Get the current theme's background color."""
        return self.themes[self.current_theme]["bg_color"]
    
    def get_box_color(self):
        """Get the current theme's box color."""
        return self.themes[self.current_theme]["box_color"]
        
    def get_circle_color(self):
        """Get the current theme's circle color."""
        return self.themes[self.current_theme]["circle_color"]
        
    def get_triangle_color(self):
        """Get the current theme's triangle color."""
        return self.themes[self.current_theme].get("triangle_color", (0, 200, 200))
        
    def get_portal_tint(self):
        """Get the current theme's portal tint factor."""
        return self.themes[self.current_theme]["portal_tint"]
        
    def toggle_theme(self):
        """Cycle to the next theme."""
        theme_options = list(self.themes.keys())
        current_index = theme_options.index(self.current_theme)
        next_index = (current_index + 1) % len(theme_options)
        self.current_theme = theme_options[next_index]
        self.logger.info(f"Changed theme to {self.current_theme}")
        return self.current_theme
    
    def update_object_original_values(self, obj_id, size_value, angle_value):
        """Update the original values of an object after applying changes.
        This is needed to ensure changes stay applied when closing the menu."""
        if self.context_menu_object and self.context_menu_object.id == obj_id:
            if hasattr(self.context_menu_object, 'original_size'):
                self.context_menu_object.original_size = size_value
            if hasattr(self.context_menu_object, 'original_angle'):
                self.context_menu_object.original_angle = math.radians(angle_value)
            self.logger.info(f"Updated original values for object {obj_id}")
