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
        
        # Set size based on type
        if obj_type == "BOX":
            self.width = 32
            self.height = 32
            self.color = (255, 255, 255)  # White
        elif obj_type == "CIRCLE":
            self.radius = 16
            self.color = (255, 255, 0)  # Yellow
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
        else:
            return pygame.Rect(
                self.position.x - self.width / 2,
                self.position.y - self.height / 2,
                self.width,
                self.height
            )
            
    def should_remove(self):
        """Check if the object should be removed."""
        # Check if object is out of bounds
        if self.position.x < -100 or self.position.x > 1380:
            return True
        if self.position.y < -100 or self.position.y > 820:
            return True
        return False
