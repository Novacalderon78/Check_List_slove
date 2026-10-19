import pygame
import sys
import os
import random
import math

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WASD Ball Game - Fun Mode!")
clock = pygame.time.Clock()
FPS = 60

# Ball properties
BALL_RADIUS = 40
SPEED = 6
DASH_SPEED = 20

ball_x = WIDTH // 2
ball_y = HEIGHT // 2
vx, vy = 0, 0
angle = 0

# Game Stats
score = 0
dash_cooldown = 0
trail_particles = []

# Load image
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "Nobody.jpg")

raw_texture = None
if os.path.exists(image_path):
    img = pygame.image.load(image_path).convert_alpha()
    img = pygame.transform.smoothscale(img, (BALL_RADIUS * 2, BALL_RADIUS * 2))
    
    circular_surface = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
    pygame.draw.circle(circular_surface, (255, 255, 255, 255), (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
    circular_surface.blit(img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    raw_texture = circular_surface
else:
    # Default circle if image not found
    raw_texture = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
    pygame.draw.circle(raw_texture, (255, 100, 100), (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)

# Collectible Star setup
def spawn_star():
    return [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)]

star_pos = spawn_star()

# Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.KEYDOWN:
            # DASH on Spacebar press
            if event.key == pygame.K_SPACE and dash_cooldown == 0:
                if vx != 0 or vy != 0:
                    ball_x += vx * DASH_SPEED
                    ball_y += vy * DASH_SPEED
                    dash_cooldown = 30  # 30 frames cooldown

    # Keyboard Movement
    keys = pygame.key.get_pressed()
    vx, vy = 0, 0
    if keys[pygame.K_w]: vy -= 1
    if keys[pygame.K_s]: vy += 1
    if keys[pygame.K_a]: vx -= 1
    if keys[pygame.K_d]: vx += 1

    # Normalize diagonal movement speed
    if vx != 0 and vy != 0:
        vx *= 0.7071
        vy *= 0.7071

    # Apply velocity
    ball_x += vx * SPEED
    ball_y += vy * SPEED

    # Rotate texture according to movement direction
    if vx != 0 or vy != 0:
        angle = (angle + vx * 5) % 360
        # Store trail points when moving
        trail_particles.append([ball_x, ball_y, BALL_RADIUS])

    # Cooldown timer update
    if dash_cooldown > 0:
        dash_cooldown -= 1

    # Screen Boundary Bouncing
    ball_x = max(BALL_RADIUS, min(WIDTH - BALL_RADIUS, ball_x))
    ball_y = max(BALL_RADIUS, min(HEIGHT - BALL_RADIUS, ball_y))

    # Star Collision Check
    distance = math.hypot(ball_x - star_pos[0], ball_y - star_pos[1])
    if distance < BALL_RADIUS + 15:
        score += 10
        star_pos = spawn_star()

    # --- DRAWING ---
    screen.fill((25, 25, 35))

    # 1. Draw Trail Effect
    new_trail = []
    for p in trail_particles:
        p[2] -= 1.5  # Shrink radius
        if p[2] > 0:
            new_trail.append(p)
            alpha_surface = pygame.Surface((int(p[2]*2), int(p[2]*2)), pygame.SRCALPHA)
            pygame.draw.circle(alpha_surface, (100, 200, 255, 80), (int(p[2]), int(p[2])), int(p[2]))
            screen.blit(alpha_surface, (p[0] - p[2], p[1] - p[2]))
    trail_particles = new_trail

    # 2. Draw Collectible Star
    pygame.draw.circle(screen, (255, 225, 50), star_pos, 15)
    pygame.draw.circle(screen, (255, 255, 200), star_pos, 8)

    # 3. Draw Rotated Ball
    rotated_texture = pygame.transform.rotate(raw_texture, angle)
    rect = rotated_texture.get_rect(center=(int(ball_x), int(ball_y)))
    screen.blit(rotated_texture, rect.topleft)

    # 4. Draw UI & Text
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (20, 20))

    dash_status = "READY" if dash_cooldown == 0 else f"{dash_cooldown//6 + 1}s"
    dash_text = font.render(f"SPACE to Dash: {dash_status}", True, (100, 200, 255) if dash_cooldown == 0 else (150, 150, 150))
    screen.blit(dash_text, (WIDTH - dash_text.get_width() - 20, 20))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()