from src.game_objects.game_object import GameObject
from src.game_objects.portal import Portal
from src.utils.logger import Logger

class ObjectManager:
    def __init__(self):
        self.logger = Logger()
        self.objects = []
        self.portals = {}  # Dictionary of portals by ID
        self.logger.info("Object manager initialized")
        
    def create_object(self, obj_type, x, y):
        """Create a new game object of specified type."""
        new_obj = GameObject(obj_type, x, y)
        self.objects.append(new_obj)
        self.logger.info(f"Created {obj_type} object at ({x}, {y})")
        return new_obj
        
    def create_portal(self, portal_id, x, y, angle):
        """Create a portal with the specified ID or update an existing one."""
        if portal_id in self.portals:
            # Update existing portal
            self.portals[portal_id].set_position(x, y)
            self.portals[portal_id].set_angle(angle)
            self.logger.info(f"Updated {portal_id} portal at ({x}, {y}) with angle {angle}")
        else:
            # Create new portal
            new_portal = Portal(portal_id, x, y, angle)
            self.portals[portal_id] = new_portal
            self.logger.info(f"Created {portal_id} portal at ({x}, {y}) with angle {angle}")
            
        # Link blue and orange portals if both exist
        if "BLUE" in self.portals and "ORANGE" in self.portals:
            self.portals["BLUE"].link_portal(self.portals["ORANGE"])
            self.portals["ORANGE"].link_portal(self.portals["BLUE"])
            self.logger.info("Linked blue and orange portals")
            
        return self.portals[portal_id]
        
    def remove_object(self, game_object):
        """Remove an object from the manager."""
        if game_object in self.objects:
            self.objects.remove(game_object)
            self.logger.info(f"Removed object {game_object.id}")
            
    def remove_portal(self, portal_id):
        """Remove a portal by ID."""
        if portal_id in self.portals:
            del self.portals[portal_id]
            self.logger.info(f"Removed {portal_id} portal")
            
    def get_objects(self):
        """Return all managed objects."""
        return self.objects
        
    def get_portals(self):
        """Return all managed portals."""
        return self.portals.values()
        
    def update(self, dt):
        """Update all managed objects."""
        # Update game objects
        for obj in self.objects[:]:  # Use a copy to safely remove while iterating
            obj.update(dt)
            
            # Check for objects that should be removed (e.g., out of bounds)
            if obj.should_remove():
                self.remove_object(obj)
                
        # Update portals
        for portal in self.portals.values():
            portal.update(dt)
            
        # Check for portal interactions
        for obj in self.objects:
            for portal in self.portals.values():
                if portal.is_linked() and portal.check_collision(obj):
                    portal.teleport_object(obj)
