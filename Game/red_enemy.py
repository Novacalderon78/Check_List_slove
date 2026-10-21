import pygame
import random
from config import *

class RedEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player, red_enemys, image_path):
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
        self.player = player  # เก็บอ้างอิงถึงวัตถุ Player
        self.red_enemys = red_enemys  # เก็บอ้างอิงถึงรายการ RedEnemy
    def update(self):
        self.pos += self.vel
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        #move towards the player slightly
        direction = pygame.math.Vector2(self.player.rect.center) - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
            self.vel += direction * 0.1  # เพิ่มความเร็วไปทางผู้เล่น
            if self.vel.length() > self.max_speed:
                self.vel.scale_to_length(self.max_speed)
        #separate from other red enemies
        for other in self.red_enemys:
            if other != self and self.rect.colliderect(other.rect):
                separation = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(other.rect.center)
                if separation.length() > 0:
                    separation = separation.normalize()
                    self.vel += separation * 0.1  # เพิ่มความเร็วไปทางการแยกตัว
                    if self.vel.length() > self.max_speed:
                        self.vel.scale_to_length(self.max_speed)

        # collision with screen boundaries reflect the velocity vector
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.vel.x *= -1
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.vel.y *= -1

