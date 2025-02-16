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

expert = pygame.transform.scale(expert, (300, 300))
defuser = pygame.transform.scale(defuser, (300, 300))

# Main Text
main_text = pygame.image.load("graphics/main_txt.png")

# Button rectangles for collision detection
expert_rect = expert.get_rect(center=(200 + 150, 320 + 150))
defuser_rect = defuser.get_rect(center=(1166 - 303 + 150, 320 + 150))

# Scaling factors and target sizes
expert_size = [300, 300]
defuser_size = [300, 300]
target_size = [315, 315]
scaling_factor = 0.1  # Controls the smoothness of the scaling

"""Display the main screen"""
def main_screen():
    running = True
    clock = pygame.time.Clock()

    # Load background once before the loop
    background_image = pygame.image.load("graphics/bomb.jpg")

    while running:
        screen.blit(background_image, (0, 0))

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Check for hover and interpolate scaling smoothly
        if expert_rect.collidepoint(mouse_pos):
            expert_size[0] += (target_size[0] - expert_size[0]) * scaling_factor
            expert_size[1] += (target_size[1] - expert_size[1]) * scaling_factor
        else:
            expert_size[0] += (300 - expert_size[0]) * scaling_factor
            expert_size[1] += (300 - expert_size[1]) * scaling_factor

        if defuser_rect.collidepoint(mouse_pos):
            defuser_size[0] += (target_size[0] - defuser_size[0]) * scaling_factor
            defuser_size[1] += (target_size[1] - defuser_size[1]) * scaling_factor
        else:
            defuser_size[0] += (300 - defuser_size[0]) * scaling_factor
            defuser_size[1] += (300 - defuser_size[1]) * scaling_factor

        # Draw expert button with scaling
        scaled_expert = pygame.transform.smoothscale(expert, (int(expert_size[0]), int(expert_size[1])))
        screen.blit(scaled_expert, (expert_rect.centerx - scaled_expert.get_width() // 2, expert_rect.centery - scaled_expert.get_height() // 2))

        # Draw defuser button with scaling
        scaled_defuser = pygame.transform.smoothscale(defuser, (int(defuser_size[0]), int(defuser_size[1])))
        screen.blit(scaled_defuser, (defuser_rect.centerx - scaled_defuser.get_width() // 2, defuser_rect.centery - scaled_defuser.get_height() // 2))

        # Change mouse cursor on hover
        if defuser_rect.collidepoint(mouse_pos) or expert_rect.collidepoint(mouse_pos):
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
        main_text_rect = main_text.get_rect(center=(WIDTH // 2, (HEIGHT // 3) - 20))
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
