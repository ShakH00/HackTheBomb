import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Wire Puzzle")

# Load images
red_wire_uncut = pygame.image.load("redwire.png")
red_wire_cut = pygame.image.load("redwirecutted.png")
blue_wire_uncut = pygame.image.load("bluewire.png")
blue_wire_cut = pygame.image.load("bluewirecutted.png")

# Scale images
red_wire_uncut = pygame.transform.scale(red_wire_uncut, (50, 300))
red_wire_cut = pygame.transform.scale(red_wire_cut, (50, 300))
blue_wire_uncut = pygame.transform.scale(blue_wire_uncut, (50, 300))
blue_wire_cut = pygame.transform.scale(blue_wire_cut, (50, 300))

# Define wire rects
red_wire_rect = pygame.Rect(680, 200, 50, 300)
blue_wire_rect = pygame.Rect(730, 200, 50, 300)

# Set initial wire state
red_wire_cutted = False
blue_wire_cutted = False

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check if mouse clicked on red wire
            if red_wire_rect.collidepoint(mouse_pos):
                red_wire_cutted = not red_wire_cutted  # Toggle wire state
            # Check if mouse clicked on blue wire
            elif blue_wire_rect.collidepoint(mouse_pos):
                blue_wire_cutted = not blue_wire_cutted  # Toggle wire state

    # Clear the screen
    screen.fill((255, 255, 255))

    # Draw wires based on their state
    if red_wire_cutted:
        screen.blit(red_wire_cut, (680, 200))
    else:
        screen.blit(red_wire_uncut, (680, 200))

    if blue_wire_cutted:
        screen.blit(blue_wire_cut, (730, 200))
    else:
        screen.blit(blue_wire_uncut, (730, 200))

    # Update the display
    pygame.display.flip()
