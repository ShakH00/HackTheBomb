import pygame
from pygame.locals import *
import sys
import subprocess

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
fade_text = "Press SPACE or click START to play"
text_color = (255, 255, 255)
fade_alpha = 0
fade_speed = 5
increasing = True

# Button setup
button_color = (255, 200, 255)
button_hover_color = (255, 170, 255)
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
button_font = pygame.font.Font(None, 40)
button_text = button_font.render("START", True, (0, 0, 0))
button_scale = 1.0
button_target_scale = 1.0
button_radius = 10


"""Display the main screen"""
def main_screen():
    global fade_alpha, increasing, button_scale, button_target_scale
    running = True
    clock = pygame.time.Clock()

    # Load background once before the loop
    background_image = pygame.image.load("graphics/placeholder_bg.png")

    while running:
        screen.blit(background_image, (0, 0))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        hovered = button_rect.collidepoint(mouse_pos)

        # Event handler
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
            elif event.type == MOUSEBUTTONDOWN and hovered:
                main_game()

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

        if hovered:
            button_target_scale = 1.1
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            button_target_scale = 1.0
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Smooth hover effect
        button_scale += (button_target_scale - button_scale) * 0.1

        scaled_width = int(200 * button_scale)
        scaled_height = int(50 * button_scale)
        scaled_button = pygame.Surface((scaled_width, scaled_height), pygame.SRCALPHA)
        pygame.draw.rect(scaled_button, button_hover_color if hovered else button_color, (0, 0, scaled_width, scaled_height), border_radius=button_radius)
        scaled_button_rect = scaled_button.get_rect(center=button_rect.center)
        screen.blit(scaled_button, scaled_button_rect)
        screen.blit(button_text, button_text.get_rect(center=scaled_button_rect.center))

        pygame.display.flip()
        clock.tick(60)


def main_game():
    try:
        # Run player1 and player2 as separate processes
        subprocess.Popen([sys.executable, "player1.py"])
        subprocess.Popen([sys.executable, "player2.py"])
    except Exception as e:
        print(f"Error launching player scripts: {e}")

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
