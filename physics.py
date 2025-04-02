import Box2D
import math
from settings import (PPM, TIME_STEP, VELOCITY_ITERATIONS, POSITION_ITERATIONS,
                      GRAVITY, USER_DATA_OBJECT, USER_DATA_PORTAL, USER_DATA_WALL,
                      DEFAULT_PORTAL_WIDTH, DEFAULT_PORTAL_HEIGHT,
                      to_box2d)
from utils import is_sensor

class PortalContactListener(Box2D.b2ContactListener):
    """Listens for collisions, specifically involving portals."""
    def __init__(self, portal_manager):
        super(PortalContactListener, self).__init__()
        self.portal_manager = portal_manager

    def BeginContact(self, contact):
        fixture_a = contact.fixtureA
        fixture_b = contact.fixtureB
        body_a = fixture_a.body
        body_b = fixture_b.body

        user_data_a = body_a.userData if body_a.userData else {}
        user_data_b = body_b.userData if body_b.userData else {}

        portal = None
        obj = None
        portal_fixture = None
        obj_fixture = None

        if is_sensor(fixture_a) and user_data_a.get('type') == USER_DATA_PORTAL \
           and body_b.type == Box2D.b2_dynamicBody and user_data_b.get('type') == USER_DATA_OBJECT:
            portal = user_data_a.get('portal_instance')
            obj = user_data_b.get('object_instance')
            portal_fixture = fixture_a
            obj_fixture = fixture_b
        elif is_sensor(fixture_b) and user_data_b.get('type') == USER_DATA_PORTAL \
             and body_a.type == Box2D.b2_dynamicBody and user_data_a.get('type') == USER_DATA_OBJECT:
            portal = user_data_b.get('portal_instance')
            obj = user_data_a.get('object_instance')
            portal_fixture = fixture_b
            obj_fixture = fixture_a

        if portal and obj and portal.linked_portal and obj.body:
            portal_center_world = portal.body.worldCenter
            object_center_world = obj.body.worldCenter
            relative_pos = object_center_world - portal_center_world
            relative_vel = obj.body.GetLinearVelocityFromWorldPoint(object_center_world)

            dot_product = relative_pos.dot(relative_vel)

            if dot_product < 0.1:
                self.portal_manager.queue_teleportation(obj, portal)


