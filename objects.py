import pygame
import Box2D # For b2Vec2
import math
from settings import (PPM, to_pygame, to_box2d, scalar_to_pygame, scalar_to_box2d,
                      COLOR_CIRCLE, COLOR_SQUARE, COLOR_TRIANGLE,
                      DEFAULT_CIRCLE_RADIUS, DEFAULT_BOX_SIZE,
                      COLOR_BACKGROUND) # Add COLOR_TRIANGLE
from utils import get_body_vertices_pygame

class GameObject:
    """Base class for objects in the game."""
    _id_counter = 0
    def __init__(self, shape_type, position_box2d, angle_rad=0.0, color=pygame.Color("gray")):
        self.id = GameObject._id_counter
        GameObject._id_counter += 1
        self.shape_type = shape_type
        self.position = Box2D.b2Vec2(position_box2d)
        self.angle = angle_rad
        self.color = color
        self.body = None
        self.teleporting = False
        self.marked_for_deletion = False

    def update_from_physics(self):
        """Updates position and angle based on the physics body."""
        if self.body and not self.marked_for_deletion:
            self.position = self.body.position
            self.angle = self.body.angle
        else:
            pass

    def draw(self, surface, renderer):
        """Placeholder draw method - subclasses should implement."""
        if self.body and not self.marked_for_deletion and not self.teleporting:
            pos_pygame = to_pygame(self.position)
            pygame.draw.circle(surface, self.color, pos_pygame, 5)

    def get_pygame_pos(self):
        """Returns the center position in Pygame coordinates."""
        return to_pygame(self.position)

    def schedule_deletion(self):
        """Marks the object for deletion and tells physics manager to remove body."""
        self.marked_for_deletion = True
        if self.body:
             pass

class Circle(GameObject):
    def __init__(self, position_box2d, radius=DEFAULT_CIRCLE_RADIUS, color=COLOR_CIRCLE, angle_rad=0.0):
        super().__init__('circle', position_box2d, angle_rad, color)
        self.radius = radius

    def draw(self, surface, renderer):
        if self.body and not self.marked_for_deletion and not self.teleporting:
            pos_pygame = to_pygame(self.position)
            radius_pygame = scalar_to_pygame(self.radius)
            renderer.draw_circle(surface, self.color, pos_pygame, radius_pygame, self.angle)

class Box(GameObject):
    def __init__(self, position_box2d, size=DEFAULT_BOX_SIZE, color=COLOR_SQUARE, angle_rad=0.0):
        super().__init__('box', position_box2d, angle_rad, color)
        self.size = size

    def draw(self, surface, renderer):
        if self.body and not self.marked_for_deletion and not self.teleporting:
            vertices_pygame = get_body_vertices_pygame(self.body)
            if vertices_pygame:
                 renderer.draw_polygon(surface, self.color, vertices_pygame)
            else:
                 pos_pygame = to_pygame(self.position)
                 size_pygame = (scalar_to_pygame(self.size[0]), scalar_to_pygame(self.size[1]))
                 pygame.draw.rect(surface, self.color, (*pos_pygame, *size_pygame))


