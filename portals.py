import pygame
import math
from settings import (Box2D, to_pygame, to_box2d, scalar_to_pygame,
                      PORTAL_COLORS, DEFAULT_PORTAL_HEIGHT, DEFAULT_PORTAL_WIDTH,
                      PORTAL_COOLDOWN)
from utils import get_body_vertices_pygame

class Portal:
    """Represents one end of a portal pair."""
    _id_counter = 0
    def __init__(self, position_box2d, angle_rad, color, pair_id):
        self.id = Portal._id_counter
        Portal._id_counter += 1
        self.position = Box2D.b2Vec2(position_box2d)
        self.angle = angle_rad
        self.color = color
        self.pair_id = pair_id
        self.body = None
        self.linked_portal = None
        self.size = (DEFAULT_PORTAL_WIDTH, DEFAULT_PORTAL_HEIGHT)
        self.marked_for_deletion = False

        self.cooldown_end_times = {}
        self.cooldown_duration = PORTAL_COOLDOWN

    def link(self, other_portal):
        """Establish a two-way link between portals."""
        if isinstance(other_portal, Portal):
            self.linked_portal = other_portal
            other_portal.linked_portal = self

    def get_pygame_pos(self):
        """Get center position in Pygame coordinates."""
        return to_pygame(self.position)

    def get_exit_transform(self, entry_obj_body):
        """Calculate exit position, angle, linear and angular velocity for an entering object body."""
        if not self.linked_portal or not entry_obj_body:
            print("Warning: get_exit_transform called without linked portal or body.")
            return entry_obj_body.position, entry_obj_body.angle, entry_obj_body.linearVelocity, entry_obj_body.angularVelocity

        exit_portal = self.linked_portal

        relative_pos = entry_obj_body.worldCenter - self.body.worldCenter
        relative_angle = exit_portal.angle - self.angle + math.pi

        cos_a = math.cos(relative_angle)
        sin_a = math.sin(relative_angle)
        rotated_relative_pos_x = relative_pos.x * cos_a - relative_pos.y * sin_a
        rotated_relative_pos_y = relative_pos.x * sin_a + relative_pos.y * cos_a
        rotated_relative_pos = Box2D.b2Vec2(rotated_relative_pos_x, rotated_relative_pos_y)

        exit_position = exit_portal.body.worldCenter + rotated_relative_pos

        exit_angle = entry_obj_body.angle + relative_angle

        entry_vel = entry_obj_body.linearVelocity
        exit_vel_x = entry_vel.x * cos_a - entry_vel.y * sin_a
        exit_vel_y = entry_vel.x * sin_a + entry_vel.y * cos_a
        exit_velocity = Box2D.b2Vec2(exit_vel_x, exit_vel_y)

        exit_angular_velocity = entry_obj_body.angularVelocity

        exit_normal = exit_portal.body.GetWorldVector((0, 1))
        safety_offset_distance = 0.05
        exit_position += exit_normal * safety_offset_distance

        return exit_position, exit_angle, exit_velocity, exit_angular_velocity

    def draw(self, surface, renderer):
        """Draw the portal using the renderer."""
        if self.body and not self.marked_for_deletion:
             vertices_pygame = get_body_vertices_pygame(self.body)
             if vertices_pygame:
                 renderer.draw_portal(surface, self.color, vertices_pygame, self.angle)
             else:
                 pos_pygame = self.get_pygame_pos()
                 size_pygame = (scalar_to_pygame(self.size[0]), scalar_to_pygame(self.size[1]))
                 pygame.draw.rect(surface, self.color, (*pos_pygame, *size_pygame), 2)

    def update_cooldowns(self, current_time):
        """Remove expired cooldown entries."""
        keys_to_remove = [obj_id for obj_id, end_time in self.cooldown_end_times.items() if current_time >= end_time]
        for key in keys_to_remove:
            del self.cooldown_end_times[key]

    def can_teleport(self, obj_id, current_time):
        """Check if an object is allowed to teleport (not on cooldown)."""
        return obj_id not in self.cooldown_end_times or current_time >= self.cooldown_end_times[obj_id]

    def start_cooldown(self, obj_id, current_time):
        """Start the teleport cooldown for a specific object ID."""
        self.cooldown_end_times[obj_id] = current_time + self.cooldown_duration

    def schedule_deletion(self):
        self.marked_for_deletion = True


