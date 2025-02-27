#!/usr/bin/env python3


import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Original and target resolutions
original_width, original_height = 1900, 890
target_width, target_height = 480, 320

# Calculate scaling factors
scale_x = target_width / (original_width*0.7)
scale_y = target_height / original_height

# Set up the display
screen = pygame.display.set_mode((target_width, target_height), pygame.FULLSCREEN)

# Load and scale images
background = pygame.transform.scale(pygame.image.load("background.jpg"), (target_width, target_height))
reticle = pygame.image.load("reticle.png")
reticle = pygame.transform.scale(reticle, (int(reticle.get_width() * scale_x), int(reticle.get_height() * scale_y)))
reticle_width, reticle_height = reticle.get_size()

# Start button
start_button = pygame.Surface((int(250 * scale_x), int(100 * scale_y)))  # Scaled size
start_button.fill((0, 150, 0))  # Green color for the start button
start_button_text = pygame.font.SysFont("Lucida Console", int(50 * scale_y)).render("START", True, (255, 255, 255))

# X button
x_button_width, x_button_height = int(50 * scale_x), int(50 * scale_y)  # Size of the X button
x_button = pygame.Surface((x_button_width, x_button_height))
x_button.fill((255, 0, 0))  # Red color for the X button
x_button_text = pygame.font.SysFont("Lucida Console", int(30 * scale_y)).render("X", True, (255, 255, 255))  # White "X" text

# Ducks
mduck = pygame.image.load("midduck.png")
mduck = pygame.transform.scale(mduck, (int(mduck.get_width() * scale_x), int(mduck.get_height() * scale_y)))
mduck_width, mduck_height = mduck.get_size()

mduck_left = pygame.image.load("midduckleft.png")
mduck_left = pygame.transform.scale(mduck_left, (int(mduck_left.get_width() * scale_x), int(mduck_left.get_height() * scale_y)))
mduck_left_width, mduck_left_height = mduck_left.get_size()

# Eagle
eagle = pygame.image.load("eagle.png")
eagle = pygame.transform.scale(eagle, (int(eagle.get_width() * scale_x), int(eagle.get_height() * scale_y)))
eagle_width, eagle_height = eagle.get_size()

# Explosion
explosion = pygame.image.load("bang.png")
explosion = pygame.transform.scale(explosion, (int(explosion.get_width() * scale_x), int(explosion.get_height() * scale_y)))
explosion_width, explosion_height = explosion.get_size()

# Duck positions and speeds
mduck_x = 0
mduck_y = int(200 * scale_y)
mduck_speed = 2*scale_x*0.1

mduck_left_x = target_width
mduck_left_y = int(300 * scale_y)
mduck_left_speed = 2*scale_x*0.1

# Other variables
savedx = 0
savedy = 0
score = 0
bonus_time = 0

# Fonts
font = pygame.font.SysFont("Lucida Console", int(50 * scale_y))
bonus_font = pygame.font.SysFont("Lucida Console", int(100 * scale_y))

# Hide the system cursor
pygame.mouse.set_visible(False)

game_started = False

# Speed weights
speed_choices1 = [2.5*scale_x*0.2, 3*scale_x*0.2, 4*scale_x*0.2, 5*scale_x*0.2, 6*scale_x*0.2]
speed_weights1 = [4, 4, 4, 3, 3]

speed_choices2 = [2*scale_x*0.2, 3*scale_x*0.2, 4*scale_x*0.2, 5*scale_x*0.2]
speed_weights2 = [4, 4, 4, 3]

def randomize_speed1():
    return random.choices(speed_choices1, weights=speed_weights1, k=1)[0]

def randomize_speed2():
    return random.choices(speed_choices2, weights=speed_weights2, k=1)[0]

