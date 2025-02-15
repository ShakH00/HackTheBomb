import pygame
import sys
import time

pygame.init()
pygame.font.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1000
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

def show_text_window():
    # Set up the text window
    text_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Text Window")

    # Fill the text window with black color
    text_window.fill((0, 0, 0))

    # Render text with typing effect
    font = pygame.font.SysFont(None, 36)
    text = "While on a train, you receive a text message:"
    text_surface = font.render('', True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 6))
    text_window.blit(text_surface, text_rect)
    pygame.display.update()

    # Typing effect for main message
    for i in range(len(text) + 1):
        text_surface = font.render(text[:i], True, (255, 255, 255))
        text_window.blit(text_surface, text_rect)
        pygame.display.update()
        time.sleep(0.03)

    # Wait for a few seconds
    time.sleep(1)

    # Load and scale the additional images
    image1 = pygame.image.load("phone.jpg").convert_alpha()
    image1 = pygame.transform.scale(image1, (300, 300))  # Adjust size as needed

    image2 = pygame.image.load("mesg.png").convert_alpha()
    image2 = pygame.transform.scale(image2, (400, 300))  # Adjust size as needed

    for alpha in range(0, 255, 5):  # Increase transparency gradually
        text_window.fill((0, 0, 0))  # Clear the window
        text_window.blit(text_surface, text_rect)  # Re-blit the text
        faded_image1 = image1.copy()  # Create a copy of the image
        faded_image1.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)  # Apply alpha value
        image_rect1 = faded_image1.get_rect(midright=(SCREEN_WIDTH - 250, SCREEN_HEIGHT // 2))
        text_window.blit(faded_image1, image_rect1)  # Blit the faded image
        faded_image2 = image2.copy()  # Create a copy of the image
        faded_image2.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)  # Apply alpha value
        image_rect2 = faded_image2.get_rect(center=(900, 400))  # Adjust x and y coordinates as needed
        text_window.blit(faded_image2, image_rect2)  # Blit the faded image
        pygame.display.update()
        pygame.time.delay(15)  # Delay for smoother animation

    # Add a button
    button_font = pygame.font.Font(None, 36)
    button_color = (184, 134, 11)
    button_width, button_height = 320, 50
    button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT - 320, button_width, button_height)
    pygame.draw.rect(text_window, button_color, button_rect)
    button_text = button_font.render("OK, I'm calling for help", True, (255, 255, 255))
    text_window.blit(button_text, button_text.get_rect(center=button_rect.center))
    pygame.display.update()

    time.sleep(1)
    # Add additional text below the button
    additional_text = "Civilian count in the blast zone : 250"
    additional_text_surface = font.render(additional_text, True, (255, 255, 255))
    additional_text_rect = additional_text_surface.get_rect(center=(SCREEN_WIDTH // 2, button_rect.bottom + 50))
    text_window.blit(additional_text_surface, additional_text_rect)
    pygame.display.update()
    time.sleep(1)

    # Add one more text below the additional text
    more_text = "Evacuation currently impossible"
    more_text_surface = font.render(more_text, True, (255, 255, 255))
    more_text_rect = more_text_surface.get_rect(center=(SCREEN_WIDTH // 2, additional_text_rect.bottom + 50))
    text_window.blit(more_text_surface, more_text_rect)
    pygame.display.update()

    # Handle button click event
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                   print("hi")

if __name__ == "__main__":
    show_text_window()
