# main.py
import pygame 
from enemy import Enemy
from red_enemy import RedEnemy
from space import Space
import random
from config import *

BLACK = (0, 0, 0)
FPS = 60
pygame.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption("Emo Player Game") 
clock = pygame.time.Clock() 

all_sprites = pygame.sprite.Group()

# Initialize the controllable player using Emo.jpg
space = Space(400, 300, "Game/images/Emo.jpg")  
all_sprites.add(space)

enemys = []
for i in range(10):  
    enemy = Enemy(50 + i * 60, 50, "Game/images/enemy.png")
    enemys.append(enemy)
    all_sprites.add(enemy)

red_enemys = []
for i in range(10):  
    enemy = RedEnemy(50, 50 + i * 60, space, red_enemys, "Game/images/red_enemy.png")
    red_enemys.append(enemy)
    all_sprites.add(enemy)

running = True 
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 

    screen.fill(BLACK) 

    all_sprites.update()
    all_sprites.draw(screen)

    pygame.display.flip() 
    clock.tick(FPS)

pygame.quit()