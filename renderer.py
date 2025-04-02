import pygame
import math
from settings import (COLOR_BACKGROUND, COLOR_DEBUG, COLOR_TEXT, COLOR_UI_ACCENT,
                        HUD_FONT_SIZE, to_pygame, Box2D,
                      COLOR_GRID, COLOR_PORTAL_PREVIEW, PPM, scalar_to_pygame) # Add Grid, Preview colors
from utils import draw_text, is_sensor # Add our new utility function import

class Renderer:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets # Dictionary containing loaded fonts, etc.
        # Fallback to default system font if specific font wasn't loaded
        self.debug_font = self.assets.get('debug_font', pygame.font.SysFont("monospace", 15))
        self.hud_font = self.assets.get('hud_font', pygame.font.SysFont(None, HUD_FONT_SIZE)) # Use setting size

    def render_all(self, game_state):
        """Main render function, draws everything based on game state."""
        if not self.screen: return # Cannot render without a screen

        # 1. Background Clear & Grid
        self.screen.fill(COLOR_BACKGROUND)
        self._draw_grid() # Draw subtle background grid

        # 2. Render Portals (Draw portals underneath objects)
        for portal in game_state.get('portals', []):
            portal.draw(self.screen, self) # Delegate drawing to portal object

        # 3. Render Portal Creation Preview Line
        preview_line = game_state.get('portal_preview_line')
        if preview_line:
             start_pos, end_pos = preview_line
             try: # Add error handling for drawing functions
                 pygame.draw.line(self.screen, COLOR_PORTAL_PREVIEW, start_pos, end_pos, 3) # Thicker line
             except Exception as e:
                  print(f"Error drawing portal preview line: {e}")

        # 4. Render Objects
        for obj in game_state.get('objects', []):
            # Delegate drawing to the object's draw method
            # This allows different object types to draw themselves
            obj.draw(self.screen, self)

        # 5. Render UI Elements (Buttons, HUD)
        self._draw_hud(game_state.get('hud_info', {}))
        for element in game_state.get('ui_elements', []):
            try:
                element.draw(self.screen, self) # UI elements draw themselves
            except Exception as e:
                 print(f"Error drawing UI element {element}: {e}")


        # 6. Debug Drawing (Optional)
        if game_state.get('debug_mode', False):
            # Draw physics wireframes
            physics_world = game_state.get('physics_world')
            if physics_world:
                self._draw_physics_debug(physics_world)
            # Draw debug text info
            self._draw_debug_info(game_state.get('debug_info', {}))

        # 7. Flip Display to show the rendered frame
        try:
            pygame.display.flip()
        except pygame.error as e:
             print(f"Error flipping display: {e}")


    # --- Specific Drawing Methods (Called by Objects/Portals/Self) ---

    def draw_circle(self, surface, color, pos_pygame, radius_pygame, angle_rad):
        """Draws a circle with an optional orientation line."""
        try:
            # Ensure radius is at least 1 pixel for visibility
            draw_radius = max(1, radius_pygame)
            pygame.draw.circle(surface, color, pos_pygame, draw_radius)

            # Draw orientation line if radius is large enough to see it
            if draw_radius > 3:
                # Calculate end point of the line based on angle
                # Remember Pygame's Y-axis is inverted for angle calculations
                end_line_x = pos_pygame[0] + draw_radius * math.cos(angle_rad)
                end_line_y = pos_pygame[1] - draw_radius * math.sin(angle_rad) # Use subtraction for Pygame Y
                # Draw line from center to edge
                pygame.draw.line(surface, COLOR_BACKGROUND, pos_pygame, (int(end_line_x), int(end_line_y)), 1)
        except Exception as e:
            print(f"Error drawing circle at {pos_pygame}: {e}")

    def draw_polygon(self, surface, color, vertices_pygame):
        """Draws a filled polygon given vertices in Pygame coordinates."""
        if len(vertices_pygame) >= 3:
            try:
                pygame.draw.polygon(surface, color, vertices_pygame)
            except Exception as e:
                 print(f"Error drawing polygon with {len(vertices_pygame)} vertices: {e}")
        # else: Not enough vertices to draw a polygon

    def draw_portal(self, surface, color, vertices_pygame, angle_rad):
        """Draws a portal rectangle. (Basic version)."""
        if len(vertices_pygame) == 4:
            try:
                # Base rectangle fill
                pygame.draw.polygon(surface, color, vertices_pygame)
                # Outline (slightly darker or contrasting color?)
                outline_color = color.lerp(COLOR_TEXT, 0.5) # Mix portal color with text color
                pygame.draw.polygon(surface, outline_color, vertices_pygame, 2) # Thickness 2

                # TODO: Add subtle glow effect (e.g., draw larger blurred shape underneath)
                # TODO: Add particle effects if active state is tracked
                # TODO: Direction indicator could be a small animated chevron on exit event

            except Exception as e:
                print(f"Error drawing portal with vertices {vertices_pygame}: {e}")


    def _draw_grid(self, grid_size=50):
        """Draws a subtle background grid."""
        width, height = self.screen.get_size()
        # Draw vertical lines
        for x in range(0, width, grid_size):
            try:
                pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, height), 1)
            except Exception as e: print(f"Error drawing grid line: {e}")
        # Draw horizontal lines
        for y in range(0, height, grid_size):
            try:
                pygame.draw.line(self.screen, COLOR_GRID, (0, y), (width, y), 1)
            except Exception as e: print(f"Error drawing grid line: {e}")


    def _draw_hud(self, hud_info):
        """Draws the Heads-Up Display using the draw_text utility."""
        if not self.hud_font: return # Cannot draw HUD without font
        y_offset = 10
        x_pos = 10
        line_height = self.hud_font.get_height() + 2 # Add small spacing

        # FPS Counter
        fps_text = f"FPS: {hud_info.get('fps', 0):.0f}"
        draw_text(self.screen, fps_text, (x_pos, y_offset), self.hud_font, COLOR_TEXT)
        y_offset += line_height

        # Object Count
        obj_text = f"Objects: {hud_info.get('obj_count', 0)}"
        draw_text(self.screen, obj_text, (x_pos, y_offset), self.hud_font, COLOR_TEXT)
        y_offset += line_height

        # Portal Count (Individual portals)
        portal_text = f"Portals: {hud_info.get('portal_count', 0)}"
        draw_text(self.screen, portal_text, (x_pos, y_offset), self.hud_font, COLOR_TEXT)
        y_offset += line_height

        # Gravity Status
        grav_status = "ON" if hud_info.get('gravity_on', False) else "OFF"
        grav_text = f"Gravity: {grav_status}"
        draw_text(self.screen, grav_text, (x_pos, y_offset), self.hud_font, COLOR_TEXT)


    def _draw_physics_debug(self, world):
        """Draws Box2D physics shapes (wireframes) for debugging."""
        if not world: return
        try:
            for body in world.bodies:
                for fixture in body.fixtures:
                    shape = fixture.shape
                    # Use our safe is_sensor function
                    is_fixture_sensor = is_sensor(fixture)
                    draw_color = COLOR_DEBUG if not is_fixture_sensor else pygame.Color('cyan') # Sensors in cyan

                    # Convert body transform for drawing
                    transform = body.transform # b2Transform object
                    try:
                        if isinstance(shape, Box2D.b2PolygonShape):
                            vertices = [(transform * v) for v in shape.vertices]
                            vertices = [to_pygame(v) for v in vertices]
                            if len(vertices) >= 2: # Need at least 2 points for lines/polygon
                                pygame.draw.polygon(self.screen, draw_color, vertices, 1) # Wireframe only
                        elif isinstance(shape, Box2D.b2CircleShape):
                            center_world = transform * shape.pos # Center in world coords
                            center_pygame = to_pygame(center_world)
                            radius_pygame = scalar_to_pygame(shape.radius)
                            if radius_pygame > 0:
                                pygame.draw.circle(self.screen, draw_color, center_pygame, radius_pygame, 1) # Wireframe
                                # Draw line for orientation
                                angle = body.angle
                                end_point_world = center_world + Box2D.b2Vec2(shape.radius * math.cos(angle), shape.radius * math.sin(angle))
                                end_point_pygame = to_pygame(end_point_world)
                                pygame.draw.line(self.screen, draw_color, center_pygame, end_point_pygame, 1)

                        # TODO: Add drawing for Edge shapes, Chain shapes if used
                    except Exception as e:
                         # Don't halt all debug drawing for one shape error
                         # print(f"Warning: Error drawing debug shape for body: {e}")
                         pass # Continue to next fixture/body
        except Exception as e:
             print(f"Error iterating physics world bodies for debug draw: {e}")


    def _draw_debug_info(self, debug_info):
         """Draws dictionary of debug info as text lines."""
         if not self.debug_font: return # Cannot draw without font
         y = 30 # Start position slightly lower
         line_height = self.debug_font.get_height() + 2
         # Position debug info top-right or elsewhere as needed
         screen_width = self.screen.get_width()
         x_pos = screen_width - 260 # Adjust X based on expected text width

         for key, value in debug_info.items():
              text = f"{key}: {value}"
              draw_text(self.screen, text, (x_pos, y), self.debug_font, COLOR_DEBUG)
              y += line_height # Move down for the next line