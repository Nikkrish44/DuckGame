import pygame
import time
import random
# Initialize Pygame
pygame.init()


# Set up the display
screen = pygame.display.set_mode((1900, 890))
pygame.display.set_caption("Reticle Following Cursor")

# Load background image
background = pygame.image.load("background.jpg")  # Replace with your background image path


reticle = pygame.image.load("reticle.png")
reticle_width, reticle_height = reticle.get_size()
 
#load first duck
mduck = pygame.image.load("midduck.png")  # Replace with your duck image path
mduck_width, mduck_height = mduck.get_size()

# Load the second (left-facing) duck
mduck_left = pygame.image.load("midduckleft.png")  # Left-facing duck
mduck_left_width, mduck_left_height = mduck_left.get_size()

#load eagle
eagle = pygame.image.load("eagle.png") 
eagle_width, eagle_height = eagle.get_size()

explosion = pygame.image.load("bang.png")  # Replace with your explosion (bang) image path
explosion_width, explosion_height = explosion.get_size()

# Duck starting position and speed
mduck_x = 0
mduck_y = 200  # Set the vertical position
mduck_speed = 2  # Speed of the duck's horizontal movement

mduck_left_x = 1900  # Start from the right side of the screen
mduck_left_y = 300
mduck_left_speed = 2  # Speed of the left-facing duck

savedx = 0
savedy = 0
score = 0
bonus_time = 0

font = pygame.font.SysFont("Lucida Console", 50)  # Using Arial font with size 36
bonus_font = pygame.font.SysFont("Lucida Console", 100)  # Larger font size for "BONUS!"
explosion_time = 0  # Time when the explosion was triggered

#hide the system cursor
pygame.mouse.set_visible(False)

# Main loop
running = True

# Set weights for speeds: 
speed_choices1 = [2.5, 3, 4, 5, 6]
speed_weights1 = [4, 4, 4, 3, 1]  # Weights: higher value = higher likelihood

def randomize_speed1():
    return random.choices(speed_choices1, weights=speed_weights1, k=1)[0]

# Set weights for speeds: 
speed_choices2 = [2, 3, 4, 5]
speed_weights2 = [4, 4, 4, 3]  # Weights: higher value = higher likelihood

def randomize_speed2():
    return random.choices(speed_choices2, weights=speed_weights2, k=1)[0]


pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            


             # Check golden eagle case
            if mduck_x <= mouse_x <= mduck_x + mduck_width and mduck_y <= mouse_y <= mduck_y + mduck_height and mduck_speed == 6:
                score += 18*mduck_speed  # Increment score by 10 if duck is clicked
                score = round(score)  # Ensures score is a whole number
                savedx = mduck_x
                savedy = mduck_y
                mduck_x = -(mduck_width + random.randint(1500, 3000))
                mduck_y = random.randint(25, 775)
                mduck_speed = randomize_speed1()  # Randomize speed after duck is clicked
                explosion_time = time.time()
                bonus_time = time.time()

            # Check if the click is within the right moving duck's bounds
            if mduck_x <= mouse_x <= mduck_x + mduck_width and mduck_y <= mouse_y <= mduck_y + mduck_height:
                score += 10*mduck_speed  # Increment score by 10 if duck is clicked
                score = round(score)  # Ensures score is a whole number
                savedx = mduck_x
                savedy = mduck_y
                mduck_x = -(mduck_width + random.randint(1500, 3000))
                mduck_y = random.randint(25, 775)
                mduck_speed = randomize_speed1()  # Randomize speed after duck is clicked
                explosion_time = time.time()
                
             # Check if the click is within the left moving duck's bounds
            elif mduck_left_x <= mouse_x <= mduck_left_x + mduck_left_width and mduck_left_y <= mouse_y <= mduck_left_y + mduck_left_height:
                score += 10*mduck_left_speed  # Increment score by 10 if duck is clicked
                score = round(score)  # Ensures score is a whole number
                savedx = mduck_left_x
                savedy = mduck_left_y
                mduck_left_x = +(mduck_left_width + random.randint(2800, 3100))
                mduck_left_y = random.randint(25, 775)
                mduck_left_speed = randomize_speed2()  # Randomize speed after duck is clicked
                explosion_time = time.time()

    #move right moving duck           
    mduck_x += mduck_speed

    if mduck_x > 1900+mduck_width:  # If the duck goes off the screen, reset its position
        mduck_x = -(mduck_width + random.randint(1800, 3000))
        mduck_y = random.randint(25, 775)
        mduck_speed = randomize_speed1()

   #move left moving duck           
    mduck_left_x -= mduck_left_speed

    if mduck_left_x < -mduck_left_width:  # If the duck goes off the screen, reset its position
        mduck_left_x = +(mduck_left_width + random.randint(1800, 3000))
        mduck_left_y = random.randint(25, 775)
        mduck_left_speed = randomize_speed2()

   # Get the current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Draw the background
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))  # Draw the background image at (0, 0)
    
    if explosion_time > 0 and time.time() - explosion_time < 0.19:  # Display explosion for 0.19 seconds
        screen.blit(explosion, (savedx + mduck_width // 2 - explosion_width // 2, savedy + mduck_height // 2 - explosion_height // 2))
    else:
        explosion_time = 0  # Reset explosion time after 0.3 seconds


    
    # Draw eagle if eagle is hit
    if(mduck_speed == 6):
        screen.blit(eagle, (mduck_x, mduck_y))
    else: 
        screen.blit(mduck, (mduck_x, mduck_y))  # Right-facing duck
    screen.blit(mduck_left, (mduck_left_x, mduck_left_y))  # Left-facing duck


    if bonus_time > 0 and time.time() - bonus_time < 2:  # Display "BONUS!" for 1 second
        bonus_text = bonus_font.render("BONUS!", True, (255, 215, 0))  # Gold colored text
        screen.blit(bonus_text, (1500, 500))  # Display the message above the score


    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
    screen.blit(score_text, (1500, 800))  # Bottom right corner (adjust as needed)


    screen.blit(reticle, (mouse_x - reticle_width // 2, mouse_y - reticle_height // 2))  # Center the reticle
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
