import pygame
import random
import socket

HOST = "127.0.0.1"
PORT = 3001

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

pygame.init()

WIDTH, HEIGHT = 800, 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CV Game")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

player_width, player_height = 50, 50
player_x = (WIDTH - player_width) // 2
player_y = HEIGHT - player_height
player_speed = 5

projectile_width, projectile_height = 10, 30
projectile_speed = 4
projectiles = []

score = 50
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
running = True
game_over = False

def draw_player():
    pygame.draw.rect(window, WHITE, (player_x, player_y, player_width, player_height))

def draw_projectiles():
    for projectile in projectiles:
        pygame.draw.rect(window, RED, (projectile[0], projectile[1], projectile_width, projectile_height))

def move_projectiles():
    for projectile in projectiles:
        projectile[1] += projectile_speed

def collision_detection():
    global score, game_over
    for projectile in projectiles:
        if player_y < projectile[1] + projectile_height and player_y + player_height > projectile[1]:
            if player_x < projectile[0] + projectile_width and player_x + player_width > projectile[0]:
                game_over = True
        if projectile[1] > HEIGHT:
            projectiles.remove(projectile)
            score += 1

def draw_score():
    text = font.render("Score: ", str(score), True, WHITE)
    window.blit(text, (10, 10))

def reset_game():
    global player_x, player_y, projectiles, score, game_over
    player_x = (WIDTH - player_width) // 2
    player_y = HEIGHT - player_height
    projectiles = []
    score = 0
    game_over = False

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        index_finger_x_str = client_socket.recv(1024).decode()

        if index_finger_x_str:
            try:
                index_finger_x = float(index_finger_x_str)
                player_x = (1 - index_finger_x) * (WIDTH - player_width)

                keys = pygame.key.get_pressed()
        
                if keys[pygame.K_LEFT] and player_x > 0:
                    player_x -= player_speed
                if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
                    player_x += player_speed

                if random.randint(0, 100) < 2:
                    projectiles.append([random.randint(0, WIDTH - projectile_width), 0])
    
                move_projectiles()
                collision_detection()
            except ValueError:
                pass
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            reset_game()
    
    window.fill((0, 0, 0))

    draw_player()
    draw_projectiles()
    draw_score()

    if game_over:
        text = font.render("Game Over! Press SPACE to play again.", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(text, text_rect)

    pygame.display.update()

pygame.quit()