class ObjectManager:
    def __init__(self, physics_manager):
        self.objects = []
        self.physics_manager = physics_manager
        self.selected_object = None
        self.mouse_joint = None
        
    def set_physics_manager(self, manager):
         """Allows setting physics manager after initialization if needed."""
         self.physics_manager = manager

    def create_object(self, obj_type, position_pygame, angle_rad=0.0):
        """Creates, adds to list, and creates physics body for a new game object."""
        if not self.physics_manager:
             print("Error: PhysicsManager not set in ObjectManager.")
             return None

        position_box2d = to_box2d(position_pygame)
        obj = None
        if obj_type == 'circle':
            obj = Circle(position_box2d, angle_rad=angle_rad)
        elif obj_type == 'box':
             obj = Box(position_box2d, angle_rad=angle_rad)

        if obj:
            self.objects.append(obj)
            body_created = self.physics_manager.add_object(obj)
            if not body_created:
                 print(f"Warning: Failed to create physics body for new {obj_type}. Removing object.")
                 self.objects.remove(obj)
                 return None
        return obj

    def delete_object(self, game_object):
        """Schedules an object and its physics body for deletion."""
        if game_object and game_object in self.objects and not game_object.marked_for_deletion:
            game_object.schedule_deletion()
            if game_object.body:
                self.physics_manager.destroy_body(game_object.body)

            if self.selected_object == game_object:
                self.stop_drag()

    def cleanup_deleted_objects(self):
        """Removes objects marked for deletion from the main list."""
        live_objects = [obj for obj in self.objects if not obj.marked_for_deletion]
        deleted_count = len(self.objects) - len(live_objects)
        if deleted_count > 0:
            pass
        self.objects = live_objects

    def get_object_at(self, pos_pygame):
        """Finds a dynamic object at Pygame coordinates using physics query."""
        if not self.physics_manager: return None
        found = self.physics_manager.get_body_at_pygame_point(pos_pygame, include_sensors=False)
        if isinstance(found, GameObject):
             return found
        return None

    def start_drag(self, game_object, mouse_pos_pygame):
        """Initiates dragging of an object using a Box2D mouse joint."""
        if not self.physics_manager or not self.physics_manager.world: return
        if game_object and game_object.body and not self.mouse_joint:
            body = game_object.body
            if body.type != Box2D.b2_dynamicBody:
                 print("Warning: Attempted to drag a non-dynamic body.")
                 return
            body.awake = True

            ground_body = getattr(self.physics_manager.world, 'groundBody', None)
            if not ground_body:
                 print("Warning: No groundBody found in world for mouse joint. Creating one.")
                 ground_body = self.physics_manager.world.CreateStaticBody(position=(0,0))
                 self.physics_manager.world.groundBody = ground_body

            mouse_pos_box2d = to_box2d(mouse_pos_pygame)

            try:
                joint_def = Box2D.b2MouseJointDef(
                    bodyA=ground_body,
                    bodyB=body,
                    target=mouse_pos_box2d,
                    maxForce=1000.0 * body.mass,
                    frequencyHz=5.0,
                    dampingRatio=0.7
                )
                self.mouse_joint = self.physics_manager.world.CreateJoint(joint_def)
                self.selected_object = game_object
                print(f"Dragging Obj {game_object.id}")
            except Exception as e:
                 print(f"Error creating mouse joint: {e}")
                 self.mouse_joint = None
                 self.selected_object = None

    def update_drag(self, mouse_pos_pygame):
        """Updates the target of the active mouse joint."""
        if self.mouse_joint:
            mouse_pos_box2d = to_box2d(mouse_pos_pygame)
            try:
                self.mouse_joint.target = mouse_pos_box2d
            except Exception as e:
                 print(f"Error updating mouse joint target: {e}")

    def stop_drag(self, apply_throw=False, mouse_vel_pygame=(0,0)):
        """Stops dragging, destroys the mouse joint, optionally applies throw impulse."""
        if not self.physics_manager or not self.mouse_joint:
             self.selected_object = None
             return

        try:
            self.physics_manager.world.DestroyJoint(self.mouse_joint)
            print(f"Stopped dragging Obj {self.selected_object.id if self.selected_object else 'None'}")
        except Exception as e:
            print(f"Warning: Error destroying mouse joint: {e}")

        current_dragged_object = self.selected_object
        self.mouse_joint = None
        self.selected_object = None

        if apply_throw and current_dragged_object and current_dragged_object.body:
            mass = current_dragged_object.body.mass
            throw_factor = 0.1
            impulse_pygame_x = mouse_vel_pygame[0] * throw_factor * mass
            impulse_pygame_y = mouse_vel_pygame[1] * throw_factor * mass
            throw_impulse_pygame = (impulse_pygame_x, impulse_pygame_y)

            if abs(throw_impulse_pygame[0]) > 0.1 or abs(throw_impulse_pygame[1]) > 0.1:
                 mouse_pos_pygame = pygame.mouse.get_pos()
                 center_pygame = current_dragged_object.get_pygame_pos()
                 self.physics_manager.apply_impulse_to_object(
                      current_dragged_object,
                      throw_impulse_pygame,
                      center_pygame
                 )

    def update(self, dt):
        """Called each frame. Handle object state updates not covered by physics."""
        self.cleanup_deleted_objects()

    def get_objects(self):
         """Returns a copy of the objects list for safe iteration."""
         return list(self.objects)

    def get_count(self):
         return len(self.objects)