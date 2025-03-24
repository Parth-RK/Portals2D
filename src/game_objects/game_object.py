import uuid
import pygame
import Box2D
from Box2D import b2Vec2

class GameObject:
    def __init__(self, obj_type, x, y):
        self.id = str(uuid.uuid4())[:8]  # Generate a unique identifier
        self.obj_type = obj_type
        self.position = b2Vec2(x, y)
        self.velocity = b2Vec2(0, 0)
        self.angle = 0.0  # Rotation angle in radians
        self.angular_velocity = 0.0
        
        # Physical properties
        self.body = None  # Will be set by physics engine
        self.fixture = None  # Will be set by physics engine
        
        # Animation properties
        self.is_teleporting = False
        self.teleport_progress = 0.0
        self.teleport_duration = 0.3  # seconds
        self.teleport_start_scale = 1.0
        self.teleport_end_scale = 0.1  # Shrink to 10% when disappearing
        self.current_scale = 1.0
        
        # Set size based on type
        if obj_type == "BOX":
            self.width = 32
            self.height = 32
            self.color = (255, 255, 255)  # White
        elif obj_type == "CIRCLE":
            self.radius = 16
            self.color = (255, 255, 0)  # Yellow
        elif obj_type == "TRIANGLE":
            self.side_length = 32  # Size of equilateral triangle
            self.color = (0, 200, 200)  # Cyan
        else:
            self.width = 16
            self.height = 16
            self.color = (200, 200, 200)  # Light gray
            
    def update(self, dt):
        """Update object state."""
        if self.body:
            # Sync position and rotation from physics body
            self.position = self.body.position
            self.angle = self.body.angle
            self.velocity = self.body.linearVelocity
            self.angular_velocity = self.body.angularVelocity
            
        # Update teleport animation if active
        if self.is_teleporting:
            self.teleport_progress += dt / self.teleport_duration
            if self.teleport_progress >= 1.0:
                self.is_teleporting = False
                self.teleport_progress = 0.0
                self.current_scale = 1.0
            else:
                # Calculate current scale based on animation progress
                self.current_scale = self.teleport_start_scale + (self.teleport_end_scale - self.teleport_start_scale) * self.teleport_progress
            
    def start_teleport_animation(self, entering=True):
        """Start teleport animation."""
        self.is_teleporting = True
        self.teleport_progress = 0.0
        if entering:
            # Entering animation (shrinking)
            self.teleport_start_scale = 1.0
            self.teleport_end_scale = 0.1
        else:
            # Exiting animation (growing)
            self.teleport_start_scale = 0.1
            self.teleport_end_scale = 1.0
            
    def set_position(self, x, y):
        """Set the object's position."""
        self.position = b2Vec2(x, y)
        if self.body:
            self.body.position = self.position
            
    def set_velocity(self, vx, vy):
        """Set the object's velocity."""
        self.velocity = b2Vec2(vx, vy)
        if self.body:
            self.body.linearVelocity = self.velocity
            
    def set_angle(self, angle):
        """Set the object's angle."""
        self.angle = angle
        if self.body:
            self.body.angle = angle
            
    def apply_force(self, fx, fy):
        """Apply force to the object."""
        if self.body:
            self.body.ApplyForce(b2Vec2(fx, fy), self.body.worldCenter, True)
            
    def apply_impulse(self, ix, iy):
        """Apply impulse to the object."""
        if self.body:
            self.body.ApplyLinearImpulse(b2Vec2(ix, iy), self.body.worldCenter, True)
            
    def get_rect(self):
        """Get the object's rectangular bounds."""
        if self.obj_type == "CIRCLE":
            return pygame.Rect(
                self.position.x - self.radius,
                self.position.y - self.radius,
                self.radius * 2,
                self.radius * 2
            )
        elif self.obj_type == "TRIANGLE":
            # Approximating the triangle with a rectangle
            height = self.side_length * 0.866  # sqrt(3)/2
            return pygame.Rect(
                self.position.x - self.side_length / 2,
                self.position.y - height / 2,
                self.side_length,
                height
            )
        else:
            return pygame.Rect(
                self.position.x - self.width / 2,
                self.position.y - self.height / 2,
                self.width,
                self.height
            )
            
    def should_remove(self):
        """Check if the object should be removed."""
        # For triangles, use side_length to determine if they're out of bounds
        if self.obj_type == "TRIANGLE":
            if self.position.x < -100 or self.position.x > 1380:
                return True
            if self.position.y < -100 or self.position.y > 820:
                return True
        else:
            # For other objects
            if self.position.x < -100 or self.position.x > 1380:
                return True
            if self.position.y < -100 or self.position.y > 820:
                return True
        return False
