import pygame
import Box2D
# Screen Dimensions
WIDTH = 1280
HEIGHT = 720
FPS = 60

# Physics Settings
PPM = 20.0  # Pixels per meter (essential Box2D scaling factor)
TIME_STEP = 1.0 / FPS
VELOCITY_ITERATIONS = 8
POSITION_ITERATIONS = 3
GRAVITY = (0, -9.8) # Standard gravity in m/s^2

# Colors (Mini Metro Inspired Palette)
COLOR_BACKGROUND = pygame.Color("#F7F5F2") # Soft off-white
COLOR_TEXT = pygame.Color("#333333")      # Dark gray
COLOR_DEBUG = pygame.Color("#FF0000")     # For debug drawing
COLOR_GRID = pygame.Color("#E0E0E0")      # Grid color

# Object Colors (Bold Primary)
COLOR_CIRCLE = pygame.Color("#1A73E8")    # Blue
COLOR_SQUARE = pygame.Color("#EA4335")    # Red
COLOR_TRIANGLE = pygame.Color("#FBBC04")  # Yellow (Add if needed)

# Portal Colors (Pastel/Secondary Variants - Define pairs later)
PORTAL_COLORS = [
    pygame.Color("#A0C3FF"), # Light Blue
    pygame.Color("#FAD2CF"), # Light Red
    pygame.Color("#FFF8E1"), # Light Yellow
    pygame.Color("#D1FAD7"), # Light Green
    pygame.Color("#E8DFF5"), # Light Purple
]

# UI Colors
COLOR_UI_ACCENT = pygame.Color("#1A73E8") # Use a primary color for accents
COLOR_BUTTON_NORMAL = pygame.Color("#E0E0E0")
COLOR_BUTTON_HOVER = pygame.Color("#CCCCCC")
COLOR_BUTTON_PRESSED = pygame.Color("#BDBDBD")
COLOR_PORTAL_PREVIEW = pygame.Color("#4CAF50") # Green for portal preview line

# Font Settings
DEFAULT_FONT_SIZE = 16
DEFAULT_FONT_NAME = 'Roboto-Regular.ttf' # Assumes font file is in assets/fonts
UI_FONT_SIZE = 18
HUD_FONT_SIZE = 14

# Object Defaults
DEFAULT_CIRCLE_RADIUS = 16 / PPM
DEFAULT_BOX_SIZE = (32 / PPM, 32 / PPM)

# Portal Defaults
DEFAULT_PORTAL_HEIGHT = 60 / PPM
DEFAULT_PORTAL_WIDTH = 10 / PPM
PORTAL_COOLDOWN = 5 # Seconds

# --- Helper Functions for Coordinate Conversion ---

def to_pygame(coords):
    """Convert Box2D coordinates (meters) to Pygame coordinates (pixels)."""
    # Check if it looks like a Box2D vector or a simple tuple/list
    if hasattr(coords, 'x') and hasattr(coords, 'y'):
        return int(coords.x * PPM), int(HEIGHT - coords.y * PPM)
    elif isinstance(coords, (tuple, list)) and len(coords) == 2:
        return int(coords[0] * PPM), int(HEIGHT - coords[1] * PPM)
    # Handle scalar conversion if needed, or raise error for unexpected type
    elif isinstance(coords, (int, float)):
         print(f"Warning: to_pygame received scalar {coords}, returning int.")
         return int(coords)
    print(f"Warning: Unexpected type in to_pygame: {type(coords)}")
    return int(coords[0]), int(coords[1]) # Best guess


def to_box2d(coords):
    """Convert Pygame coordinates (pixels) to Box2D coordinates (meters)."""
    if isinstance(coords, (tuple, list)) and len(coords) == 2:
        # Adjust y-coordinate based on Pygame's inverted y-axis
        # Return a Box2D vector instead of a tuple
        return Box2D.b2Vec2(coords[0] / PPM, (HEIGHT - coords[1]) / PPM)
    elif isinstance(coords, (int, float)):
        print(f"Warning: to_box2d received scalar {coords}, returning float.")
        return float(coords)
    print(f"Warning: Unexpected type in to_box2d: {type(coords)}")
    # If we can't determine the proper conversion, try to return something safe
    try:
        return Box2D.b2Vec2(float(coords[0]), float(coords[1]))
    except:
        return Box2D.b2Vec2(0, 0)  # Last resort fallback


def scalar_to_pygame(scalar):
    """Convert Box2D scalar (meters) to Pygame scalar (pixels)."""
    return int(scalar * PPM)

def scalar_to_box2d(scalar):
     """Convert Pygame scalar (pixels) to Box2D scalar (meters)."""
     return scalar / PPM

# Convenience aliases for Box2D types directly
# Avoid redefining types like b2Vec2 = Box2D.b2Vec2 here if possible,
# just use Box2D.b2Vec2 directly in the code for clarity.

# --- User Data Types for Box2D Bodies ---
# Helps identify body types during collisions
USER_DATA_OBJECT = 'object'
USER_DATA_PORTAL = 'portal'
USER_DATA_WALL = 'wall'