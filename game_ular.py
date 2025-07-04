import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Warna
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 255)
gray = (100, 100, 100)

# Ukuran layar
width = 600
height = 400

# Ukuran blok ular & kecepatan
block = 20
speed = 15

# Setup layar
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Snake by Hayyan")

# Font
font = pygame.font.SysFont("comicsansms", 25)

clock = pygame.time.Clock()

# Fungsi tampilkan teks
def draw_text(msg, color, x, y):
    text = font.render(msg, True, color)
    win.blit(text, [x, y])

# Fungsi untuk menggambar ular
def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(win, green, [x[0], x[1], block, block])

# Fungsi gambar tembok
def draw_walls():
    wall_thickness = block
    pygame.draw.rect(win, gray, [0, 0, width, wall_thickness])  # atas
    pygame.draw.rect(win, gray, [0, height - wall_thickness, width, wall_thickness])  # bawah
    pygame.draw.rect(win, gray, [0, 0, wall_thickness, height])  # kiri
    pygame.draw.rect(win, gray, [width - wall_thickness, 0, wall_thickness, height])  # kanan

# Menu Awal
def game_intro():
    intro = True
    while intro:
        win.fill(white)
        draw_text("Selamat Datang di Game Snake!", blue, 100, 100)
        draw_text("Tekan [SPASI] untuk Mulai atau [Q] untuk Keluar", black, 60, 150)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit(); quit()
                if event.key == pygame.K_SPACE:
                    intro = False

# Fungsi utama game
def gameLoop():
    game_over = False
    game_close = False

    x = width // 2
    y = height // 2
    x_change = block
    y_change = 0

    snake_list = []
    snake_length = 1

    foodx = round(random.randrange(block, width - 2 * block) / block) * block
    foody = round(random.randrange(block, height - 2 * block) / block) * block

    while not game_over:

        while game_close:
            win.fill(white)
            draw_text("KAMU KALAH! Tekan [C] untuk Coba Lagi atau [Q] untuk Keluar", red, 30, height // 3)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # tombol input di dalam game
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

        # Cek tabrakan dengan tembok
        if x < block or x >= width - block or y < block or y >= height - block:
            game_close = True

        win.fill(white)
        draw_walls()
        pygame.draw.rect(win, red, [foodx, foody, block, block])

        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Cek tabrakan dengan badan sendiri
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_list)
        draw_text(f"Skor: {snake_length - 1}", black, 10, 10)

        pygame.display.update()

        # Cek jika makan makanan
        if x == foodx and y == foody:
            foodx = round(random.randrange(block, width - 2 * block) / block) * block
            foody = round(random.randrange(block, height - 2 * block) / block) * block
            snake_length += 1

        clock.tick(speed)

    pygame.quit()
    quit()

# Jalankan game
game_intro()
gameLoop()
