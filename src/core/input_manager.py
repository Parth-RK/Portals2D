import pygame
from src.utils.logger import Logger

class InputManager:
    def __init__(self):
        self.logger = Logger()
        self.mouse_pos = (0, 0)
        
        # State for portal creation
        self.portal_creation_mode = False
        self.current_portal_color_index = 0
        self.portal_colors = ["BLUE", "ORANGE", "GREEN", "PURPLE", "YELLOW", "CYAN", "MAGENTA"]
        self.portal_pair_count = {color: 0 for color in self.portal_colors}
        
        # State for object dragging
        self.dragged_object = None
        self.drag_offset = (0, 0)
        self.throw_velocity = (0, 0)
        self.last_mouse_pos = (0, 0)
        self.mouse_velocity = (0, 0)
        
        # State for context menu
        self.context_menu_open = False
        self.context_menu_object = None
        
        self.logger.info("Input manager initialized")
        
    def process_events(self, events=None):
        """Process all input events and return a list of actions."""
        commands = []
        
        # Get current mouse position
        current_mouse_pos = pygame.mouse.get_pos()
        
        # Calculate mouse velocity for throwing objects
        if self.last_mouse_pos != (0, 0):
            self.mouse_velocity = (
                (current_mouse_pos[0] - self.last_mouse_pos[0]) * 10,  # Scale for more dramatic throws
                (current_mouse_pos[1] - self.last_mouse_pos[1]) * 10
            )
        self.last_mouse_pos = current_mouse_pos
        self.mouse_pos = current_mouse_pos
        
        # If events weren't provided, get them now
        if events is None:
            events = pygame.event.get()
            
        for event in events:
            # Handle quit event
            if event.type == pygame.QUIT:
                commands.append("QUIT")
                
            # Handle key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.context_menu_open:
                        # Close context menu if open
                        self.context_menu_open = False
                        commands.append("CLOSE_CONTEXT_MENU")
                    else:
                        commands.append("QUIT")
                elif event.key == pygame.K_g:
                    commands.append("TOGGLE_GRAVITY")
                elif event.key == pygame.K_b:
                    # Create a box at mouse position
                    commands.append(f"CREATE_OBJECT:BOX:{self.mouse_pos[0]}:{self.mouse_pos[1]}")
                elif event.key == pygame.K_c:
                    # Create a circle at mouse position
                    commands.append(f"CREATE_OBJECT:CIRCLE:{self.mouse_pos[0]}:{self.mouse_pos[1]}")
                elif event.key == pygame.K_t:
                    # Swap T and Shift+T - T now creates triangle, Shift+T changes theme
                    if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        commands.append("TOGGLE_THEME")
                    else:
                        commands.append(f"CREATE_OBJECT:TRIANGLE:{self.mouse_pos[0]}:{self.mouse_pos[1]}")
                elif event.key == pygame.K_p:
                    # Handle portal creation mode
                    color = self.portal_colors[self.current_portal_color_index]
                    portal_id = f"{self.portal_pair_count[color] % 2}"
                    
                    # When creating portals, prefer to give them a vertical orientation by default
                    default_angle = 0  # Vertical orientation
                    
                    commands.append(f"CREATE_PORTAL:{color}:{portal_id}:{self.mouse_pos[0]}:{self.mouse_pos[1]}:{default_angle}")
                    
                    # Update portal state
                    self.portal_pair_count[color] += 1
                    if self.portal_pair_count[color] % 2 == 0:
                        # Move to next color after creating a pair
                        self.current_portal_color_index = (self.current_portal_color_index + 1) % len(self.portal_colors)
                    
                    self.logger.info(f"Created portal {portal_id} of color {color}")
                    
            # Handle mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if self.context_menu_open:
                        # Handle context menu selection
                        commands.append(f"CONTEXT_MENU_SELECT:{self.mouse_pos[0]}:{self.mouse_pos[1]}")
                        self.context_menu_open = False
                    else:
                        # Try to grab an object
                        commands.append(f"TRY_GRAB_OBJECT:{self.mouse_pos[0]}:{self.mouse_pos[1]}")
                elif event.button == 3:  # Right click
                    # Open context menu for object if clicked
                    commands.append(f"TRY_OPEN_CONTEXT_MENU:{self.mouse_pos[0]}:{self.mouse_pos[1]}")
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.dragged_object:  # Left click release
                    # Throw the object with current velocity
                    commands.append(f"THROW_OBJECT:{self.dragged_object}:{self.mouse_velocity[0]}:{self.mouse_velocity[1]}")
                    self.dragged_object = None
                    
            elif event.type == pygame.MOUSEMOTION:
                # Update dragged object position
                if self.dragged_object:
                    commands.append(f"DRAG_OBJECT:{self.dragged_object}:{self.mouse_pos[0]}:{self.mouse_pos[1]}")
        
        return commands
        
    def set_dragged_object(self, obj_id):
        """Set which object is currently being dragged."""
        self.dragged_object = obj_id
        
    def clear_dragged_object(self):
        """Clear the currently dragged object."""
        self.dragged_object = None
        
    def set_context_menu_open(self, is_open, obj_id=None):
        """Set the context menu state."""
        self.context_menu_open = is_open
        self.context_menu_object = obj_id
