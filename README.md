# sanke
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
BLOCK_SIZE = 20
FPS = 10

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Font for score
font = pygame.font.SysFont(None, 35)

def draw_snake(snake_body):
    for block in snake_body:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

def draw_food(food_pos):
    pygame.draw.rect(screen, RED, [food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE])

def get_random_food():
    x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
    return [x, y]

def game_loop():
    game_over = False
    game_close = False

    # Initial snake position and body
    snake_body = [[WIDTH // 2, HEIGHT // 2]]
    snake_length = 1

    # Initial direction
    direction = 'RIGHT'
    change_to = direction

    # Initial food
    food_pos = get_random_food()

    score = 0

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message = font.render("Game Over! Press Q to Quit or C to Play Again", True, WHITE)
            screen.blit(message, [WIDTH / 6, HEIGHT / 3])
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
                        game_loop()  # Restart the game

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'
                elif event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'

        # Update direction
        direction = change_to

        # Move snake head
        head = list(snake_body[0])
        if direction == 'LEFT':
            head[0] -= BLOCK_SIZE
        elif direction == 'RIGHT':
            head[0] += BLOCK_SIZE
        elif direction == 'UP':
            head[1] -= BLOCK_SIZE
        elif direction == 'DOWN':
            head[1] += BLOCK_SIZE

        # Check wall collision
        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT:
            game_close = True

        # Check self collision
        for block in snake_body[1:]:
            if block == head:
                game_close = True

        # Add new head
        snake_body.insert(0, head)

        # Check food collision
        if head == food_pos:
            food_pos = get_random_food()
            snake_length += 1
            score += 1

        # Remove tail if not grown
        if len(snake_body) > snake_length:
            snake_body.pop()

        # Draw everything
        screen.fill(BLACK)
        draw_food(food_pos)
        draw_snake(snake_body)

        # Display score
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, [10, 10])

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

# Start the game
game_loop()
