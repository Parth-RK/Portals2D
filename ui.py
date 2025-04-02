import pygame
from settings import (COLOR_TEXT, COLOR_BUTTON_NORMAL, COLOR_BUTTON_HOVER,
                      COLOR_BUTTON_PRESSED, UI_FONT_SIZE) # Keep using settings
from utils import draw_text # Keep using text utility

class Button:
    """A simple clickable button with different visual states."""
    def __init__(self, rect, text, callback, font,
                 color_normal=COLOR_BUTTON_NORMAL,
                 color_hover=COLOR_BUTTON_HOVER,
                 color_pressed=COLOR_BUTTON_PRESSED,
                 text_color=COLOR_TEXT,
                 border_radius=5): # Add border radius
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback # The function to call when clicked
        self.font = font
        self.colors = {'normal': color_normal, 'hover': color_hover, 'pressed': color_pressed}
        self.text_color = text_color
        self.border_radius = border_radius
        self.state = 'normal' # Possible states: normal, hover, pressed
        self.visible = True
        self.enabled = True

    def handle_event(self, event):
        """Handles mouse events relevant to the button. Returns True if event was handled."""
        if not self.visible or not self.enabled:
             return False # Cannot interact if not visible or enabled

        event_handled = False
        mouse_pos = pygame.mouse.get_pos()
        collides = self.rect.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEMOTION:
            if collides:
                # If mouse moved over the button, change state to hover (unless already pressed)
                if self.state != 'pressed':
                    self.state = 'hover'
                    event_handled = True # Hovering is an interaction
            else:
                # If mouse moved off the button, reset state to normal
                if self.state == 'hover':
                     self.state = 'normal'
                     event_handled = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # If left mouse button pressed down while over the button
            if event.button == 1 and collides:
                self.state = 'pressed'
                event_handled = True # Pressing down handled
        elif event.type == pygame.MOUSEBUTTONUP:
            # If left mouse button released
            if event.button == 1:
                 # If it was released while in 'pressed' state (i.e., was pressed on this button)
                 if self.state == 'pressed':
                      if collides:
                           # If released over the button -> SUCCESSFUL CLICK
                           self.state = 'hover' # Go back to hover state after click
                           if self.callback:
                                try:
                                    self.callback() # Execute the button's action
                                except Exception as e:
                                     print(f"Error executing button callback for '{self.text}': {e}")
                           event_handled = True # Click handled
                      else:
                           # If released outside the button after pressing it -> cancel click
                           self.state = 'normal'
                           event_handled = True # Release handled (no action)

        return event_handled # Let InputManager know if event is used

    def draw(self, surface, renderer):
        """Draws the button based on its current state."""
        if not self.visible: return # Don't draw if not visible

        # Determine color based on state (and enabled status)
        base_color = self.colors[self.state]
        if not self.enabled:
             # Desaturate or darken color if disabled (simple grayscale lerp)
             disabled_color = base_color.lerp(pygame.Color('gray'), 0.6)
             final_color = disabled_color
             text_color = COLOR_TEXT.lerp(pygame.Color('gray'), 0.5)
        else:
             final_color = base_color
             text_color = self.text_color


        try:
            # Draw the button background rectangle
            pygame.draw.rect(surface, final_color, self.rect, border_radius=self.border_radius)
            # Optional: Draw a subtle outline
            outline_color = final_color.lerp(COLOR_TEXT, 0.2)
            pygame.draw.rect(surface, outline_color, self.rect, 1, border_radius=self.border_radius)

            # Draw the button text centered
            if self.text and self.font:
                draw_text(surface, self.text, self.rect.center, self.font, text_color, center=True)
        except Exception as e:
             print(f"Error drawing button '{self.text}': {e}")


    def is_clicked(self, pos):
        """DEPRECATED - Use handle_event. Checks if a point is inside the button rect."""
        return self.visible and self.enabled and self.rect.collidepoint(pos)

class UIManager:
    def __init__(self, assets):
        self.elements = [] # List of UI elements (buttons, labels, etc.)
        self.assets = assets
        # Get font safely, providing fallback if needed
        self.ui_font = assets.get('ui_font', pygame.font.SysFont(None, UI_FONT_SIZE))

    def create_button(self, rect, text, callback, **kwargs):
        """Creates a Button and adds it to the UI manager."""
        if not self.ui_font:
             print("Warning: UI Font not available, cannot create button with text.")
             # Potentially use a default sysfont or create without text
             # font = pygame.font.SysFont(None, UI_FONT_SIZE)
             return None # Or handle differently

        button = Button(rect, text, callback, self.ui_font, **kwargs)
        self.elements.append(button)
        return button

    # Add methods for other UI elements (Labels, sliders?) here
    # def create_label(...)

    def handle_event(self, event):
        """Passes events to UI elements, stopping if one handles it."""
        handled = False
        # Iterate in reverse order so topmost elements receive events first
        for element in reversed(self.elements):
            # Check if the element has a handle_event method
            if hasattr(element, 'handle_event'):
                if element.handle_event(event):
                    handled = True
                    break # Stop processing this event if a UI element consumed it
        return handled

    def update(self, dt):
        """Update UI elements if needed (e.g., animations, timers)."""
        for element in self.elements:
            if hasattr(element, 'update'): # If element has an update method
                 element.update(dt)


    def get_elements(self):
        """Returns the list of UI elements for rendering."""
        return self.elements