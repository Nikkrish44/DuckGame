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
 

mduck = pygame.image.load("midduck.png")  # Replace with your duck image path
mduck_width, mduck_height = mduck.get_size()

explosion = pygame.image.load("bang.png")  # Replace with your explosion (bang) image path
explosion_width, explosion_height = explosion.get_size()

# Duck starting position and speed
mduck_x = 0
mduck_y = 200  # Set the vertical position
mduck_speed = 2  # Speed of the duck's horizontal movement

savedx = 0
savedy = 0
score = 0
font = pygame.font.Font(None, 36)  # Default font, size 36
explosion_time = 0  # Time when the explosion was triggered


# Timer for the duck's random reappearance
last_appearance_time = pygame.time.get_ticks()
duck_appear_delay = random.randint(3000, 7000)  # Random delay between 3 to 7 seconds for duck appearance

#hide the system cursor
pygame.mouse.set_visible(False)

# Main loop
running = True

pygame.display.flip()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click is within the duck's bounds
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mduck_x <= mouse_x <= mduck_x + mduck_width and mduck_y <= mouse_y <= mduck_y + mduck_height:
                score += 10  # Increment score by 10 if duck is clicked
                savedx = mduck_x
                savedy = mduck_y
                mduck_x = -mduck_width
                explosion_time = time.time()
                
    current_time = pygame.time.get_ticks()

    if mduck_x <= -mduck_width or current_time - last_appearance_time >= duck_appear_delay:
        mduck_x = -mduck_width  # Reset duck position off-screen
        last_appearance_time = current_time  # Update the last appearance time
        duck_appear_delay = random.randint(3000, 7000)  # Set new random delay for next appearance

    mduck_x += mduck_speed
    if mduck_x > 1900:  # If the duck goes off the screen, reset its position
        mduck_x = -mduck_width
   # Get the current mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Draw the background
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))  # Draw the background image at (0, 0)
    
    if explosion_time > 0 and time.time() - explosion_time < 0.19:  # Display explosion for 0.3 seconds
        screen.blit(explosion, (savedx + mduck_width // 2 - explosion_width // 2, savedy + mduck_height // 2 - explosion_height // 2))
        mduck_x = -mduck_width
    else:
        explosion_time = 0  # Reset explosion time after 0.3 seconds


    
    screen.blit(mduck, (mduck_x, mduck_y))

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))  # White text
    screen.blit(score_text, (1700, 850))  # Bottom right corner (adjust as needed)


    screen.blit(reticle, (mouse_x - reticle_width // 2, mouse_y - reticle_height // 2))  # Center the reticle
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()