class PortalManager:
    def __init__(self, physics_manager):
        self.portal_pairs = {}
        self.next_pair_id = 0
        self.physics_manager = physics_manager
        self.teleport_queue = []
        self.creation_state = {'active': False, 'start_pos_pygame': None, 'start_angle': None} # For drag creation

    def set_physics_manager(self, manager):
        self.physics_manager = manager

    def start_portal_creation(self, start_pos_pygame):
        """Initiates the portal creation drag sequence."""
        if not self.physics_manager: return False
        valid_surface_found = True
        surface_angle = 0.0

        if valid_surface_found:
            self.creation_state['active'] = True
            self.creation_state['start_pos_pygame'] = start_pos_pygame
            self.creation_state['start_angle'] = surface_angle
            return True
        else:
            return False


    def finish_portal_creation(self, end_pos_pygame):
        """Completes portal creation, creating the pair."""
        if not self.creation_state['active'] or not self.physics_manager:
            self.cancel_portal_creation()
            return

        start_pos_pygame = self.creation_state['start_pos_pygame']
        start_angle = self.creation_state['start_angle']

        valid_end_surface = True
        end_angle = math.pi / 2

        if valid_end_surface and start_pos_pygame:
            start_pos_box2d = to_box2d(start_pos_pygame)
            end_pos_box2d = to_box2d(end_pos_pygame)

            self._create_pair(start_pos_box2d, start_angle, end_pos_box2d, end_angle)
        else:
             print("Invalid end surface or start position lost.")

        self.cancel_portal_creation()

    def cancel_portal_creation(self):
         """Resets the portal creation state."""
         self.creation_state['active'] = False
         self.creation_state['start_pos_pygame'] = None
         self.creation_state['start_angle'] = None


    def _create_pair(self, pos1_box2d, angle1_rad, pos2_box2d, angle2_rad):
        """Internal helper to create a linked pair and their physics bodies."""
        if not self.physics_manager:
            print("Error: Cannot create portal pair without PhysicsManager.")
            return

        pair_id = self.next_pair_id
        color = PORTAL_COLORS[pair_id % len(PORTAL_COLORS)]

        portal1 = Portal(pos1_box2d, angle1_rad, color, pair_id)
        portal2 = Portal(pos2_box2d, angle2_rad, color, pair_id)

        portal1.link(portal2)

        body1_created = self.physics_manager.add_portal(portal1)
        body2_created = self.physics_manager.add_portal(portal2)

        if body1_created and body2_created:
            self.portal_pairs[pair_id] = [portal1, portal2]
            self.next_pair_id += 1
            print(f"Created portal pair {pair_id}")
        else:
            print(f"Failed to create physics bodies for portal pair {pair_id}. Aborting.")
            if body1_created and portal1.body: self.physics_manager.destroy_body(portal1.body)
            if body2_created and portal2.body: self.physics_manager.destroy_body(portal2.body)


    def delete_portal_pair(self, pair_id):
         """Deletes a portal pair and schedules their bodies for destruction."""
         if pair_id in self.portal_pairs:
              portal_a, portal_b = self.portal_pairs[pair_id]
              portal_a.schedule_deletion()
              portal_b.schedule_deletion()
              if portal_a.body: self.physics_manager.destroy_body(portal_a.body)
              if portal_b.body: self.physics_manager.destroy_body(portal_b.body)
              del self.portal_pairs[pair_id]
              print(f"Deleted portal pair {pair_id}")

    def cleanup_deleted_portals(self):
         """Removes portal pairs where portals are marked for deletion."""
         ids_to_remove = [pid for pid, pair in self.portal_pairs.items() if pair[0].marked_for_deletion or pair[1].marked_for_deletion]
         for pid in ids_to_remove:
              if pid in self.portal_pairs:
                   del self.portal_pairs[pid]


    def get_all_portals(self):
        """Returns a flat list of all active, individual portal instances."""
        all_portals = []
        for pair in self.portal_pairs.values():
            if pair[0] and not pair[0].marked_for_deletion: all_portals.append(pair[0])
            if pair[1] and not pair[1].marked_for_deletion: all_portals.append(pair[1])
        return all_portals

    def queue_teleportation(self, obj, entry_portal):
        """Add object and entry portal to the queue for processing after physics step."""
        current_time = pygame.time.get_ticks() / 1000.0
        exit_portal = entry_portal.linked_portal

        if not obj or not obj.body or not exit_portal:
            return
        if not exit_portal.can_teleport(obj.id, current_time):
            return

        if (obj, entry_portal) not in self.teleport_queue:
            self.teleport_queue.append((obj, entry_portal))
            obj.teleporting = True

    def process_teleportation_queue(self, physics_manager):
        """Handles actual teleportation for items in the queue."""
        if not self.teleport_queue: return

        processed_objects_this_frame = set()
        current_time = pygame.time.get_ticks() / 1000.0

        for obj, entry_portal in self.teleport_queue:
            if obj in processed_objects_this_frame or not obj or obj.marked_for_deletion or not obj.body:
                if obj: obj.teleporting = False # Reset flag if object is invalid
                continue

            exit_portal = entry_portal.linked_portal
            if not exit_portal or exit_portal.marked_for_deletion or not exit_portal.body:
                 obj.teleporting = False # Reset flag if cannot teleport
                 continue # Skip if no valid exit portal

            if not exit_portal.can_teleport(obj.id, current_time):
                 obj.teleporting = False # Reset flag
                 continue # Skip if on cooldown

            exit_pos, exit_angle, exit_vel, exit_ang_vel = entry_portal.get_exit_transform(obj.body)

            try:
                obj.body.transform = (Box2D.b2Vec2(exit_pos), exit_angle)
                obj.body.linearVelocity = exit_vel
                obj.body.angularVelocity = exit_ang_vel
                obj.body.awake = True
            except Exception as e:
                 print(f"FATAL ERROR during teleport body transform: {e}")
                 obj.teleporting = False
                 continue


            obj.update_from_physics()

            exit_portal.start_cooldown(obj.id, current_time)

            obj.teleporting = False
            processed_objects_this_frame.add(obj)


        self.teleport_queue.clear()


    def update(self, dt):
        """Update portal states, like cooldowns."""
        current_time = pygame.time.get_ticks() / 1000.0
        for portal in self.get_all_portals():
             portal.update_cooldowns(current_time)
        self.cleanup_deleted_portals()


    def get_creation_preview_line(self):
        """Return start/end points (Pygame coords) for rendering the portal creation line."""
        if self.creation_state['active'] and self.creation_state['start_pos_pygame']:
            return self.creation_state['start_pos_pygame'], pygame.mouse.get_pos()
        return None

    def get_portal_count(self):
        """Returns the number of individual portals active."""
        return len(self.get_all_portals())