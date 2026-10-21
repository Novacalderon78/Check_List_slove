# space.py
import pygame
import sys
import math
from config import *

class Space(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        
        # Use .convert() for JPG images (no alpha transparency channel)
        self.original_image = pygame.image.load(image_path).convert()
        self.original_image = pygame.transform.scale(self.original_image, (100, 100))
        self.image = pygame.transform.scale(self.original_image, (100, 100))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5
        self.angle = 0
        self.rotation_speed = 3
        self.rotation_smoothness = 0.15

        self.thrust = 0.5       # Acceleration
        self.friction = 0.98    # Friction (deceleration)
        self.max_speed = 5     # Maximum speed limit
        self.velocity = pygame.math.Vector2(0, 0)  
        self.pos = pygame.math.Vector2(x, y)  

    def update(self):
        keys = pygame.key.get_pressed()

        # --- WASD Keyboard Controls ---
        input_dir = pygame.math.Vector2(0, 0)
        if keys[pygame.K_a]:      # Move Left
            input_dir.x -= 1
        if keys[pygame.K_d]:      # Move Right
            input_dir.x += 1
        if keys[pygame.K_w]:      # Move Up
            input_dir.y -= 1
        if keys[pygame.K_s]:      # Move Down
            input_dir.y += 1

        # Calculate movement & rotation when keys are pressed
        if input_dir.length() > 0:
            input_dir = input_dir.normalize()
            
            target_angle = math.degrees(math.atan2(-input_dir.y, input_dir.x)) - 90
            
            angle_diff = (target_angle - self.angle) % 360
            if angle_diff > 180:
                angle_diff -= 360
                
            self.angle += angle_diff * self.rotation_smoothness

            angle_rad = math.radians(self.angle + 90)
            accel_x = math.cos(angle_rad) * self.thrust
            accel_y = -math.sin(angle_rad) * self.thrust
            
            self.velocity.x += accel_x
            self.velocity.y += accel_y
            
        else:
            # Apply friction when no movement keys are pressed
            self.velocity *= self.friction
            if self.velocity.length() < 0.1:
                self.velocity.update(0, 0)

        if self.velocity.length() > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        self.pos += self.velocity
        
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=(round(self.pos.x), round(self.pos.y)))

        # Screen boundary check (Bounce)
        if self.rect.left < 0:  
            self.rect.left = 0
            self.pos.x = self.rect.centerx
            self.velocity.x *= -1  
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.pos.x = self.rect.centerx
            self.velocity.x *= -1  
        if self.rect.top < 0:
            self.rect.top = 0
            self.pos.y = self.rect.centery
            self.velocity.y *= -1  
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.pos.y = self.rect.centery
            self.velocity.y *= -1