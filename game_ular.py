import pygame
import random
import os

pygame.init()
pygame.mixer.init()

WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
BLUE = (0, 0, 255)
GRAY = (180, 180, 180)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Edisi Progresif")
font = pygame.font.SysFont("comicsansms", 25)
clock = pygame.time.Clock()

ASSET_FOLDER = os.path.join(os.path.dirname(__file__), 'assets')

def get_asset_path(filename):
    return os.path.join(ASSET_FOLDER, filename)

try:
    eat_sound = pygame.mixer.Sound(get_asset_path("suara_makan.mp3"))
    eat_sound.set_volume(0.6)
except pygame.error:
    eat_sound = None
    print("⚠️ Peringatan: suara_makan.mp3 tidak ditemukan di folder 'assets'.")

def draw_text(msg, color, x, y):
    text = font.render(msg, True, color)
    win.blit(text, text.get_rect(center=(x, y)))

def draw_snake(snake_list):
    if not snake_list:
        return
    head = snake_list[-1]
    pygame.draw.rect(win, DARK_GREEN, [head[0], head[1], BLOCK_SIZE, BLOCK_SIZE])
    for x in snake_list[:-1]:
        pygame.draw.rect(win, GREEN, [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])

def draw_grid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(win, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(win, GRAY, (0, y), (WIDTH, y))

def draw_walls(walls):
    for wall in walls:
        pygame.draw.rect(win, BLACK, wall)

def load_highscore():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0

def save_highscore(score):
    highscore = load_highscore()
    if score > highscore:
        with open("highscore.txt", "w") as f:
            f.write(str(score))

def get_level_data(level_name):
    levels = {
        "baby": (5, []),
        "sangat noob": (8, [[200, 100, BLOCK_SIZE*2, BLOCK_SIZE]]),
        "noob": (10, [[200, 100, BLOCK_SIZE*2, BLOCK_SIZE], [300, 200, BLOCK_SIZE*2, BLOCK_SIZE]]),
        "ez": (13, [[200, 100, BLOCK_SIZE*2, BLOCK_SIZE], [300, 200, BLOCK_SIZE*2, BLOCK_SIZE], [100, 250, BLOCK_SIZE*2, BLOCK_SIZE]]),
        "normal": (15, [[200, 100, BLOCK_SIZE*2, BLOCK_SIZE], [300, 200, BLOCK_SIZE*2, BLOCK_SIZE], [100, 250, BLOCK_SIZE*2, BLOCK_SIZE], [400, 150, BLOCK_SIZE, BLOCK_SIZE*2]]),
        "hard": (18, [[200, 100, BLOCK_SIZE*2, BLOCK_SIZE], [300, 200, BLOCK_SIZE*2, BLOCK_SIZE], [100, 250, BLOCK_SIZE*2, BLOCK_SIZE], [400, 150, BLOCK_SIZE, BLOCK_SIZE*2], [250, 300, BLOCK_SIZE*2, BLOCK_SIZE], [150, 50, BLOCK_SIZE*2, BLOCK_SIZE]]),
        "expert": (22, [[200, 100, BLOCK_SIZE*2, BLOCK_SIZE], [300, 200, BLOCK_SIZE*2, BLOCK_SIZE], [100, 250, BLOCK_SIZE*2, BLOCK_SIZE], [400, 150, BLOCK_SIZE, BLOCK_SIZE*2], [250, 300, BLOCK_SIZE*2, BLOCK_SIZE], [150, 50, BLOCK_SIZE*2, BLOCK_SIZE], [350, 100, BLOCK_SIZE, BLOCK_SIZE*3], [100, 100, BLOCK_SIZE*3, BLOCK_SIZE]])
    }
    return levels.get(level_name, (10, []))

def choose_level():
    levels = ["baby", "sangat noob", "noob", "ez", "normal", "hard", "expert"]
    selected = 0
    choosing = True
    
    try:
        pygame.mixer.music.load(get_asset_path("backsound.wav"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("⚠️ Peringatan: backsound.wav tidak ditemukan di folder 'assets' untuk menu.")

    while choosing:
        win.fill(WHITE)
        draw_text("Pilih Level (Gunakan ↑↓, lalu ENTER)", BLUE, WIDTH / 2, 50)
        
        for i, name in enumerate(levels):
            color = RED if i == selected else BLACK
            draw_text(f"{i+1}. {name.title()}", color, WIDTH / 2, 120 + i*40)
            
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(levels)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(levels)
                elif event.key == pygame.K_RETURN:
                    choosing = False
    
    pygame.mixer.music.stop()
    return levels[selected]

def gameLoop():
    level_name = choose_level()
    initial_speed, wall_defs = get_level_data(level_name)
    
    if level_name in ["normal", "hard"]:
        music_file = "menengah.wav"
    elif level_name == "expert":
        music_file = "mencekam.mp3"
    else:
        music_file = "backsound.wav"
    
    try:
        pygame.mixer.music.load(get_asset_path(music_file))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        print(f"🎵 Memainkan musik: {music_file}")
    except pygame.error:
        print(f"⚠️ Peringatan: {music_file} tidak ditemukan di folder 'assets'!")

    game_over = False
    game_close = False
    paused = False
    highscore = load_highscore()

    # --- PERUBAHAN 1: Variabel untuk kecepatan dinamis ---
    current_speed = initial_speed
    speed_increment = 1 # Kecepatan akan bertambah 1 setiap 5 skor

    x = round((WIDTH / 4) / BLOCK_SIZE) * BLOCK_SIZE
    y = round((HEIGHT / 2) / BLOCK_SIZE) * BLOCK_SIZE
    x_change = BLOCK_SIZE
    y_change = 0

    snake_list = []
    snake_length = 1

    foodx = round(random.randrange(BLOCK_SIZE, WIDTH - 2 * BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    foody = round(random.randrange(BLOCK_SIZE, HEIGHT - 2 * BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    walls = [
        [0, 0, WIDTH, BLOCK_SIZE],
        [0, HEIGHT - BLOCK_SIZE, WIDTH, BLOCK_SIZE],
        [0, 0, BLOCK_SIZE, HEIGHT],
        [WIDTH - BLOCK_SIZE, 0, BLOCK_SIZE, HEIGHT]
    ] + wall_defs

    while not game_over:
        
        while game_close:
            pygame.mixer.music.stop()
            current_score = snake_length - 1
            save_highscore(current_score)
            highscore = load_highscore()

            win.fill(WHITE)
            draw_text("KAMU KALAH!", RED, WIDTH / 2, HEIGHT / 3)
            draw_text(f"Skor Kamu: {current_score}", BLACK, WIDTH / 2, HEIGHT / 2 - 20)
            draw_text(f"Skor Tertinggi: {highscore}", BLUE, WIDTH / 2, HEIGHT / 2 + 20)
            draw_text("Tekan [C] untuk Kembali ke Menu", BLACK, WIDTH / 2, HEIGHT * 2 / 3 + 20)
            draw_text("Tekan [Q] untuk Keluar", BLACK, WIDTH / 2, HEIGHT * 2 / 3 + 60)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

                if not paused:
                    if event.key == pygame.K_LEFT and x_change == 0:
                        x_change = -BLOCK_SIZE; y_change = 0
                    elif event.key == pygame.K_RIGHT and x_change == 0:
                        x_change = BLOCK_SIZE; y_change = 0
                    elif event.key == pygame.K_UP and y_change == 0:
                        y_change = -BLOCK_SIZE; x_change = 0
                    elif event.key == pygame.K_DOWN and y_change == 0:
                        y_change = BLOCK_SIZE; x_change = 0
        
        if paused:
            draw_text("|| PAUSED ||", BLUE, WIDTH / 2, HEIGHT / 2)
            pygame.display.update()
            clock.tick(5)
            continue

        x += x_change
        y += y_change

        win.fill(WHITE)
        draw_grid()
        draw_walls(walls)
        pygame.draw.rect(win, RED, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        for wall in walls:
            if pygame.Rect(wall).colliderect(pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)):
                game_close = True

        draw_snake(snake_list)
        # --- PERUBAHAN 2: Tampilkan kecepatan saat ini di layar ---
        score_text = f"Skor: {snake_length - 1} | Kecepatan: {int(current_speed)}"
        draw_text(score_text, BLACK, WIDTH / 2, 30)
        pygame.display.update()

        if x == foodx and y == foody:
            snake_length += 1
            if eat_sound:
                eat_sound.play()
            
            # --- PERUBAHAN 3: Logika peningkatan kecepatan ---
            current_score = snake_length - 1
            if current_score > 0 and current_score % 5 == 0:
                current_speed += speed_increment
                print(f"Skor mencapai {current_score}! Kecepatan meningkat menjadi: {current_speed}")

            while True:
                foodx = round(random.randrange(BLOCK_SIZE, WIDTH - 2 * BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                foody = round(random.randrange(BLOCK_SIZE, HEIGHT - 2 * BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
                
                food_in_wall = any(pygame.Rect(w).colliderect(foodx, foody, BLOCK_SIZE, BLOCK_SIZE) for w in walls)
                food_in_snake = any([foodx, foody] == seg for seg in snake_list)

                if not food_in_wall and not food_in_snake:
                    break
        
        # --- PERUBAHAN 4: Gunakan variabel kecepatan dinamis ---
        clock.tick(current_speed)

    pygame.quit()
    quit()

def main():
    while True:
        gameLoop()

if __name__ == '__main__':
    main()