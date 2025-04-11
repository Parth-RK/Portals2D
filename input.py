import pygame
# Import Portal specifically for type checking later
from portals import Portal
# Import settings to access the new constant
from settings import to_box2d, MIN_PORTAL_DRAG_DISTANCE
import math # For distance calculation if needed (we'll use squared)

class InputManager:
    def __init__(self, game_instance):
        self.game = game_instance
        self.mouse_pos = (0, 0)
        self.prev_mouse_pos = (0, 0)
        self.mouse_rel = (0, 0)
        self.mouse_pressed = {1: False, 2: False, 3: False}

    def process_inputs(self):
        """Processes all Pygame events for a frame and updates input state."""

        self.prev_mouse_pos = self.mouse_pos
        try:
            current_mouse_pos = pygame.mouse.get_pos()
            if (isinstance(current_mouse_pos, tuple) and isinstance(self.prev_mouse_pos, tuple) and
                len(current_mouse_pos) == 2 and len(self.prev_mouse_pos) == 2):
                dx = current_mouse_pos[0] - self.prev_mouse_pos[0]
                dy = current_mouse_pos[1] - self.prev_mouse_pos[1]
                self.mouse_rel = (dx, dy)
                self.mouse_pos = current_mouse_pos
            else:
                self.mouse_rel = (0, 0)
                if isinstance(current_mouse_pos, tuple) and len(current_mouse_pos) == 2:
                    self.mouse_pos = current_mouse_pos
        except Exception as e:
            self.mouse_rel = (0, 0)
            print(f"Warning: Error updating mouse position: {e}")

        # --- Event Loop ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False
                    return
                if event.key == pygame.K_g:
                    self.game.physics_manager.toggle_gravity()
                if event.key == pygame.K_d:
                    self.game.debug_mode = not self.game.debug_mode
                    print(f"Debug mode: {'ON' if self.game.debug_mode else 'OFF'}")

                if event.key == pygame.K_c:
                    self.game.object_manager.create_object('circle', self.mouse_pos)
                if event.key == pygame.K_b:
                    self.game.object_manager.create_object('box', self.mouse_pos)
            
            ui_handled = self.game.ui_manager.handle_event(event)

            if not ui_handled:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pressed[event.button] = True
                    if event.button == 1:
                        obj_to_drag = self.game.object_manager.get_object_at(self.mouse_pos)
                        if obj_to_drag:
                            self.game.object_manager.start_drag(obj_to_drag, self.mouse_pos)
                        else:
                            # Start portal creation, it implicitly stores the start_pos_pygame now
                            self.game.portal_manager.start_portal_creation(self.mouse_pos)

                    elif event.button == 3:
                        # --- MODIFIED: Right-click handling ---
                        if self.game.portal_manager.creation_state['active']:
                             self.game.portal_manager.cancel_portal_creation()
                        else:
                             obj_to_delete = self.game.object_manager.get_object_at(self.mouse_pos)
                             if obj_to_delete:
                                  self.game.object_manager.delete_object(obj_to_delete)
                             else:
                                  # --- ADDED: Check for portal deletion if no object found ---
                                  # Use physics manager directly to query sensors
                                  potential_portal = self.game.physics_manager.get_body_at_pygame_point(
                                      self.mouse_pos, include_sensors=True
                                  )
                                  # Check if the result is actually a Portal instance
                                  if isinstance(potential_portal, Portal):
                                      # Found a portal, delete its pair
                                      print(f"Input: Deleting portal pair {potential_portal.pair_id} via right-click.")
                                      self.game.portal_manager.delete_portal_pair(potential_portal.pair_id)
                                  # --- End of Added Portal Deletion Check ---
                             
                elif event.type == pygame.MOUSEBUTTONUP:
                    button = event.button
                    self.mouse_pressed[button] = False
                    if button == 1:
                        if self.game.object_manager.selected_object:
                            self.game.object_manager.stop_drag(apply_throw=True, mouse_vel_pygame=self.mouse_rel)
                        elif self.game.portal_manager.creation_state['active']:
                             # --- MODIFIED: Check minimum distance before finishing ---
                             start_pos = self.game.portal_manager.creation_state.get('start_pos_pygame')
                             end_pos = self.mouse_pos
                             if start_pos:
                                 dx = end_pos[0] - start_pos[0]
                                 dy = end_pos[1] - start_pos[1]
                                 # Use squared distance to avoid sqrt calculation
                                 distance_sq = dx*dx + dy*dy
                                 min_dist_sq = MIN_PORTAL_DRAG_DISTANCE ** 2

                                 if distance_sq > min_dist_sq:
                                     # Sufficient distance, finish creation
                                     self.game.portal_manager.finish_portal_creation(end_pos)
                                 else:
                                     # Drag was too short, cancel silently or with a log
                                     # print("Portal drag too short, creation cancelled.")
                                     self.game.portal_manager.cancel_portal_creation()
                             else:
                                 # Should not happen if state is active, but cancel defensively
                                 self.game.portal_manager.cancel_portal_creation()
                             # --- End of Modified Minimum Distance Check ---

            if event.type == pygame.MOUSEMOTION:
                 if self.game.object_manager.mouse_joint:
                      self.game.object_manager.update_drag(self.mouse_pos)
