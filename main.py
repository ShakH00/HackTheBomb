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

# Start buttons
expert = pygame.image.load("graphics/Expertlogo.jpg")
defuser = pygame.image.load("graphics/defuser.jpg")

expert = pygame.transform.scale(expert, (303, 303))
defuser = pygame.transform.scale(defuser, (300, 300))

# Main Text
main_text = pygame.image.load("graphics/main_text.png")

# Button rectangles for collision detection
expert_rect = expert.get_rect(topleft=(200, 350))
defuser_rect = defuser.get_rect(topleft=(1166 - 303, 350))

"""Display the main screen"""
def main_screen():
    running = True
    clock = pygame.time.Clock()

    # Load background once before the loop
    background_image = pygame.image.load("graphics/placeholder_bg.png")

    while running:
        screen.blit(background_image, (0, 0))

        # Logos on page
        screen.blit(expert, expert_rect.topleft)
        screen.blit(defuser, defuser_rect.topleft)

        # Change mouse cursor on hover
        if defuser_rect.collidepoint(pygame.mouse.get_pos()) or expert_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # Event handler
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    run_both()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                if defuser_rect.collidepoint(event.pos):
                    run_defuser()
                elif expert_rect.collidepoint(event.pos):
                    run_expert()

        # Draw the main text
        main_text_rect = main_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(main_text, main_text_rect)

        pygame.display.flip()
        clock.tick(60)


def run_both():
    try:
        # Run player1 and player2 as separate processes
        subprocess.Popen([sys.executable, "player1.py"])
        subprocess.Popen([sys.executable, "player2.py"])
    except Exception as e:
        print(f"Error launching player scripts: {e}")


def run_defuser():
    try:
        # Run player1 and player2 as separate processes
        subprocess.Popen([sys.executable, "player1.py"])
    except Exception as e:
        print(f"Error launching defuser script: {e}")


def run_expert():
    try:
        subprocess.Popen([sys.executable, "player2.py"])
    except Exception as e:
        print(f"Error launching player scripts: {e}")


# Run the main screen function
main_screen()

# Quit Pygame
pygame.quit()
sys.exit()