class PhysicsManager:
    def __init__(self, object_manager, portal_manager):
        try:
            self.world = Box2D.b2World(gravity=GRAVITY, doSleep=True)
        except Exception as e:
             print(f"FATAL: Failed to create Box2D World: {e}")
             raise

        self.object_manager = object_manager
        self.portal_manager = portal_manager
        self.contact_listener = PortalContactListener(self.portal_manager)
        self.world.contactListener = self.contact_listener
        self.bodies_to_destroy = []

    def add_object(self, game_object):
        """Creates a Box2D body for a game object."""
        if not game_object: return None

        body_def = Box2D.b2BodyDef()
        body_def.type = Box2D.b2_dynamicBody
        body_def.position = game_object.position
        body_def.angle = game_object.angle
        body_def.userData = {'type': USER_DATA_OBJECT, 'object_instance': game_object}
        try:
            body = self.world.CreateBody(body_def)
        except Exception as e:
             print(f"Error creating Box2D body for object: {e}")
             return None

        shape = None
        if game_object.shape_type == 'circle':
            shape = Box2D.b2CircleShape(radius=game_object.radius)
        elif game_object.shape_type == 'box':
            shape = Box2D.b2PolygonShape(box=(game_object.size[0] / 2, game_object.size[1] / 2))

        if shape:
            try:
                fixture_def = Box2D.b2FixtureDef(
                    shape=shape,
                    density=1.0,
                    friction=0.3,
                    restitution=0.3
                )
                body.CreateFixture(fixture_def)
            except Exception as e:
                 print(f"Error creating Box2D fixture for object: {e}")
                 self.bodies_to_destroy.append(body)
                 return None

        game_object.body = body
        return body

    def add_portal(self, portal):
        """Creates a Box2D sensor body for a portal."""
        if not portal: return None

        body_def = Box2D.b2BodyDef()
        body_def.type = Box2D.b2_staticBody
        body_def.position = portal.position
        body_def.angle = portal.angle
        body_def.userData = {'type': USER_DATA_PORTAL, 'portal_instance': portal}
        try:
            body = self.world.CreateBody(body_def)
        except Exception as e:
             print(f"Error creating Box2D body for portal: {e}")
             return None

        try:
            shape = Box2D.b2PolygonShape(box=(portal.size[0] / 2, portal.size[1] / 2))
            fixture_def = Box2D.b2FixtureDef(shape=shape, isSensor=True)
            body.CreateFixture(fixture_def)
        except Exception as e:
            print(f"Error creating Box2D fixture for portal: {e}")
            self.bodies_to_destroy.append(body)
            return None

        portal.body = body
        return body

    def add_boundaries(self, width_m, height_m):
        """Creates static bodies for the screen edges."""
        wall_data = {'type': USER_DATA_WALL}
        boundary_thickness = 0.1
        try:
            self.world.CreateStaticBody(
                position=(width_m / 2, -boundary_thickness),
                shapes=Box2D.b2PolygonShape(box=(width_m / 2, boundary_thickness)),
                userData=wall_data
            )
            self.world.CreateStaticBody(
                position=(width_m / 2, height_m + boundary_thickness),
                shapes=Box2D.b2PolygonShape(box=(width_m / 2, boundary_thickness)),
                userData=wall_data
            )
            self.world.CreateStaticBody(
                position=(-boundary_thickness, height_m / 2),
                shapes=Box2D.b2PolygonShape(box=(boundary_thickness, height_m / 2)),
                userData=wall_data
            )
            self.world.CreateStaticBody(
                position=(width_m + boundary_thickness, height_m / 2),
                shapes=Box2D.b2PolygonShape(box=(boundary_thickness, height_m / 2)),
                userData=wall_data
            )
            if not hasattr(self.world, 'groundBody'):
                 self.world.groundBody = self.world.CreateStaticBody(position=(0, 0), userData={'type': 'ground_joint_anchor'})

        except Exception as e:
             print(f"Error creating boundaries: {e}")

    def update(self, dt):
        """Steps the physics world and processes pending actions."""
        destroyed_this_frame = 0
        bodies_remaining = []
        for body in self.bodies_to_destroy:
            try:
                body_found = False
                for world_body in self.world.bodies:
                     if world_body == body:
                          body_found = True
                          break
                if body_found:
                    self.world.DestroyBody(body)
                    destroyed_this_frame += 1
            except Exception as e:
                 pass
        self.bodies_to_destroy.clear()

        try:
            self.world.Step(TIME_STEP, VELOCITY_ITERATIONS, POSITION_ITERATIONS)
            self.world.ClearForces()
        except Exception as e:
             print(f"Error during Box2D world step: {e}")

        for obj in self.object_manager.get_objects():
            if obj and obj.body:
                obj.update_from_physics()

        self.portal_manager.process_teleportation_queue(self)

    def toggle_gravity(self):
        """Toggles gravity ON/OFF and wakes bodies."""
        current_gravity_y = self.world.gravity.y
        if abs(current_gravity_y) < 0.01:
            self.world.gravity = Box2D.b2Vec2(GRAVITY)
            print("Gravity ON")
            on = True
        else:
            self.world.gravity = Box2D.b2Vec2(0, 0)
            print("Gravity OFF")
            on = False
        for body in self.world.bodies:
            if body.type == Box2D.b2_dynamicBody:
                body.awake = True
        return on

    def apply_force_to_object(self, game_object, force_vector_pygame, point_pygame):
        """Applies force to an object's physics body in world coordinates."""
        if game_object and game_object.body:
            body = game_object.body
            force_vector_box2d = (force_vector_pygame[0] / PPM, -force_vector_pygame[1] / PPM)
            point_box2d = to_box2d(point_pygame)
            try:
                body.ApplyForce(force_vector_box2d, point_box2d, True)
            except Exception as e:
                 print(f"Error applying force: {e}")

    def apply_impulse_to_object(self, game_object, impulse_vector_pygame, point_pygame):
        """Applies impulse (mass * velocity change) to an object's physics body."""
        if game_object and game_object.body:
            body = game_object.body
            impulse_vector_box2d = (impulse_vector_pygame[0] / PPM, -impulse_vector_pygame[1] / PPM)
            point_box2d = to_box2d(point_pygame)
            try:
                body.ApplyLinearImpulse(impulse_vector_box2d, point_box2d, True)
            except Exception as e:
                 print(f"Error applying impulse: {e}")

    def move_body(self, body, new_pos_box2d, new_angle_rad):
        """Instantly moves a body using SetTransform - USE WITH CAUTION (esp. for teleport)."""
        if not body: return
        try:
            body.transform = (Box2D.b2Vec2(new_pos_box2d), new_angle_rad)
            body.linearVelocity = Box2D.b2Vec2(0,0)
            body.angularVelocity = 0.0
            body.awake = True
        except Exception as e:
             print(f"Error moving body with SetTransform: {e}")

    def get_body_at_pygame_point(self, point_pygame, include_sensors=False):
        """Finds a body (optionally sensor) whose fixture contains the given Pygame screen point."""
        try:
            point_box2d = to_box2d(point_pygame)
            
            if not isinstance(point_box2d, Box2D.b2Vec2):
                point_box2d = Box2D.b2Vec2(point_box2d[0], point_box2d[1])
            
            offset = 0.001
            lower_x = point_box2d.x - offset
            lower_y = point_box2d.y - offset
            upper_x = point_box2d.x + offset
            upper_y = point_box2d.y + offset
            
            aabb = Box2D.b2AABB(
                lowerBound=(lower_x, lower_y),
                upperBound=(upper_x, upper_y)
            )

            selected_game_object = None

            class PointQueryCallback(Box2D.b2QueryCallback):
                def __init__(self, point, include_sensors):
                    super(PointQueryCallback, self).__init__()
                    self.point = point
                    self.fixture = None
                    self.include_sensors = include_sensors

                def ReportFixture(self, fixture):
                    body = fixture.body
                    is_fixture_sensor = is_sensor(fixture)
                    if is_fixture_sensor and not self.include_sensors:
                         return True

                    if fixture.TestPoint(self.point):
                        self.fixture = fixture
                        return False
                    else:
                        return True

            query = PointQueryCallback(point_box2d, include_sensors)
            try:
                self.world.QueryAABB(query, aabb)
            except Exception as e:
                print(f"Error during QueryAABB: {e}")
                return None

            if query.fixture:
                body = query.fixture.body
                if body.userData and isinstance(body.userData, dict):
                     if body.userData.get('type') == USER_DATA_OBJECT:
                        selected_game_object = body.userData.get('object_instance')
                     elif body.userData.get('type') == USER_DATA_PORTAL and include_sensors:
                          selected_game_object = body.userData.get('portal_instance')

        except Exception as e:
            print(f"Error in get_body_at_pygame_point: {e}")
            return None
        
        return selected_game_object

    def destroy_body(self, body):
        """Safely schedule a body for destruction on the next physics step."""
        if body and body not in self.bodies_to_destroy:
             self.bodies_to_destroy.append(body)

    def get_gravity_state(self):
        """Returns True if gravity is ON, False otherwise."""
        return abs(self.world.gravity.y) > 0.01