import Box2D
from Box2D import b2World, b2Vec2, b2PolygonShape, b2CircleShape, b2BodyDef, b2_dynamicBody, b2_staticBody, b2_kinematicBody
from src.utils.logger import Logger

class PhysicsEngine:
    def __init__(self, object_manager):
        self.logger = Logger()
        self.object_manager = object_manager
        
        # Create Box2D world with default gravity
        self.gravity_on = True
        self.world = b2World(gravity=(0, 10), doSleep=True)
        
        # Ground body (bottom of the screen)
        ground_def = b2BodyDef()
        ground_def.position = (640, 710)
        self.ground_body = self.world.CreateBody(ground_def)
        ground_shape = b2PolygonShape()
        ground_shape.SetAsBox(640, 10)  # 1280x20 rectangle
        self.ground_fixture = self.ground_body.CreateFixture(shape=ground_shape, friction=0.3)
        
        # Create walls
        self.create_wall(0, 360, 10, 360)     # Left wall
        self.create_wall(1280, 360, 10, 360)  # Right wall
        self.create_wall(640, 0, 640, 10)     # Top wall
        
        self.logger.info("Physics engine initialized")
        
    def create_wall(self, x, y, half_width, half_height):
        """Create a static wall body."""
        wall_def = b2BodyDef()
        wall_def.position = (x, y)
        wall_body = self.world.CreateBody(wall_def)
        wall_shape = b2PolygonShape()
        wall_shape.SetAsBox(half_width, half_height)
        wall_fixture = wall_body.CreateFixture(shape=wall_shape, friction=0.3)
        
    def create_physics_body(self, game_object):
        """Create a physics body for a game object."""
        # Create body definition
        body_def = b2BodyDef()
        body_def.type = b2_dynamicBody
        body_def.position = (game_object.position.x, game_object.position.y)
        body_def.angle = game_object.angle
        body = self.world.CreateBody(body_def)
        
        # Store reference to the game object for collision detection
        body.userData = game_object
        
        # Create shape based on object type
        if game_object.obj_type == "CIRCLE":
            shape = b2CircleShape(radius=game_object.radius)
            fixture = body.CreateFixture(shape=shape, density=1.0, friction=0.3)
        elif game_object.obj_type == "TRIANGLE":
            # Create a triangular shape using polygon
            height = game_object.side_length * 0.866  # sqrt(3)/2
            vertices = [
                (0, -height/2),  # top
                (-game_object.side_length/2, height/2),  # bottom left
                (game_object.side_length/2, height/2)  # bottom right
            ]
            shape = b2PolygonShape(vertices=vertices)
            fixture = body.CreateFixture(shape=shape, density=1.0, friction=0.3)
        else:  # BOX or default
            shape = b2PolygonShape()
            shape.SetAsBox(game_object.width / 2, game_object.height / 2)
            fixture = body.CreateFixture(shape=shape, density=1.0, friction=0.3)
        
        # Attach physics body to game object
        game_object.body = body
        game_object.fixture = fixture
        
        self.logger.info(f"Created physics body for object {game_object.id}")
        
    def create_portal_sensor(self, portal):
        """Create a sensor for portal detection."""
        # If the portal already has a body, destroy it first
        if portal.sensor:
            if hasattr(portal.sensor, "userData") and portal.sensor.userData and portal.sensor.userData.get("needs_rebuild", False):
                self.world.DestroyBody(portal.sensor)
            else:
                return  # Sensor already exists and doesn't need rebuild
        
        body_def = b2BodyDef()
        body_def.position = (portal.position.x, portal.position.y)
        body_def.angle = portal.angle
        body = self.world.CreateBody(body_def)
        
        # Store reference to the portal for collision detection
        body.userData = portal
        
        # Create a rectangular sensor
        shape = b2PolygonShape()
        shape.SetAsBox(portal.width / 2, portal.height / 2)
        fixture = body.CreateFixture(shape=shape, isSensor=True)
        fixture.userData = "portal_sensor"  # Tag the fixture for identification
        
        # Attach sensor to portal
        portal.sensor = body
        
        self.logger.info(f"Created sensor for portal {portal.id}")
        
    def toggle_gravity(self):
        """Toggle gravity on/off."""
        self.gravity_on = not self.gravity_on
        if self.gravity_on:
            self.world.gravity = b2Vec2(0, 10)
            
            # Wake up all sleeping bodies when gravity is re-enabled
            for obj in self.object_manager.get_objects():
                if obj.body and obj.body.type == b2_dynamicBody:
                    obj.body.awake = True
                    
            self.logger.info("Gravity turned ON")
        else:
            self.world.gravity = b2Vec2(0, 0)
            self.logger.info("Gravity turned OFF")
        
    def set_object_kinematic(self, obj_id, is_kinematic):
        """Set whether an object should be kinematic (moved by game code) or dynamic (moved by physics)."""
        for obj in self.object_manager.get_objects():
            if obj.id == obj_id and obj.body:
                if is_kinematic:
                    # Make kinematic
                    obj.body.type = b2_kinematicBody
                else:
                    # Make dynamic
                    obj.body.type = b2_dynamicBody
                return True
        return False
    
    def update(self, dt):
        """Update physics world and sync with game objects."""
        # Create physics bodies for new objects
        for obj in self.object_manager.get_objects():
            if not obj.body:
                self.create_physics_body(obj)
            elif hasattr(obj.body, 'userData') and obj.body.userData and isinstance(obj.body.userData, dict) and obj.body.userData.get('needs_rebuild', False):
                # Recreate body if needed (e.g., after resizing)
                self.world.DestroyBody(obj.body)
                self.create_physics_body(obj)
                
        # Create sensors for portals
        for portal in self.object_manager.get_portals():
            if not portal.sensor or (hasattr(portal.sensor, 'userData') and isinstance(portal.sensor.userData, dict) and portal.sensor.userData.get('needs_rebuild', False)):
                self.create_portal_sensor(portal)
        
        # Wake up objects when they're interacted with
        if self.gravity_on:
            for obj in self.object_manager.get_objects():
                if obj.body and obj.body.type == b2_dynamicBody and obj.body.linearVelocity.lengthSquared < 0.01:
                    # If object is nearly stationary, ensure it's awake to respond to gravity
                    obj.body.awake = True
                
        # Step the physics simulation
        self.world.Step(dt, 8, 3)
        self.world.ClearForces()
        
        # Check for portal collisions after physics step
        for obj in self.object_manager.get_objects():
            for portal in self.object_manager.get_portals():
                if portal.is_linked() and portal.check_collision(obj):
                    portal.teleport_object(obj)
