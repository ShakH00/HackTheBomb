import pygame
from pygame.locals import *
import sys
import pygbag

# Initialize Pygame
pygame.init()

# Set the screen dimensions and create the screen object
WIDTH = 1366
HEIGHT = 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HackTheBomb")
icon = pygame.image.load("graphics/icon.png")
pygame.display.set_icon(icon)

# Main Text
main_text = pygame.image.load("graphics/main_text.png")

# Font setup for fading text
font = pygame.font.Font(None, 50)
fade_text = "Press SPACE to play"
text_color = (255, 255, 255)
fade_alpha = 0
fade_speed = 5
increasing = True


"""Display the main screen"""
def main_screen():
    global fade_alpha, increasing
    running = True
    clock = pygame.time.Clock()

    # Load background once before the loop
    background_image = pygame.image.load("graphics/placeholder_bg.png")

    while running:
        screen.blit(background_image, (0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    main_game()
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Draw the main text
        main_text_rect = main_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(main_text, main_text_rect)

        # Fade in and fade out effect
        if increasing:
            fade_alpha += fade_speed
            if fade_alpha >= 255:
                fade_alpha = 255
                increasing = False
        else:
            fade_alpha -= fade_speed
            if fade_alpha <= 50:
                fade_alpha = 50
                increasing = True

        # Display fading text
        fade_surface = font.render(fade_text, True, text_color)
        fade_surface.set_alpha(fade_alpha)
        text_rect = fade_surface.get_rect(center=(WIDTH // 2, HEIGHT * 3 // 4))
        screen.blit(fade_surface, text_rect)

        # Update the display
        pygame.display.flip()
        clock.tick(60)


def main_game():
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))

        # Update the display
        pygame.display.flip()
        clock.tick(60)


# Run the main screen function
main_screen()

# Quit Pygame
pygame.quit()
sys.exit()
