import pygame
import sys
import random

pygame.init()

# Game window dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Define basic colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake starting position, speed, and food
snake_pos = [[100, 50], [90, 50], [80, 50]]
snake_speed = [10, 0]
food = {'pos': [0, 0], 'weight': 1, 'spawn_time': 0}
food_spawn = True
score = 0
level = 1
speed_increase = 0.1
food_counter = 0  # Counter for spawning weighted food

fps = pygame.time.Clock()

def check_collision(pos):
    # Check if snake collides with the screen borders or itself
    if pos[0] < 0 or pos[0] > SCREEN_WIDTH-10 or pos[1] < 0 or pos[1] > SCREEN_HEIGHT-10:
        return True
    if pos in snake_pos[1:]:
        return True
    return False

def get_random_food():
    # Generate a random position for food within the game field
    # and assign a weight based on the food counter
    global food_counter
    while True:
        pos = [random.randrange(1, (SCREEN_WIDTH//10)) * 10, random.randrange(1, (SCREEN_HEIGHT//10)) * 10]
        if pos not in snake_pos:
            weight = 2 if food_counter >= 2 else 1
            food_counter = 0 if weight == 2 else food_counter + 1
            return {'pos': pos, 'weight': weight, 'spawn_time': pygame.time.get_ticks()}

# Main game loop
# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # Use '==' instead of 'is' for comparison
            # Key press handling for snake control
            if event.key == pygame.K_UP and snake_speed[1] == 0:
                snake_speed = [0, -10]
            elif event.key == pygame.K_DOWN and snake_speed[1] == 0:
                snake_speed = [0, 10]
            elif event.key == pygame.K_LEFT and snake_speed[0] == 0:
                snake_speed = [-10, 0]
            elif event.key == pygame.K_RIGHT and snake_speed[0] == 0:
                snake_speed = [10, 0]


    snake_pos.insert(0, list(map(lambda x, y: x + y, snake_pos[0], snake_speed)))

    if check_collision(snake_pos[0]):
        pygame.quit()
        sys.exit()

    # Check if the snake has eaten the food
    if snake_pos[0] == food['pos']:
        score += food['weight']  # Increase score by the weight of the food
        if score % 3 == 0:  # Increase level every 3 points
            level += 1
            fps.tick(10 + level*speed_increase)  # Adjust the game speed based on level
        food_spawn = True
    else:
        snake_pos.pop()

    if food_spawn:
        food = get_random_food()
        food_spawn = False

    # Check if the food should disappear after 10 seconds
    current_time = pygame.time.get_ticks()
    if current_time - food['spawn_time'] > 10000:  # 10 seconds in milliseconds
        food_spawn = True

    screen.fill(BLACK)

    # Draw snake
    for pos in snake_pos:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw food with color intensity based on weight
    food_color = RED if food['weight'] == 1 else (255, 165, 0)  # Orange for weight 2
    pygame.draw.rect(screen, food_color, pygame.Rect(food['pos'][0], food['pos'][1], 10, 10))

    # Display the score and level
    font = pygame.font.SysFont('arial', 20)
    score_text = font.render(f"Score: {score} Level: {level}", True, WHITE)
    screen.blit(score_text, [0, 0])

    pygame.display.flip()
    fps.tick(10 + level*speed_increase)  # Control game speed
