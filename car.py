pip install pygame

import pygame
import random
import time

# Initialize pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Player car
player_width = 50
player_height = 60
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# Obstacle settings
obstacle_width = 50
obstacle_height = 60
obstacle_speed = 5
obstacles = []

# Font settings
font = pygame.font.SysFont("Arial", 30)
score_font = pygame.font.SysFont("Arial", 40)

# Game over screen
def game_over():
    game_over_text = font.render("GAME OVER", True, RED)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 3))
    restart_text = font.render("Press R to Restart", True, BLUE)
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2))
    pygame.display.update()

# Show score
def display_score(score):
    score_text = score_font.render(f"Score: {score}", True, GREEN)
    screen.blit(score_text, (10, 10))

# Create new obstacle
def create_obstacle():
    x_pos = random.randint(0, screen_width - obstacle_width)
    return pygame.Rect(x_pos, -obstacle_height, obstacle_width, obstacle_height)

# Main game loop
def game_loop():
    global player_x, player_y
    score = 0
    running = True
    game_over_flag = False

    while running:
        screen.fill(WHITE)

        # Check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over_flag and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game when 'R' is pressed
                    game_loop()

        # Movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed

        # Draw player car
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

        # Create new obstacles and move them
        if not game_over_flag:
            if random.random() < 0.02:  # 2% chance to spawn a new obstacle per frame
                obstacles.append(create_obstacle())

        # Move obstacles
        for obstacle in obstacles:
            obstacle.y += obstacle_speed
            pygame.draw.rect(screen, RED, obstacle)

            # Check for collision with player
            if obstacle.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
                game_over_flag = True

            # Remove obstacles that pass the bottom of the screen
            if obstacle.y > screen_height:
                obstacles.remove(obstacle)
                score += 1

        # Display score
        display_score(score)

        # Check for game over
        if game_over_flag:
            game_over()

        # Update the display
        pygame.display.update()

        # Control frame rate
        clock.tick(FPS)

# Run the game
game_loop()

# Quit pygame
pygame.quit()
