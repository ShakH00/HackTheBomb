import pygame
import sys


def game_completed():
    # Initialize Pygame
    pygame.init()

    # Get screen dimensions
    SCREEN_WIDTH = pygame.display.Info().current_w
    SCREEN_HEIGHT = pygame.display.Info().current_h
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Centered Image")

    # Load image
    image = pygame.image.load("newspaper_completed.jpg")
    image.set_alpha(0)  # Set initial transparency level to fully transparent

    # Get image dimensions
    image_rect = image.get_rect()

    # Calculate position to center image on screen
    image_x = (SCREEN_WIDTH - image_rect.width) // 2
    image_y = (SCREEN_HEIGHT - image_rect.height) // 2

    # Define button parameters
    button_width = 200
    button_height = 50
    button_x = (SCREEN_WIDTH - button_width) // 2
    button_y = SCREEN_HEIGHT - 100
    button_color = (0, 0, 0)  # Black color

    # Create font object
    font = pygame.font.SysFont(None, 30)

    # Create text surface and get its rect
    text_surface = font.render("Main Menu", True, (255, 255, 255))  # White text color
    text_rect = text_surface.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))

    # Main loop
    fade_in_speed = 5  # Speed of fade-in effect
    alpha_value = 0  # Initial alpha value for the image
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[
                    1] <= button_y + button_height:
                    print("Button clicked!")  # Placeholder for button action

        # Fill the screen with white color
        screen.fill((255, 255, 255))

        # Blit image onto the screen at the calculated position with the current alpha value
        screen.blit(image, (image_x, image_y))

        # Increase alpha value gradually until it reaches 255 (fully opaque)
        if alpha_value < 255:
            alpha_value += fade_in_speed
            if alpha_value > 255:
                alpha_value = 255
            image.set_alpha(alpha_value)

        # Draw the button
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        # Blit the text onto the button
        screen.blit(text_surface, text_rect)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()


# Call the function
game_completed()
