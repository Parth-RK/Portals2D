import pygame
from src.utils.logger import Logger

class InputManager:
    def __init__(self):
        self.logger = Logger()
        self.mouse_pos = (0, 0)
        self.logger.info("Input manager initialized")
        
    def process_events(self):
        """Process all input events and return a list of actions."""
        commands = []
        
        # Get current mouse position
        self.mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            # Handle quit event
            if event.type == pygame.QUIT:
                commands.append("QUIT")
                
            # Handle key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    commands.append("QUIT")
                elif event.key == pygame.K_g:
                    commands.append("TOGGLE_GRAVITY")
                elif event.key == pygame.K_b:
                    # Create a box at mouse position
                    commands.append(f"CREATE_OBJECT:BOX:{self.mouse_pos[0]}:{self.mouse_pos[1]}")
                elif event.key == pygame.K_c:
                    # Create a circle at mouse position
                    commands.append(f"CREATE_OBJECT:CIRCLE:{self.mouse_pos[0]}:{self.mouse_pos[1]}")
                    
            # Handle mouse clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    # Create blue portal
                    commands.append(f"CREATE_PORTAL:BLUE:{self.mouse_pos[0]}:{self.mouse_pos[1]}:0")
                elif event.button == 3:  # Right click
                    # Create orange portal
                    commands.append(f"CREATE_PORTAL:ORANGE:{self.mouse_pos[0]}:{self.mouse_pos[1]}:0")
        
        return commands
