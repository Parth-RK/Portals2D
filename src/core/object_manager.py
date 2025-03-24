from src.game_objects.game_object import GameObject
from src.game_objects.portal import Portal
from src.utils.logger import Logger
import math

class ObjectManager:
    def __init__(self):
        self.logger = Logger()
        self.objects = []
        self.portals = {}  # Dictionary of portals by ID
        # Portal pairs: color -> [portal1, portal2]
        self.portal_pairs = {}
        self.logger.info("Object manager initialized")
        
    def create_object(self, obj_type, x, y, ui_manager=None):
        """Create a new game object of specified type."""
        new_obj = GameObject(obj_type, x, y)
        
        # Set object color based on current theme if UI manager is provided
        if ui_manager:
            if obj_type == "BOX":
                new_obj.color = ui_manager.get_box_color()
            elif obj_type == "CIRCLE":
                new_obj.color = ui_manager.get_circle_color()
        
        self.objects.append(new_obj)
        self.logger.info(f"Created {obj_type} object at ({x}, {y})")
        return new_obj
        
    def create_portal(self, color, portal_id, x, y, angle, ui_manager=None):
        """Create a portal with the specified color and ID or update an existing one."""
        full_id = f"{color}_{portal_id}"
        
        if full_id in self.portals:
            # Update existing portal
            self.portals[full_id].set_position(x, y)
            self.portals[full_id].set_angle(angle)
            self.logger.info(f"Updated {full_id} portal at ({x}, {y}) with angle {angle}")
        else:
            # Create new portal
            new_portal = Portal(full_id, color, x, y, angle)
            # Apply theme tint if UI manager is provided
            if ui_manager:
                new_portal.apply_tint(ui_manager.get_portal_tint())
                
            self.portals[full_id] = new_portal
            
            # Set up portal pairs
            if color not in self.portal_pairs:
                self.portal_pairs[color] = []
            
            self.portal_pairs[color].append(new_portal)
            
            # If we have a pair, link them
            if len(self.portal_pairs[color]) == 2:
                self.portal_pairs[color][0].link_portal(self.portal_pairs[color][1])
                self.portal_pairs[color][1].link_portal(self.portal_pairs[color][0])
                self.logger.info(f"Linked {color} portal pair")
            
            self.logger.info(f"Created {full_id} portal at ({x}, {y}) with angle {angle}")
            
        return self.portals[full_id]
        
    def remove_object(self, game_object):
        """Remove an object from the manager."""
        if isinstance(game_object, str):
            # Find object by ID
            for obj in self.objects[:]:
                if obj.id == game_object:
                    self.objects.remove(obj)
                    self.logger.info(f"Removed object {obj.id}")
                    return
        elif game_object in self.objects:
            self.objects.remove(game_object)
            self.logger.info(f"Removed object {game_object.id}")
            
    def remove_portal(self, portal_id):
        """Remove a portal by ID."""
        if portal_id in self.portals:
            portal = self.portals[portal_id]
            color = portal.color_name  # Use color_name we added in Portal class
            
            # Remove from portal pairs
            if color in self.portal_pairs:
                if portal in self.portal_pairs[color]:
                    self.portal_pairs[color].remove(portal)
                
            # Unlink any linked portals
            if portal.linked_portal:
                portal.linked_portal.unlink_portal()
                
            del self.portals[portal_id]
            self.logger.info(f"Removed {portal_id} portal")
            
    def get_objects(self):
        """Return all managed objects."""
        return self.objects
        
    def get_portals(self):
        """Return all managed portals."""
        return list(self.portals.values())
        
    def get_object_at_position(self, x, y):
        """Find object at the given position."""
        for obj in self.objects:
            if obj.obj_type == "CIRCLE":
                # Check if position is within circle
                dx = obj.position.x - x
                dy = obj.position.y - y
                if (dx * dx + dy * dy) <= (obj.radius * obj.radius):
                    return obj
            else:
                # Check if position is within rotated box
                # Transform point to object's local space
                dx = x - obj.position.x
                dy = y - obj.position.y
                
                # Rotate point
                cos_angle = math.cos(-obj.angle)
                sin_angle = math.sin(-obj.angle)
                rx = dx * cos_angle - dy * sin_angle
                ry = dx * sin_angle + dy * cos_angle
                
                # Check if point is inside the box
                if (abs(rx) <= obj.width / 2) and (abs(ry) <= obj.height / 2):
                    return obj
        
        # If no object found, check portals
        for portal in self.portals.values():
            # Transform point to portal's local space
            dx = x - portal.position.x
            dy = y - portal.position.y
            
            # Rotate point
            cos_angle = math.cos(-portal.angle)
            sin_angle = math.sin(-portal.angle)
            rx = dx * cos_angle - dy * sin_angle
            ry = dx * sin_angle + dy * cos_angle
            
            # Check if point is inside the portal
            if (abs(rx) <= portal.width / 2) and (abs(ry) <= portal.height / 2):
                return portal
                
        return None
    
    def move_object_to(self, obj_id, x, y):
        """Move an object to a specified position."""
        # Check if it's a regular object
        for obj in self.objects:
            if obj.id == obj_id:
                obj.set_position(x, y)
                return True
        
        # Check if it's a portal
        for portal in self.portals.values():
            if portal.id == obj_id:
                portal.set_position(x, y)
                return True
                
        return False
    
    def set_object_velocity(self, obj_id, vx, vy):
        """Set the velocity of an object."""
        for obj in self.objects:
            if obj.id == obj_id:
                obj.set_velocity(vx, vy)
                return True
        return False
    
    def resize_object(self, obj_id, scale):
        """Resize an object by a scale factor."""
        # Try regular objects first
        for obj in self.objects:
            if obj.id == obj_id:
                if obj.obj_type == "CIRCLE":
                    obj.radius *= scale
                else:
                    obj.width *= scale
                    obj.height *= scale
                # Recreate physics body after resize
                if obj.body:
                    obj.body.userData = {"needs_rebuild": True}
                return True
        
        # Try portals
        for portal in self.portals.values():
            if portal.id == obj_id:
                portal.resize(scale)
                return True
                
        return False
    
    def rotate_object(self, obj_id, angle_degrees):
        """Rotate an object to the specified angle in degrees."""
        # Try regular objects
        for obj in self.objects:
            if obj.id == obj_id:
                current_angle = obj.angle
                new_angle = current_angle + math.radians(angle_degrees)
                obj.set_angle(new_angle)
                return True
                
        # Try portals
        for portal in self.portals.values():
            if portal.id == obj_id:
                current_angle = portal.angle
                new_angle = current_angle + math.radians(angle_degrees)
                portal.set_angle(new_angle)
                return True
                
        return False
        
    def update_object_colors(self, ui_manager):
        """Update colors of all objects based on the current theme."""
        # Update regular objects
        for obj in self.objects:
            if obj.obj_type == "BOX":
                obj.color = ui_manager.get_box_color()
            elif obj.obj_type == "CIRCLE":
                obj.color = ui_manager.get_circle_color()
                
        # Update portal colors
        portal_tint = ui_manager.get_portal_tint()
        for portal in self.portals.values():
            portal.apply_tint(portal_tint)
            
        self.logger.info("Updated object colors for theme change")
        
    def update(self, dt):
        """Update all managed objects."""
        # Update game objects
        for obj in self.objects[:]:  # Use a copy to safely remove while iterating
            obj.update(dt)
            
            # Check for objects that should be removed (e.g., out of bounds)
            if obj.should_remove():
                self.remove_object(obj)
                
        # Update portals
        for portal in list(self.portals.values()):
            portal.update(dt)
            
        # Check for portal interactions
        for obj in self.objects:
            for portal in self.portals.values():
                if portal.is_linked() and portal.check_collision(obj):
                    portal.teleport_object(obj)
