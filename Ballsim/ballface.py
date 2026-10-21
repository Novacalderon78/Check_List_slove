import os
import sys
import matplotlib.pyplot as plt
import pygame

# --- ค่ากำหนดต่าง ๆ ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 30  # Increased for better visibility of the face
GRAVITY = 0.1
BOUNCE_DAMPING = 0.9
DAMPING_COEFFICIENT = 0.999
FPS = 60
FRAME_LIMIT = 600

# สี
BLACK = (0, 0, 0)

# --- เริ่มต้น Pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Optimized Bouncing Image - Circular Face")
clock = pygame.time.Clock()

# --- โหลดและปรับรูปภาพให้เป็นวงกลม ---
# หาเส้นทางโฟลเดอร์ที่ไฟล์สคริปต์นี้ตั้งอยู่
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_PATH = os.path.join(SCRIPT_DIR, "Emo.jpg")

if os.path.exists(IMAGE_PATH):
    try:
        # 1. โหลดภาพต้นฉบับ
        ball_original_image = pygame.image.load(IMAGE_PATH).convert_alpha()
        
        # 2. ปรับขนาดภาพเป็นสี่เหลี่ยมจัตุรัสที่มีขนาดเส้นผ่านศูนย์กลาง (2 * r)
        target_size = (BALL_RADIUS * 2, BALL_RADIUS * 2)
        ball_scaled_image = pygame.transform.scale(ball_original_image, target_size)
        
        # 3. สร้าง Surface หน้ากาก (Mask) วงกลมสีขาว
        mask_surface = pygame.Surface(target_size, pygame.SRCALPHA)
        # วาดวงกลมสีขาวสนิท (Alpha=255) ตรงกลาง โดยพิกัดศูนย์กลางคือ r, r
        pygame.draw.circle(mask_surface, (255, 255, 255), (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        
        # 4. รวมภาพสี่เหลี่ยมกับหน้ากากเข้าด้วยกัน
        # สร้างภาพใหม่ที่ว่างเปล่า (ใส)
        ball_circular_image = pygame.Surface(target_size, pygame.SRCALPHA)
        # วางภาพสี่เหลี่ยมลงไป
        ball_circular_image.blit(ball_scaled_image, (0, 0))
        # ใช้โหมด BLEND_RGBA_MULT คูณ Alpha ของภาพกับหน้ากาก
        # (ส่วนขาวของ mask จะคงภาพไว้, ส่วนใสของ mask จะทำให้ภาพใส)
        ball_circular_image.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        # 5. ใช้ภาพวงกลมเป็นภาพลูกบอลสุดท้าย
        ball_image = ball_circular_image
        print("โหลดไฟล์ Emo.jpg และสร้างวงกลมสำเร็จ!")

    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการโหลดหรือประมวลผลภาพ: {e}")
        pygame.quit()
        sys.exit()
else:
    # --- กรณีหาไฟล์ไม่เจอ (Fallback) ---
    print(f"ไม่พบไฟล์ '{IMAGE_PATH}' ใช้รูปวงกลมสีขาวธรรมดาแทน")
    ball_image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
    pygame.draw.circle(ball_image, (255, 255, 255), (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)

# --- สถานะลูกบอลและตำแหน่ง ---
ball = {"x": 400.0, "y": 100.0, "vx": 3.0, "vy": 0.0}
positions = []


def move_ball(ball):
    # อัปเดตตำแหน่งและแรงทางฟิสิกส์
    ball["x"] += ball["vx"]
    ball["y"] += ball["vy"]
    ball["vy"] += GRAVITY
    ball["vx"] *= DAMPING_COEFFICIENT
    ball["vy"] *= DAMPING_COEFFICIENT

    # การชนขอบซ้าย-ขวา พร้อมป้องกันภาพจมขอบ
    if ball["x"] - BALL_RADIUS <= 0:
        ball["vx"] = -ball["vx"] * BOUNCE_DAMPING
        ball["x"] = BALL_RADIUS
    elif ball["x"] + BALL_RADIUS >= SCREEN_WIDTH:
        ball["vx"] = -ball["vx"] * BOUNCE_DAMPING
        ball["x"] = SCREEN_WIDTH - BALL_RADIUS

    # การชนขอบล่าง พร้อมป้องกันภาพจมขอบ
    if ball["y"] + BALL_RADIUS >= SCREEN_HEIGHT:
        ball["vy"] = -ball["vy"] * BOUNCE_DAMPING
        ball["y"] = SCREEN_HEIGHT - BALL_RADIUS


def draw_ball(ball, image):
    # วาดภาพให้อยู่ตรงกลางตำแหน่งศูนย์กลางของลูกบอล
    # ลบด้วยรัศมีเพื่อให้พิกัด blit อยู่ที่มุมซ้ายบน
    top_left_x = int(ball["x"] - BALL_RADIUS)
    top_left_y = int(ball["y"] - BALL_RADIUS)
    screen.blit(image, (top_left_x, top_left_y))


# --- Simulation Loop ---
running = True
time_steps = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    move_ball(ball)
    draw_ball(ball, ball_image)

    # บันทึกตำแหน่งปัจจุบันเพื่อนำไปพล็อต กราฟ
    positions.append((ball["x"], ball["y"]))

    pygame.display.flip()
    clock.tick(FPS)

    time_steps += 1
    if time_steps > FRAME_LIMIT:
        running = False

pygame.quit()

# --- พล็อต กราฟด้วย Matplotlib ---
positions_x = [p[0] for p in positions]
positions_y = [p[1] for p in positions]

plt.figure(figsize=(10, 6))
plt.plot(positions_x, positions_y, label="Emo.jpg Path", color="blue")
plt.xlabel("X Position (Pixels)")
plt.ylabel("Y Position (Pixels)")
plt.title("Circular Emo.jpg Trajectory over Time")
plt.legend()
plt.grid(True)

# กลับแกน Y เพื่อให้ตรงกับพิกัดจอของ Pygame (0 อยู่บนสุด)
plt.gca().invert_yaxis()
plt.show()