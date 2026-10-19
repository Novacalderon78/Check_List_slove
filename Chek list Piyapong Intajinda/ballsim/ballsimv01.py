import pygame
import sys
import os
import math
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Simulator - Drag, Drop & Graph")
clock = pygame.time.Clock()
FPS = 60

# Physics constants
GRAVITY = 0.5
FRICTION = 0.99
BOUNCE_DAMPING = 0.8

def create_circular_texture(image_path, radius):
    """Loads an image, scales it, and crops it into a circle."""
    try:
        img = pygame.image.load(image_path).convert_alpha()
        img = pygame.transform.smoothscale(img, (radius * 2, radius * 2))
        circular_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(circular_surface, (255, 255, 255, 255), (radius, radius), radius)
        circular_surface.blit(img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return circular_surface
    except Exception as e:
        print(f"Could not load image: {e}")
        return None

class Ball:
    def __init__(self, x, y, radius, image_filename="Nobody.jpg"):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 5.0
        self.vy = 0.0
        self.color = (255, 100, 100)
        self.texture = None
        
        # Dragging states
        self.is_dragging = False
        self.offset_x = 0
        self.offset_y = 0
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_image_path = os.path.join(script_dir, image_filename)
        
        if os.path.exists(full_image_path):
            print(f"Successfully loaded '{image_filename}' from {script_dir}!")
            self.texture = create_circular_texture(full_image_path, radius)
        else:
            print(f"Could not find '{full_image_path}'.")

    def update(self):
        if self.is_dragging:
            return

        self.vy += GRAVITY
        self.vx *= FRICTION
        self.vy *= FRICTION
        
        self.x += self.vx
        self.y += self.vy
        
        if self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy = -self.vy * BOUNCE_DAMPING
        elif self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy * BOUNCE_DAMPING
            
        if self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx = -self.vx * BOUNCE_DAMPING
        elif self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx * BOUNCE_DAMPING

    def draw(self, surface):
        if self.texture:
            surface.blit(self.texture, (int(self.x - self.radius), int(self.y - self.radius)))
        else:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

# Create our ball
ball_radius = 80
my_ball = Ball(WIDTH // 2, HEIGHT // 2, ball_radius, image_filename="Nobody.jpg")

# Data tracking for the graph
history_x = []
history_y = []
frames = []
frame_count = 0

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mx, my = pygame.mouse.get_pos()
                distance = math.hypot(mx - my_ball.x, my - my_ball.y)
                if distance <= my_ball.radius:
                    my_ball.is_dragging = True
                    my_ball.offset_x = my_ball.x - mx
                    my_ball.offset_y = my_ball.y - my
                    my_ball.vx = 0
                    my_ball.vy = 0

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                my_ball.is_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if my_ball.is_dragging:
                mx, my = event.pos
                my_ball.x = mx + my_ball.offset_x
                my_ball.y = my + my_ball.offset_y
                my_ball.vx = event.rel[0]
                my_ball.vy = event.rel[1]

    # Update physics
    my_ball.update()

    # Record data for the graph
    frames.append(frame_count)
    history_x.append(my_ball.x)
    history_y.append(HEIGHT - my_ball.y) # Invert Y so the graph shows bouncing UP properly
    frame_count += 1

    # Draw everything
    screen.fill((30, 30, 40)) 
    
    font = pygame.font.SysFont(None, 36)
    if my_ball.texture:
        text = font.render("Close window to see graph! (Piyapong Intajinda)", True, (200, 200, 200))
    else:
        text = font.render("No 'Nobody.jpg' found. Check your folder.", True, (255, 100, 100))
        
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 30))

    my_ball.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

# Close Pygame window
pygame.quit()

# ----------------- SHOW GRAPH -----------------
print("Generating graph...")
plt.figure(figsize=(10, 5))
plt.plot(frames, history_y, label="Y Position (Bounce Height)", color="blue")
plt.plot(frames, history_x, label="X Position (Horizontal)", color="orange")

plt.title("Ball Trajectory Over Time")
plt.xlabel("Time (Frames)")
plt.ylabel("Position (Pixels)")
plt.legend()
plt.grid(True)
plt.show()

sys.exit()