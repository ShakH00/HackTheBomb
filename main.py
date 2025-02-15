import pygame
from pygame.locals import *
import sys
import pygbag


# Initialize Pygame
pygame.init()

# Set the screen dimensions and create the screen object
screen_width = 1366
screen_height = 768
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("HackTheBomb")
icon = pygame.image.load("graphics/icon.png")
pygame.display.set_icon(icon)

# Main Text
main_text = pygame.image.load("graphics/main_text.png")

def main_screen():
    """Display the main screen with emojis"""
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

            # Fill the screen with the background image
            background_image = pygame.image.load("graphics/placeholder_bg.png")
            screen.blit(background_image, (0, 0))

            # Get dimensions of main_text image
            main_text_rect = main_text.get_rect(center=(screen_width // 2, screen_height // 4))
            screen.blit(main_text, main_text_rect)

        # Update the display
        pygame.display.flip()


# Run the main screen function
main_screen()

# Quit Pygame
pygame.quit()
sys.exit()
