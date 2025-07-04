import pygame
import random
import os

pygame.init()

# Warna
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 255)
gray = (180, 180, 180)

# Ukuran layar & blok
width = 600
height = 400
block = 20
speed = 15

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Snake dengan Sound & Grid")

font = pygame.font.SysFont("comicsansms", 25)
clock = pygame.time.Clock()

# Load suara makan
try:
    eat_sound = pygame.mixer.Sound("suara_makan.mp3")
except:
    eat_sound = None
    print("⚠️ Suara tidak ditemukan! Pastikan file eat.wav ada di folder ini.")

# Gambar tulisan
def draw_text(msg, color, x, y):
    text = font.render(msg, True, color)
    win.blit(text, [x, y])

# Gambar ular
def draw_snake(snake_list):
    for x in snake_list:
        pygame.draw.rect(win, green, [x[0], x[1], block, block])

# Gambar tembok
def draw_walls():
    wall_thickness = block
    pygame.draw.rect(win, black, [0, 0, width, wall_thickness])
    pygame.draw.rect(win, black, [0, height - wall_thickness, width, wall_thickness])
    pygame.draw.rect(win, black, [0, 0, wall_thickness, height])
    pygame.draw.rect(win, black, [width - wall_thickness, 0, wall_thickness, height])

# Gambar grid tiap blok
def draw_grid():
    for x in range(0, width, block):
        pygame.draw.line(win, gray, (x, 0), (x, height))
    for y in range(0, height, block):
        pygame.draw.line(win, gray, (0, y), (width, y))

# Menu awal
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

# Game utama
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
                    game_over = True; game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True; game_close = False
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

        if x < block or x >= width - block or y < block or y >= height - block:
            game_close = True

        win.fill(white)
        draw_grid()
        draw_walls()
        pygame.draw.rect(win, red, [foodx, foody, block, block])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
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

# Mulai game
game_intro()
gameLoop()
