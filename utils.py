import pygame
import math
from settings import PPM, HEIGHT, to_pygame, to_box2d # Assuming Box2D is imported elsewhere when needed

def rotate_point(point, angle_rad, center):
    """Rotates a point around a center by a given angle in radians."""
    s = math.sin(angle_rad)
    c = math.cos(angle_rad)

    # Translate point back to origin
    px, py = point[0] - center[0], point[1] - center[1]

    # Rotate point
    x_new = px * c - py * s
    y_new = px * s + py * c

    # Translate point back
    return x_new + center[0], y_new + center[1]

def draw_text(surface, text, position, font, color=pygame.Color("black"), center=False):
    """Helper function to draw text. Returns the text rect."""
    if not font:
        print("Error: Attempted to draw text with no font.")
        return None
    try:
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if center:
            text_rect.center = position
        else:
            text_rect.topleft = position
        surface.blit(text_surface, text_rect)
        return text_rect # Return the rect for potential layout use
    except pygame.error as e:
        print(f"Error rendering text '{text}': {e}")
        return None
    except Exception as e:
         print(f"Unexpected error rendering text '{text}': {e}")
         return None


def get_body_vertices_pygame(body):
    """Gets world vertices of a polygon body in Pygame coordinates."""
    vertices_pygame = []
    if not body: return vertices_pygame

    for fixture in body.fixtures:
        shape = fixture.shape
        # Check if it's a polygon shape
        if hasattr(shape, 'vertices') and isinstance(shape.vertices, (list, tuple)):
            try:
                # Transform vertices from local body coordinates to world coordinates
                vertices_box2d = [(body.transform * v) for v in shape.vertices]
                # Convert world coordinates (meters) to Pygame coordinates (pixels)
                vertices_pygame = [to_pygame(v) for v in vertices_box2d]
                # Assuming the first polygon fixture defines the renderable shape
                break
            except Exception as e:
                 print(f"Error transforming vertices for body {body}: {e}")
                 return [] # Return empty on error
    return vertices_pygame

def is_sensor(fixture):
    """Safely checks if a Box2D fixture is a sensor, handling different Box2D-py API versions."""
    try:
        # Try property access (older Box2D-py versions)
        return fixture.isSensor
    except AttributeError:
        try:
            # Try method call (some Box2D-py versions)
            return fixture.IsSensor()
        except AttributeError:
            try:
                # Try fixture def property with different casing
                return fixture.sensor
            except AttributeError:
                # If all checks fail, use getters if available
                try:
                    return fixture.GetFilterData().isSensor
                except:
                    # Last resort - check through userData if available
                    if hasattr(fixture, 'userData') and fixture.userData and isinstance(fixture.userData, dict):
                        return fixture.userData.get('isSensor', False)
                    # If all checks fail, assume it's not a sensor
                    print(f"Warning: Could not determine if fixture is sensor: {fixture}")
                    return False