

import pygame 
import matplotlib.pyplot as plt 
 
# ก ำหนดค่ำต่ำง ๆ 
SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 600 
BALL_RADIUS = 15 
GRAVITY = 0.1 
BOUNCE_DAMPING = 0.9 
DAMPING_COEFFICIENT = 0.999 
FPS = 60 
FRAME_LIMIT = 600 
 
# สี 
BLACK = (0, 0, 0) 
RED = (255, 0, 0) 
 
 
# ลูกบอลและต ำแหน่ง 
ball = {"x": 400, "y": 100, "vx": 3, "vy": 0, "color": RED} 
positions = []  # เก็บต ำแหน่งเพื่อพล็อตกรำฟ 
 
ball["x"] += ball["vx"] 
ball["y"] += ball["vy"] 
 
ball["vx"] *= DAMPING_COEFFICIENT 
ball["vy"] *= DAMPING_COEFFICIENT 
 
ball["vy"] += GRAVITY  # Apply gravity 
 
# กำรชนกับขอบจอ 
if ball["x"] - BALL_RADIUS <= 0 or ball["x"] + BALL_RADIUS >= SCREEN_WIDTH: 
    ball["vx"] = -ball["vx"] * BOUNCE_DAMPING 
 
if ball["y"] + BALL_RADIUS >= SCREEN_HEIGHT: 
    ball["vy"] = -ball["vy"] * BOUNCE_DAMPING 
    ball["y"] = SCREEN_HEIGHT - BALL_RADIUS 
 

positions.append((ball["x"], ball["y"]))  # บันทึกต ำแหน่ง

 
def draw_ball(ball): 
    pygame.draw.circle(screen, ball["color"], (int(ball["x"]), 
int(ball["y"])),  BALL_RADIUS) 
 

 
import pygame 
import matplotlib.pyplot as plt 
 
# ก ำหนดค่ำต่ำง ๆ 
SCREEN_WIDTH = 800 
SCREEN_HEIGHT = 600 
BALL_RADIUS = 15 
GRAVITY = 0.1 
BOUNCE_DAMPING = 0.9 
DAMPING_COEFFICIENT = 0.999 
FPS = 60 
FRAME_LIMIT = 600 
 
# สี 
BLACK = (0, 0, 0) 
RED = (255, 0, 0) 
 
# เริ ่มต้น Pygame 
pygame.init() 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
pygame.display.set_caption("ลูกบอลเด้ง") 
clock = pygame.time.Clock() 
 
# ลูกบอลและต ำแหน่ง 
ball = {"x": 400, "y": 100, "vx": 3, "vy": 0, "color": RED}

positions = []  # เก็บต ำแหน่งเพื่อพล็อตกรำฟ 
 
def move_ball(ball): 
    ball["x"] += ball["vx"] 
    ball["y"] += ball["vy"] 
    ball["vy"] += GRAVITY 
    ball["vx"] *= DAMPING_COEFFICIENT 
    ball["vy"] *= DAMPING_COEFFICIENT 
     
    # กำรชนกับขอบจอ 
    if ball["x"] - BALL_RADIUS <= 0 or ball["x"] + BALL_RADIUS >= SCREEN_WIDTH: 
        ball["vx"] = -ball["vx"] * BOUNCE_DAMPING 
    if ball["y"] + BALL_RADIUS >= SCREEN_HEIGHT: 
        ball["vy"] = -ball["vy"] * BOUNCE_DAMPING 
        ball["y"] = SCREEN_HEIGHT - BALL_RADIUS 
 
def draw_ball(ball): 
    pygame.draw.circle(screen, ball["color"], (int(ball["x"]), 
int(ball["y"])), BALL_RADIUS) 
 
# Simulation loop 
running = True 
time_steps = 0 
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
 
    screen.fill(BLACK) 
    move_ball(ball) 
    draw_ball(ball) 
    positions.append((ball["x"], ball["y"]))  # บันทึกต ำแหน่ง 
    pygame.display.flip() 
    clock.tick(FPS) 
    time_steps += 1 
    if time_steps > FRAME_LIMIT:  # จ ำกัดจ ำนวนเฟรม 
        running = False 
 
pygame.quit() 
 
# พล็อตกรำฟ 
positions_x = [p[0] for p in positions] 
positions_y = [p[1] for p in positions] 
 
plt.plot(positions_x, positions_y, label="Ball Path") 
plt.xlabel("X Position") 
plt.ylabel("Y Position") 

plt.title("Ball Trajectory") 
plt.legend() 
plt.grid() 
# Invert แกน y 
plt.gca().invert_yaxis() 
plt.show()

