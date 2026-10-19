import pygame
import sys
import os
import math

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Simulator - Drag and Drop")
clock = pygame.time.Clock()
FPS = 60

# Physics constants
GRAVITY = 0.5
FRICTION = 0.99
BOUNCE_DAMPING = 0.8

def create_circular_texture(image_path, radius):
    """Loads an image, scales it, and crops it into a circle."""
    try:
        # Load the image and scale it to fit the ball's diameter
        img = pygame.image.load(image_path).convert_alpha()
        img = pygame.transform.smoothscale(img, (radius * 2, radius * 2))
        
        # Create a blank transparent surface
        circular_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        
        # Draw a solid white circle on the transparent surface
        pygame.draw.circle(circular_surface, (255, 255, 255, 255), (radius, radius), radius)
        
        # Multiply the colors of the image with the solid circle
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
        
        # Get the absolute directory where THIS script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Combine it with the image filename
        full_image_path = os.path.join(script_dir, image_filename)
        
        # Check for the image using the absolute path
        if os.path.exists(full_image_path):
            print(f"Successfully loaded '{image_filename}' from {script_dir}!")
            self.texture = create_circular_texture(full_image_path, radius)
        else:
            print(f"Could not find '{full_image_path}'.")

    def update(self):
        # Stop physics if the ball is being dragged
        if self.is_dragging:
            return

        # Apply gravity and friction
        self.vy += GRAVITY
        self.vx *= FRICTION
        self.vy *= FRICTION
        
        # Move ball
        self.x += self.vx
        self.y += self.vy
        
        # Bounce off the bottom
        if self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy = -self.vy * BOUNCE_DAMPING
            
        # Bounce off the top
        elif self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy * BOUNCE_DAMPING
            
        # Bounce off the right
        if self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx = -self.vx * BOUNCE_DAMPING
            
        # Bounce off the left
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

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Start Dragging
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse click
                mx, my = pygame.mouse.get_pos()
                # Check if mouse is clicking inside the ball
                distance = math.hypot(mx - my_ball.x, my - my_ball.y)
                if distance <= my_ball.radius:
                    my_ball.is_dragging = True
                    # Calculate the offset so the ball doesn't snap its center to the mouse
                    my_ball.offset_x = my_ball.x - mx
                    my_ball.offset_y = my_ball.y - my
                    # Stop its movement while held
                    my_ball.vx = 0
                    my_ball.vy = 0

        # Stop Dragging
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                my_ball.is_dragging = False

        # Handle Dragging Motion
        elif event.type == pygame.MOUSEMOTION:
            if my_ball.is_dragging:
                mx, my = event.pos
                # Update ball position based on mouse position and offset
                my_ball.x = mx + my_ball.offset_x
                my_ball.y = my + my_ball.offset_y
                # Set velocity based on mouse movement speed (allows you to "throw" it)
                my_ball.vx = event.rel[0]
                my_ball.vy = event.rel[1]

    # Update physics
    my_ball.update()

    # Draw everything
    screen.fill((30, 30, 40)) 
    
    # Draw instructions
    font = pygame.font.SysFont(None, 36)
    if my_ball.texture:
        text = font.render("Click and hold the ball to drag it! (Piyapong Intajinda)", True, (200, 200, 200))
    else:
        text = font.render("No 'Nobody.jpg' found. Check your folder.", True, (255, 100, 100))
        
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 30))

    # Draw ball
    my_ball.draw(screen)

    # Refresh screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()