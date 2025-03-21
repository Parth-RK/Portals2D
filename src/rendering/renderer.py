import pygame
import math
from src.utils.logger import Logger

class Renderer:
    def __init__(self, screen, object_manager):
        self.logger = Logger()
        self.screen = screen
        self.object_manager = object_manager
        self.width, self.height = screen.get_size()
        self.background_color = (255, 255, 250)  # Default background color
        self.logger.info("Renderer initialized")
        
    def set_background_color(self, color):
        """Set the background color."""
        self.background_color = color
        
    def clear(self):
        """Clear the screen."""
        self.screen.fill(self.background_color)
        
    def draw_objects(self):
        """Draw all game objects and portals."""
        # Draw all game objects
        for obj in self.object_manager.get_objects():
            self.draw_object(obj)
            
        # Draw all portals
        for portal in self.object_manager.get_portals():
            self.draw_portal(portal)
            
    def draw_object(self, game_object):
        """Draw a game object."""
        screen_pos = (int(game_object.position.x), int(game_object.position.y))
        
        if game_object.obj_type == "CIRCLE":
            pygame.draw.circle(
                self.screen, 
                game_object.color, 
                screen_pos, 
                int(game_object.radius)
            )
            
            # Draw a line to show orientation
            end_x = screen_pos[0] + int(math.cos(game_object.angle) * game_object.radius)
            end_y = screen_pos[1] + int(math.sin(game_object.angle) * game_object.radius)
            pygame.draw.line(
                self.screen,
                (0, 0, 0),  # Black
                screen_pos,
                (end_x, end_y),
                2
            )
        else:  # BOX or default
            # Create a rect for the box
            rect = pygame.Rect(
                screen_pos[0] - game_object.width / 2,
                screen_pos[1] - game_object.height / 2,
                game_object.width,
                game_object.height
            )
            
            # Rotate and draw the box
            if game_object.angle == 0:
                pygame.draw.rect(self.screen, game_object.color, rect)
            else:
                # Create a surface for rotation
                box_surface = pygame.Surface((game_object.width, game_object.height), pygame.SRCALPHA)
                pygame.draw.rect(box_surface, game_object.color, (0, 0, game_object.width, game_object.height))
                
                # Rotate the surface
                angle_degrees = math.degrees(game_object.angle)
                rotated_surface = pygame.transform.rotate(box_surface, -angle_degrees)
                
                # Get the rect of the rotated surface and center it
                rotated_rect = rotated_surface.get_rect(center=screen_pos)
                
                # Draw the rotated surface
                self.screen.blit(rotated_surface, rotated_rect)
                
    def draw_portal(self, portal):
        """Draw a portal."""
        screen_pos = (int(portal.position.x), int(portal.position.y))
        
        # Create a surface for the portal
        portal_surface = pygame.Surface((portal.width, portal.height), pygame.SRCALPHA)
        
        # Use portal.color (which contains the RGB tuple)
        portal_color = portal.color
        
        # Draw the main portal rectangle
        pygame.draw.rect(
            portal_surface,
            portal_color,
            (0, 0, portal.width, portal.height)
        )
        
        # Add a glow effect - get color components
        r, g, b = portal_color[0], portal_color[1], portal_color[2]
        
        # Create glow with semi-transparency
        glow_color = (r, g, b, 128)  # Add alpha for glow effect
        
        # Add an inner highlight for a more portal-like appearance
        highlight_color = (min(r + 70, 255), min(g + 70, 255), min(b + 70, 255), 200)
        highlight_rect = pygame.Rect(portal.width * 0.25, portal.height * 0.25, 
                                    portal.width * 0.5, portal.height * 0.5)
        pygame.draw.rect(portal_surface, highlight_color, highlight_rect)
        
        # Add outer glow
        glow_rect = pygame.Rect(-5, -5, portal.width + 10, portal.height + 10)
        pygame.draw.rect(portal_surface, glow_color, glow_rect, 5)
        
        # Portal connection indicator (draw a small indicator if portal is linked)
        if portal.linked_portal:
            # Draw a small dot in the center to indicate connection
            pygame.draw.circle(portal_surface, (255, 255, 255), 
                              (portal.width // 2, portal.height // 2), 3)
        
        # Rotate the portal
        angle_degrees = math.degrees(portal.angle)
        rotated_surface = pygame.transform.rotate(portal_surface, -angle_degrees)
        
        # Draw the portal
        rotated_rect = rotated_surface.get_rect(center=screen_pos)
        self.screen.blit(rotated_surface, rotated_rect)
