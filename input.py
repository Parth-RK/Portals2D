import pygame
from settings import to_box2d

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
                            self.game.portal_manager.start_portal_creation(self.mouse_pos)

                    elif event.button == 3:
                        if self.game.portal_manager.creation_state['active']:
                             self.game.portal_manager.cancel_portal_creation()
                        else:
                             obj_to_delete = self.game.object_manager.get_object_at(self.mouse_pos)
                             if obj_to_delete:
                                  self.game.object_manager.delete_object(obj_to_delete)
                             
                elif event.type == pygame.MOUSEBUTTONUP:
                    button = event.button
                    self.mouse_pressed[button] = False
                    if button == 1:
                        if self.game.object_manager.selected_object:
                            self.game.object_manager.stop_drag(apply_throw=True, mouse_vel_pygame=self.mouse_rel)
                        elif self.game.portal_manager.creation_state['active']:
                             self.game.portal_manager.finish_portal_creation(self.mouse_pos)

            if event.type == pygame.MOUSEMOTION:
                 if self.game.object_manager.mouse_joint:
                      self.game.object_manager.update_drag(self.mouse_pos)
