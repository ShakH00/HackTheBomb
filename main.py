import pygame
from pygame.locals import *
import sys


# Initialize Pygame
pygame.init()

# Set the screen dimensions and create the screen object
screen_width = 900
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

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

        # Update the display
        pygame.display.flip()


# Run the main screen function
main_screen()

# Quit Pygame
pygame.quit()
sys.exit()
