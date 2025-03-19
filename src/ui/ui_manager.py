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
        
        # Button areas (for future implementation)
        self.buttons = {}
        
        # Help text and controls display
        self.show_help = True
        self.help_text = [
            "Controls:",
            "ESC - Quit game",
            "G - Toggle gravity",
            "B - Create box at cursor",
            "C - Create circle at cursor",
            "Left click - Place blue portal",
            "Right click - Place orange portal"
        ]
        
        self.logger.info("UI Manager initialized")
        
    def update(self, dt):
        """Update UI elements."""
        # For future: update button states, animations, etc.
        pass
        
    def draw(self):
        """Draw UI elements."""
        # Draw FPS and object count in top-left corner
        self.draw_debug_info()
        
        # Draw help text if visible
        if self.show_help:
            self.draw_help_text()
        
    def draw_debug_info(self):
        """Draw debug information."""
        fps = int(pygame.time.Clock().get_fps())
        fps_text = f"FPS: {fps}"
        
        # Render FPS text
        fps_surface = self.font.render(fps_text, True, (255, 255, 255))
        self.screen.blit(fps_surface, (10, 10))
        
    def draw_help_text(self):
        """Draw help text with controls."""
        y_offset = 50
        for line in self.help_text:
            text_surface = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 25
            
    def toggle_help(self):
        """Toggle help text visibility."""
        self.show_help = not self.show_help
        self.logger.info(f"Help text {'shown' if self.show_help else 'hidden'}")
        
    def add_button(self, name, rect, callback):
        """Add a button to the UI."""
        self.buttons[name] = {
            'rect': rect,
            'callback': callback,
            'hover': False,
            'active': False
        }
        
    def handle_mouse_event(self, event, pos):
        """Handle mouse events for UI elements."""
        if event.type == pygame.MOUSEMOTION:
            # Update button hover states
            for button_name, button in self.buttons.items():
                button['hover'] = button['rect'].collidepoint(pos)
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check button clicks
            for button_name, button in self.buttons.items():
                if button['rect'].collidepoint(pos):
                    button['active'] = True
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            # Execute button callbacks
            for button_name, button in self.buttons.items():
                if button['active'] and button['rect'].collidepoint(pos):
                    button['callback']()
                button['active'] = False
