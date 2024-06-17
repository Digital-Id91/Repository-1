import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 225, 0)
YELLOW = (255, 255, 0)
PELLET_RADIUS = 7  
GHOST_RADIUS = 25
NUM_PELLETS = 3  # Number of pellets

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("JetBrains")

# JetBrains attributes
jetbrains_x = WIDTH // 2
jetbrains_y = HEIGHT // 2
jetbrains_direction = 0  # 0: right, 1: up, 2: left, 3: down
jetbrains_speed = 5  

# Pellet attributes
pellets = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(NUM_PELLETS)]

# Ghost attributes
ghosts = [[400, 100, 0, 0], [100, 400, 0, 0]]  # x, y, x_direction, y_direction for two ghosts
ghost_speed = 2

# Score
score = 0

# Game over attributes
game_over = False

# Check if all pellets have been eaten
def check_win_condition():
    return len(pellets) == 0

def update_jetbrains_position():
    global jetbrains_x, jetbrains_y
    if jetbrains_direction == 0:
        jetbrains_x += jetbrains_speed
    elif jetbrains_direction == 1:
        jetbrains_y -= jetbrains_speed
    elif jetbrains_direction == 2:
        jetbrains_x -= jetbrains_speed
    elif jetbrains_direction == 3:
        jetbrains_y += jetbrains_speed

def eat_pellet():
    global score
    for pellet in pellets:
        distance = pygame.math.Vector2(jetbrains_x - pellet[0], jetbrains_y - pellet[1]).length()
        if distance < PELLET_RADIUS * 2:  # size of PELLET
            pellets.remove(pellet)
            score += 1

def draw_pellets():
    for pellet in pellets:
        pygame.draw.circle(screen, YELLOW, pellet, PELLET_RADIUS)

def draw_ghosts():
    for ghost in ghosts:
        pygame.draw.circle(screen, RED, (int(ghost[0]), int(ghost[1])), GHOST_RADIUS)

def move_ghosts():
    for ghost in ghosts:
        # Simple chase behavior: move towards JetBrains
        if jetbrains_x < ghost[0]:
            ghost[2] = -1  # Move left
        elif jetbrains_x > ghost[0]:
            ghost[2] = 1   # Move right
        else:
            ghost[2] = 0   # Stop in the x direction

        if jetbrains_y < ghost[1]:
            ghost[3] = -1  # Move up
        elif jetbrains_y > ghost[1]:
            ghost[3] = 1   # Move down
        else:
            ghost[3] = 0   # Stop in the y direction

        ghost[0] += ghost[2] * ghost_speed  # Move in x direction
        ghost[1] += ghost[3] * ghost_speed  # Move in y direction

def handle_ghost_collision():
    global game_over
    for ghost in ghosts:
        distance = pygame.math.Vector2(jetbrains_x - ghost[0], jetbrains_y - ghost[1]).length()
        if distance < PELLET_RADIUS + GHOST_RADIUS:  # size of the ghosts
            game_over = True

# Main game loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_RIGHT:
                jetbrains_direction = 0
            elif event.key == pygame.K_UP:
                jetbrains_direction = 1
            elif event.key == pygame.K_LEFT:
                jetbrains_direction = 2
            elif event.key == pygame.K_DOWN:
                jetbrains_direction = 3

    if not game_over:
        update_jetbrains_position()
        eat_pellet()
        move_ghosts()
        handle_ghost_collision()

        # Check if all pellets have been eaten
        if check_win_condition():
            game_over = True

        # Boundary checking for JetBrains
        jetbrains_x = max(PELLET_RADIUS, min(WIDTH - PELLET_RADIUS, jetbrains_x))
        jetbrains_y = max(PELLET_RADIUS, min(HEIGHT - PELLET_RADIUS, jetbrains_y))

    # Draw the game window
    screen.fill(BLACK)
    draw_pellets()
    draw_ghosts()
    pygame.draw.circle(screen, BLUE, (jetbrains_x, jetbrains_y), PELLET_RADIUS)

    if game_over:
        if check_win_condition():
            font = pygame.font.Font(None, 72)
            win_text = font.render("YOU WIN!!!", True, GREEN)
            screen.blit(win_text, (WIDTH // 2 - 200, HEIGHT // 2 - 36))
        else:
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("Game Over!!!", True, RED)
            screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2 - 36))

    else:
        # Draw the score on the screen
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLUE)
        screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)