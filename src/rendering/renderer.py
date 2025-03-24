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
        
        # Apply teleport animation scaling if active
        scale = 1.0
        if hasattr(game_object, 'is_teleporting') and game_object.is_teleporting:
            scale = game_object.current_scale
            if scale < 0.1:  # Don't render if almost invisible during teleport
                return
        
        if game_object.obj_type == "CIRCLE":
            # Apply teleport animation scaling
            radius = int(game_object.radius * scale)
            
            pygame.draw.circle(
                self.screen, 
                game_object.color, 
                screen_pos, 
                radius
            )
            
            # Draw a line to show orientation
            end_x = screen_pos[0] + int(math.cos(game_object.angle) * radius)
            end_y = screen_pos[1] + int(math.sin(game_object.angle) * radius)
            pygame.draw.line(
                self.screen,
                (0, 0, 0),  # Black
                screen_pos,
                (end_x, end_y),
                2
            )
        elif game_object.obj_type == "TRIANGLE":
            # Apply teleport animation scaling
            side_length = game_object.side_length * scale
            
            # Create a surface for the triangle
            triangle_surface = pygame.Surface((side_length, side_length), pygame.SRCALPHA)
            
            # Calculate triangle points (equilateral)
            height = side_length * math.sqrt(3) / 2
            points = [
                (side_length / 2, 0),  # top
                (0, height),  # bottom left
                (side_length, height)  # bottom right
            ]
            
            # Draw the triangle
            pygame.draw.polygon(triangle_surface, game_object.color, points)
            
            # Rotate the surface
            if game_object.angle != 0:
                angle_degrees = math.degrees(game_object.angle)
                rotated_surface = pygame.transform.rotate(triangle_surface, -angle_degrees)
                
                # Get the rect of the rotated surface and center it
                rotated_rect = rotated_surface.get_rect(center=screen_pos)
                
                # Draw the rotated surface
                self.screen.blit(rotated_surface, rotated_rect)
            else:
                # Center the triangle on screen_pos
                pos = (screen_pos[0] - side_length / 2, 
                       screen_pos[1] - height / 2)
                self.screen.blit(triangle_surface, pos)
            
            # Draw a line to show orientation if not too small during animation
            if scale > 0.3:
                if game_object.angle == 0:
                    end_x = screen_pos[0]
                    end_y = screen_pos[1] - height / 2  # Point to the top vertex
                else:
                    # Calculate rotated top point
                    end_x = screen_pos[0] + math.sin(game_object.angle) * height / 2
                    end_y = screen_pos[1] - math.cos(game_object.angle) * height / 2
                    
                pygame.draw.line(
                    self.screen,
                    (0, 0, 0),  # Black
                    screen_pos,
                    (end_x, end_y),
                    2
                )
        else:  # BOX or default
            # Apply teleport animation scaling
            width = game_object.width * scale
            height = game_object.height * scale
            
            # Create a rect for the box
            rect = pygame.Rect(
                screen_pos[0] - width / 2,
                screen_pos[1] - height / 2,
                width,
                height
            )
            
            # Rotate and draw the box
            if game_object.angle == 0:
                pygame.draw.rect(self.screen, game_object.color, rect)
            else:
                # Create a surface for rotation
                box_surface = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.rect(box_surface, game_object.color, (0, 0, width, height))
                
                # Rotate the surface
                angle_degrees = math.degrees(game_object.angle)
                rotated_surface = pygame.transform.rotate(box_surface, -angle_degrees)
                
                # Get the rect of the rotated surface and center it
                rotated_rect = rotated_surface.get_rect(center=screen_pos)
                
                # Draw the rotated surface
                self.screen.blit(rotated_surface, rotated_rect)
                
    def draw_portal(self, portal):
        """Draw a portal with directional indicators."""
        screen_pos = (int(portal.position.x), int(portal.position.y))
        
        # Create a surface for the portal
        portal_surface = pygame.Surface((portal.width, portal.height), pygame.SRCALPHA)
        
        # Use portal.color (which contains the RGB tuple)
        portal_color = portal.color
        
        # Draw the main portal rectangle
        pygame.draw.rect(
            portal_surface,
            portal_color,
            (0, 0, portal.width, portal.height),
            border_radius=3  # Add rounded corners
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
        
        # Draw directional arrow (facing outward from the portal)
        arrow_color = (255, 255, 255, 220)  # Slightly transparent white
        arrow_length = min(portal.width, portal.height) * 0.4
        
        # Draw arrow at the center of the portal
        center_x = portal.width // 2
        center_y = portal.height // 2
        
        # Arrow points from center to the edge based on portal orientation
        # For vertical portals (the default), arrow points to the right
        # For horizontal portals, arrow points down
        arrow_head_size = arrow_length * 0.4
        
        # Draw arrow shaft
        pygame.draw.line(
            portal_surface,
            arrow_color,
            (center_x, center_y),
            (center_x + arrow_length, center_y),
            3
        )
        
        # Draw arrow head
        pygame.draw.polygon(
            portal_surface,
            arrow_color,
            [
                (center_x + arrow_length, center_y),  # tip
                (center_x + arrow_length - arrow_head_size, center_y - arrow_head_size/2),  # top corner
                (center_x + arrow_length - arrow_head_size, center_y + arrow_head_size/2),  # bottom corner
            ]
        )
        
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
