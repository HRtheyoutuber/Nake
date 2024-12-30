import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Nake')

# Set up the clock for controlling the frame rate
clock = pygame.time.Clock()

# Snake settings
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = 'RIGHT'
change_to = snake_direction
speed = 15

# Food settings
food_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10)) * 10]
food_spawn = True

# Power-up settings
power_up_types = ['speed', 'extra_points']
power_up_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10)) * 10]
power_up_spawn = True
power_up_active = False
power_up_type = None
power_up_timer = 0

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Score
score = 0
font = pygame.font.SysFont('arial', 35)

def show_score(color, font, size):
    score_surface = font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (width / 2, 15)
    window.blit(score_surface, score_rect)

def game_over():
    window.fill(black)
    game_over_surface = font.render('Your Score is : ' + str(score), True, white)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (width / 2, height / 4)
    window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    pygame.time.sleep(3)
    pygame.quit()
    sys.exit()

def spawn_power_up():
    global power_up_pos, power_up_type, power_up_spawn
    power_up_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10)) * 10]
    power_up_type = random.choice(power_up_types)
    power_up_spawn = True

print("Starting main game loop...")
# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            elif event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Validate direction change
    if change_to == 'UP' and snake_direction != 'DOWN':
        snake_direction = change_to
    if change_to == 'DOWN' and snake_direction != 'UP':
        snake_direction = change_to
    if change_to == 'LEFT' and snake_direction != 'RIGHT':
        snake_direction = change_to
    if change_to == 'RIGHT' and snake_direction != 'LEFT':
        snake_direction = change_to

    # Move the snake
    if snake_direction == 'UP':
        snake_pos[1] -= 10
    if snake_direction == 'DOWN':
        snake_pos[1] += 10
    if snake_direction == 'LEFT':
        snake_pos[0] -= 10
    if snake_direction == 'RIGHT':
        snake_pos[0] += 10

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        food_spawn = False
        score += 10
    else:
        snake_body.pop()

    # Spawn new food
    if not food_spawn:
        food_pos = [random.randrange(1, (width//10)) * 10, random.randrange(1, (height//10)) * 10]
    food_spawn = True

    # Spawn new power-up
    if not power_up_spawn and not power_up_active:
        spawn_power_up()

    # Check if snake has collected a power-up
    if snake_pos == power_up_pos:
        power_up_spawn = False
        power_up_active = True
        power_up_timer = pygame.time.get_ticks()

        if power_up_type == 'speed':
            speed = 30
        elif power_up_type == 'extra_points':
            score += 50

    # Deactivate power-up after 10 seconds
    if power_up_active and pygame.time.get_ticks() - power_up_timer > 10000:
        power_up_active = False
        speed = 15

    # Fill the screen with black
    window.fill(black)

    # Draw the snake
    for pos in snake_body:
        pygame.draw.rect(window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw the food
    pygame.draw.rect(window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # Draw the power-up
    if power_up_spawn:
        if power_up_type == 'speed':
            pygame.draw.rect(window, red, pygame.Rect(power_up_pos[0], power_up_pos[1], 10, 10))
        elif power_up_type == 'extra_points':
            pygame.draw.rect(window, blue, pygame.Rect(power_up_pos[0], power_up_pos[1], 10, 10))

    # Game Over conditions
    # Snake hits the boundaries
    if snake_pos[0] < 0 or snake_pos[0] > width-10 or snake_pos[1] < 0 or snake_pos[1] > height-10:
        game_over()
    # Snake hits itself
    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    # Show score
    show_score(white, font, 35)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(speed)

print("Exiting game loop...")
# Quit Pygame
pygame.quit()
sys.exit()