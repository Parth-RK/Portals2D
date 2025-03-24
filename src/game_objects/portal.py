import math
from Box2D import b2Vec2
import pygame

class Portal:
    def __init__(self, portal_id, color, x, y, angle):
        self.id = portal_id
        self.color_name = color  # Store the color name (e.g., "BLUE")
        self.position = b2Vec2(x, y)
        self.angle = angle
        self.width = 10
        self.height = 50
        self.linked_portal = None
        self.sensor = None  # Will be set by physics engine
        
        # Set display color based on portal type
        self.set_color_by_type(color)
        
        # Store base color for theme adjustments
        self.base_color = self.color
            
        # Object cache for preventing immediate re-entry
        self.recently_teleported = set()
        self.teleport_cooldown = 0.5  # seconds
        self.cooldown_timers = {}
    
    def set_color_by_type(self, color):
        """Set the display color based on portal color name."""
        color_map = {
            "BLUE": (0, 100, 255),     # Blue
            "ORANGE": (255, 165, 0),   # Orange
            "GREEN": (0, 255, 0),      # Green
            "PURPLE": (128, 0, 128),   # Purple
            "YELLOW": (255, 255, 0),   # Yellow
            "CYAN": (0, 255, 255),     # Cyan
            "MAGENTA": (255, 0, 255),  # Magenta
        }
        # Store the RGB color value in self.color for rendering
        self.color = color_map.get(color, (128, 128, 128))  # Default gray
        # Also store the base color for theme adjustments
        self.base_color = self.color
        
    def apply_tint(self, tint_factor):
        """Apply a tint factor to adjust portal color based on theme."""
        r = min(255, int(self.base_color[0] * tint_factor))
        g = min(255, int(self.base_color[1] * tint_factor))
        b = min(255, int(self.base_color[2] * tint_factor))
        self.color = (r, g, b)
            
    def link_portal(self, other_portal):
        """Link this portal with another portal."""
        self.linked_portal = other_portal
        
    def unlink_portal(self):
        """Remove any portal linking."""
        self.linked_portal = None
        
    def is_linked(self):
        """Check if this portal is linked to another."""
        return self.linked_portal is not None
        
    def set_position(self, x, y):
        """Set the portal's position."""
        self.position = b2Vec2(x, y)
        if self.sensor:
            self.sensor.position = self.position
            
    def set_angle(self, angle):
        """Set the portal's angle."""
        self.angle = angle
        if self.sensor:
            self.sensor.angle = angle
            
    def check_collision(self, game_object):
        """Check if an object is colliding with this portal."""
        if not self.sensor or not game_object.body or game_object.id in self.recently_teleported:
            return False
            
        # Check for collision between object and portal sensor
        for contact_edge in game_object.body.contacts:
            contact = contact_edge.contact
            if (contact.fixtureA.body == self.sensor or contact.fixtureB.body == self.sensor) and contact.touching:
                return True
                
        return False
        
    def teleport_object(self, game_object):
        """Teleport an object to the linked portal's position."""
        if not self.is_linked() or game_object.id in self.recently_teleported:
            return False
            
        # Calculate position offset relative to this portal
        local_pos = game_object.position - self.position
        
        # Rotate the local position by the difference in portal angles
        angle_diff = self.linked_portal.angle - self.angle + math.pi  # Add pi to flip the direction
        cos_angle = math.cos(angle_diff)
        sin_angle = math.sin(angle_diff)
        rotated_x = local_pos.x * cos_angle - local_pos.y * sin_angle
        rotated_y = local_pos.x * sin_angle + local_pos.y * cos_angle
        
        # Calculate new position relative to linked portal
        new_position = self.linked_portal.position + b2Vec2(rotated_x, rotated_y)
        
        # Transform velocity
        vel_mag = game_object.velocity.length
        if vel_mag > 0:
            # Normalize velocity
            normalized = b2Vec2(game_object.velocity.x / vel_mag, game_object.velocity.y / vel_mag)
            
            # Rotate normalized velocity
            rotated_vx = normalized.x * cos_angle - normalized.y * sin_angle
            rotated_vy = normalized.x * sin_angle + normalized.y * cos_angle
            
            # Scale velocity (can add a boost factor here if desired)
            boost_factor = 1.0  # No boost by default
            new_velocity = b2Vec2(rotated_vx * vel_mag * boost_factor, rotated_vy * vel_mag * boost_factor)
            game_object.set_velocity(new_velocity.x, new_velocity.y)
        
        # Set new position
        game_object.set_position(new_position.x, new_position.y)
        
        # Set new angle
        new_angle = game_object.angle + angle_diff
        game_object.set_angle(new_angle)
        
        # Add to recently teleported list to prevent immediate re-entry
        self.recently_teleported.add(game_object.id)
        self.cooldown_timers[game_object.id] = self.teleport_cooldown
        
        return True
        
    def update(self, dt):
        """Update portal state."""
        # Update cooldown timers
        keys_to_remove = []
        for obj_id, timer in list(self.cooldown_timers.items()):
            self.cooldown_timers[obj_id] -= dt
            if self.cooldown_timers[obj_id] <= 0:
                keys_to_remove.append(obj_id)
                
        # Remove expired cooldowns
        for obj_id in keys_to_remove:
            if obj_id in self.recently_teleported:
                self.recently_teleported.remove(obj_id)
            del self.cooldown_timers[obj_id]
            
    def resize(self, scale):
        """Resize the portal."""
        self.width *= scale
        self.height *= scale
        # Recreate the sensor in physics engine
        if self.sensor:
            self.sensor.userData = {"needs_rebuild": True}
        return True
