import pygame
import random
from config import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.original_image = pygame.image.load(image_path)
        self.original_image = pygame.transform.scale(
                        self.original_image, (50, 50))  # ปรับ
        self.image = pygame.transform.scale(
                        self.original_image, (50, 50))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.max_speed = 2     # ล็อกความเร็วสูงสุด
        vx = random.uniform(-self.max_speed, self.max_speed)
        vy = random.uniform(-self.max_speed, self.max_speed)
        self.vel = pygame.math.Vector2(vx, vy)  # เวกเตอร์ความเร็ว
        self.pos = pygame.math.Vector2(x, y)  # เวกเตอร์ตำแหน่ง (ใช้ float เพื่อความแม่นยำ)

    def update(self):
        self.pos += self.vel
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        # collision with screen boundaries reflect the velocity vector
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.vel.x *= -1
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.vel.y *= -1