import pygame
import sys

# Initialize Pygame
pygame.init()

# Get the screen dimensions
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Set up the display in fullscreen mode
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Fullscreen Wires")

# Define colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
CUT_COLOR = (0, 0, 0)  # Color to represent the wire being cut

# Define wire dimensions
wire_width = 10
wire_height = screen_height // 3  # Divide screen height into 3 equal parts

# Define wire positions
wire1_x = (screen_width - wire_width) // 4
wire1_y = screen_height // 6

wire2_x = (screen_width - wire_width) // 4 * 2
wire2_y = screen_height // 6

wire3_x = (screen_width - wire_width) // 4 * 3
wire3_y = screen_height // 6

# Function to check if a point is within a rectangle
def point_in_rect(point, rect):
    x, y = point
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is within the area of any wire
            mouse_pos = pygame.mouse.get_pos()
            if point_in_rect(mouse_pos, (wire1_x, wire1_y, wire_width, wire_height)):
                # Wire 1 is clicked, simulate cut effect
                pygame.draw.line(screen, CUT_COLOR, (wire1_x, wire1_y), (wire1_x + wire_width, wire1_y + wire_height), 5)
            elif point_in_rect(mouse_pos, (wire2_x, wire2_y, wire_width, wire_height)):
                # Wire 2 is clicked, simulate cut effect
                pygame.draw.line(screen, CUT_COLOR, (wire2_x, wire2_y), (wire2_x + wire_width, wire2_y + wire_height), 5)
            elif point_in_rect(mouse_pos, (wire3_x, wire3_y, wire_width, wire_height)):
                # Wire 3 is clicked, simulate cut effect
                pygame.draw.line(screen, CUT_COLOR, (wire3_x, wire3_y), (wire3_x + wire_width, wire3_y + wire_height), 5)

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Draw wire 1 (red)
    pygame.draw.rect(screen, RED, (wire1_x, wire1_y, wire_width, wire_height))

    # Draw wire 2 (blue)
    pygame.draw.rect(screen, BLUE, (wire2_x, wire2_y, wire_width, wire_height))

    # Draw wire 3 (green)
    pygame.draw.rect(screen, GREEN, (wire3_x, wire3_y, wire_width, wire_height))

    pygame.display.flip()

pygame.quit()
sys.exit()
