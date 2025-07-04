import pygame
import random

pygame.init()
pygame.mixer.init()

# Ukuran layar dan blok
width = 600
height = 400
block = 20

# Warna
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 255)
gray = (180, 180, 180)

# Setup layar dan font
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game Level Edition")
font = pygame.font.SysFont("comicsansms", 25)
clock = pygame.time.Clock()

# Load backsound & suara makan
try:
    pygame.mixer.music.load("backsound.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except:
    print("⚠️ backsound.mp3 tidak ditemukan")

try:
    eat_sound = pygame.mixer.Sound("suara_makan.mp3")
    eat_sound.set_volume(0.6)
except:
    eat_sound = None
    print("⚠️ suara_makan.mp3 tidak ditemukan")

# Fungsi bantuan
def draw_text(msg, color, x, y):
    text = font.render(msg, True, color)
    win.blit(text, [x, y])

def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(win, green, [x[0], x[1], block, block])

def draw_grid():
    for x in range(0, width, block):
        pygame.draw.line(win, gray, (x, 0), (x, height))
    for y in range(0, height, block):
        pygame.draw.line(win, gray, (0, y), (width, y))

def draw_walls(walls):
    for wall in walls:
        pygame.draw.rect(win, black, wall)

def get_level_data(level_name):
    levels = {
        "baby": (5, []),
        "sangat noob": (8, [[200, 100, block*2, block]]),
        "noob": (10, [[200, 100, block*2, block], [300, 200, block*2, block]]),
        "ez": (13, [[200, 100, block*2, block], [300, 200, block*2, block], [100, 250, block*2, block]]),
        "normal": (15, [[200, 100, block*2, block], [300, 200, block*2, block], [100, 250, block*2, block], [400, 150, block, block*2]]),
        "hard": (18, [[200, 100, block*2, block], [300, 200, block*2, block], [100, 250, block*2, block], [400, 150, block, block*2], [250, 300, block*2, block], [150, 50, block*2, block]]),
        "expert": (22, [[200, 100, block*2, block], [300, 200, block*2, block], [100, 250, block*2, block], [400, 150, block, block*2], [250, 300, block*2, block], [150, 50, block*2, block], [350, 100, block, block*3], [100, 100, block*3, block]])
    }
    return levels.get(level_name, (10, []))

def choose_level():
    levels = ["baby", "sangat noob", "noob", "ez", "normal", "hard", "expert"]
    selected = 0
    choosing = True
    while choosing:
        win.fill(white)
        draw_text("Pilih Level (↑↓, ENTER):", blue, 30, 30)
        for i, name in enumerate(levels):
            color = red if i == selected else black
            draw_text(f"{i+1}. {name}", color, 100, 80 + i*30)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(levels)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(levels)
                elif event.key == pygame.K_RETURN:
                    choosing = False
    return levels[selected]

def gameLoop():
    level_name = choose_level()
    speed, wall_defs = get_level_data(level_name)
    game_over = False
    game_close = False

    # === PERBAIKAN DI SINI ===
    # Memastikan posisi awal ular sejajar dengan grid
    x = round((width / 4) / block) * block
    y = round((height / 2) / block) * block
    
    x_change = block
    y_change = 0

    snake_list = []
    snake_length = 1

    foodx = round(random.randrange(block, width - 2 * block) / block) * block
    foody = round(random.randrange(block, height - 2 * block) / block) * block

    walls = [
        [0, 0, width, block],  # atas
        [0, height - block, width, block],  # bawah
        [0, 0, block, height],  # kiri
        [width - block, 0, block, height]  # kanan
    ] + wall_defs

    while not game_over:
        while game_close:
            win.fill(white)
            draw_text("KAMU KALAH! Tekan [C] untuk Ulang atau [Q] untuk Keluar", red, 30, height // 3)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit(); quit()
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -block; y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = block; y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    y_change = -block; x_change = 0
                elif event.key == pygame.K_DOWN and y_change == 0:
                    y_change = block; x_change = 0

        x += x_change
        y += y_change

        win.fill(white)
        draw_grid()
        draw_walls(walls)
        pygame.draw.rect(win, red, [foodx, foody, block, block])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        for wall in walls:
            wall_rect = pygame.Rect(wall)
            if wall_rect.colliderect(pygame.Rect(x, y, block, block)):
                game_close = True

        draw_snake(snake_list)
        draw_text(f"Skor: {snake_length - 1}", black, 10, 10)
        pygame.display.update()

        if x == foodx and y == foody:
            foodx = round(random.randrange(block, width - 2 * block) / block) * block
            foody = round(random.randrange(block, height - 2 * block) / block) * block
            snake_length += 1
            if eat_sound:
                eat_sound.play()

        clock.tick(speed)

    pygame.quit()
    quit()

gameLoop()