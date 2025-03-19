import Box2D
from Box2D import b2World, b2Vec2, b2PolygonShape, b2CircleShape, b2BodyDef, b2_dynamicBody, b2_staticBody
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
        
        # Create shape based on object type
        if game_object.obj_type == "CIRCLE":
            shape = b2CircleShape(radius=game_object.radius)
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
        body_def = b2BodyDef()
        body_def.position = (portal.position.x, portal.position.y)
        body_def.angle = portal.angle
        body = self.world.CreateBody(body_def)
        
        # Create a rectangular sensor
        shape = b2PolygonShape()
        shape.SetAsBox(portal.width / 2, portal.height / 2)
        fixture = body.CreateFixture(shape=shape, isSensor=True)
        
        # Attach sensor to portal
        portal.sensor = body
        
        self.logger.info(f"Created sensor for portal {portal.id}")
        
    def toggle_gravity(self):
        """Toggle gravity on/off."""
        self.gravity_on = not self.gravity_on
        if self.gravity_on:
            self.world.gravity = b2Vec2(0, 10)
            self.logger.info("Gravity turned ON")
        else:
            self.world.gravity = b2Vec2(0, 0)
            self.logger.info("Gravity turned OFF")
        
    def update(self, dt):
        """Update physics world and sync with game objects."""
        # Create physics bodies for new objects
        for obj in self.object_manager.get_objects():
            if not obj.body:
                self.create_physics_body(obj)
                
        # Create sensors for new portals
        for portal in self.object_manager.get_portals():
            if not portal.sensor:
                self.create_portal_sensor(portal)
                
        # Step the physics simulation
        self.world.Step(dt, 8, 3)
        self.world.ClearForces()