# Main loop
running = True
explosion_time = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Check if the X button is clicked
            if int(target_width - x_button_width) <= mouse_x <= int(target_width) and 0 <= mouse_y <= x_button_height:
                running = False  # Exit the program

            if not game_started and start_button.get_rect(topleft=(int(550 * scale_x), int(395 * scale_y))).collidepoint(mouse_x, mouse_y):
                game_started = True



            # Golden eagle check
            if game_started and mduck_x <= mouse_x <= mduck_x + mduck_width and mduck_y <= mouse_y <= mduck_y + mduck_height and mduck_speed == (6*scale_x*0.2):
                score += 18 * (mduck_speed/(scale_x*0.05))
                savedx, savedy = mduck_x, mduck_y
                mduck_x = -(mduck_width + random.randint(int(1000 * scale_x), int(2000 * scale_x)))
                mduck_y = random.randint(int(25 * scale_y), int(775 * scale_y))
                mduck_speed = randomize_speed1()
                explosion_time = time.time()
                bonus_time = time.time()

            # Right-moving duck
            elif game_started and mduck_x <= mouse_x <= mduck_x + mduck_width and mduck_y <= mouse_y <= mduck_y + mduck_height:
                score += 10 * (mduck_speed/(scale_x*0.05))
                savedx, savedy = mduck_x, mduck_y
                mduck_x = -(mduck_width + random.randint(int(200 * scale_x), int(400 * scale_x)))
                mduck_y = random.randint(int(25 * scale_y), int(775 * scale_y))
                mduck_speed = randomize_speed1()
                explosion_time = time.time()

            # Left-moving duck
            elif game_started and mduck_left_x <= mouse_x <= mduck_left_x + mduck_left_width and mduck_left_y <= mouse_y <= mduck_left_y + mduck_left_height:
                score += 10 * (mduck_left_speed/(scale_x*0.05))
                savedx, savedy = mduck_left_x, mduck_left_y
                mduck_left_x = target_width + random.randint(int(200 * scale_x), int(400 * scale_x))
                mduck_left_y = random.randint(int(25 * scale_y), int(775 * scale_y))
                mduck_left_speed = randomize_speed2()
                explosion_time = time.time()

    if game_started:
        mduck_x += mduck_speed
        if mduck_x > target_width:
            mduck_x = -(mduck_width + random.randint(int(1800 * scale_x), int(3000 * scale_x)))
            mduck_y = random.randint(int(25 * scale_y), int(775 * scale_y))
            mduck_speed = randomize_speed1()

        mduck_left_x -= mduck_left_speed
        if mduck_left_x < -mduck_left_width:
            mduck_left_x = target_width + random.randint(int(1800 * scale_x), int(3000 * scale_x))
            mduck_left_y = random.randint(int(25 * scale_y), int(775 * scale_y))
            mduck_left_speed = randomize_speed2()

    # Draw background and elements
    screen.blit(background, (0, 0))
    
    if explosion_time > 0 and time.time() - explosion_time < 0.19:
        screen.blit(explosion, (savedx + mduck_width // 2 - explosion_width // 2, savedy + mduck_height // 2 - explosion_height // 2))
    else:
        explosion_time = 0

    if not game_started:
        screen.blit(start_button, (int(550 * scale_x), int(395 * scale_y)))
        screen.blit(start_button_text, (int(600 * scale_x), int(420 * scale_y)))

    # Display ducks and eagle
    screen.blit(eagle if mduck_speed == (6*scale_x*0.2) else mduck, (mduck_x, mduck_y))
    screen.blit(mduck_left, (mduck_left_x, mduck_left_y))


     # Display "BONUS!" message
    if bonus_time > 0 and time.time() - bonus_time < 2:
        bonus_text = bonus_font.render("BONUS!", True, (255, 215, 0))
        screen.blit(bonus_text, (int(940 * scale_x), int(500 * scale_y)))

    # Draw the X button in the top-right corner
    screen.blit(x_button, (int(target_width - x_button_width), 0))  # Draw the button
    screen.blit(x_button_text, (int(target_width - x_button_width // 2 - x_button_text.get_width() // 2), 
    int(x_button_height // 2 - x_button_text.get_height() // 2)))  # Center the text

    if game_started:
        score_text = font.render(f"Score: {int(score)}", True, (255, 255, 255))
        screen.blit(score_text, (int(900 * scale_x), int(800 * scale_y)))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    screen.blit(reticle, (mouse_x - reticle_width // 2, mouse_y - reticle_height // 2))
    pygame.display.flip()

pygame.quit()
