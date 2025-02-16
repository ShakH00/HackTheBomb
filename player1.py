import os
import pygame
import sys
import time
import socket
import threading
import random
from game_state import GameState

# Initialize pygame
pygame.init()

game_state = GameState()

# Set the screen dimensions and create the screen object
WIDTH = 1366
HEIGHT = 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HackTheBomb | Player 1 (Defuser)")
icon = pygame.image.load("graphics/icon.png")
pygame.display.set_icon(icon)

# Colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (50, 50, 50)
GREEN_BRIGHT = (0, 255, 0)

# Font
font = pygame.font.Font(None, 48)
big_font = pygame.font.Font(None, 80)

# Load scissor cursor image
scissor_cursor = pygame.image.load("graphics/scissor_cursor.png")
scissor_cursor = pygame.transform.scale(scissor_cursor, (32, 32))

# Load countdown digit images (0-9)
digit_images = []
for i in range(10):
    image_path = os.path.join("graphics/numbers", f"0{i}.png")
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (43, 60))  # Adjust image size here
    digit_images.append(image)

# Timer
bomb_timer = 300  # 5-minute countdown
start_time = time.time()


# Wire Module (Wonky wires)
def generate_wonky_wire(start_x, start_y, length, color, wire_id):
    """Generate a wonky wire path using random offsets."""
    points = [(start_x, start_y)]
    for i in range(1, 10):  # 10 segments
        new_x = start_x + (length // 10) * i
        new_y = start_y + random.randint(-5, 5)  # Random up/down offsets
        points.append((new_x, new_y))
    return {"points": points, "color": color, "cut": False, "id": wire_id}

# Creating the wonky wires
wires = [
    generate_wonky_wire(100, 200, 300, RED, "red"),
    generate_wonky_wire(100, 250, 300, GREEN, "green"),
    generate_wonky_wire(100, 300, 300, BLUE, "blue"),
]

wire_colors = ["red", "green", "blue"]
correct_wire = game_state.choose_wire
print(correct_wire)

# Symbol Keypad Module
symbols = ["%", "!", ";", "&"]
symbol_positions = [(600, 500), (700, 500), (800, 500), (900, 500)]
correct_symbol_order = game_state.choose_symbol_order
print(correct_symbol_order)
pressed_symbols = []
symbols_completed = False

# Number Code Module
bomb_number_code = game_state.bomb_number_code
player_input_code = ""
code_correct = False
print(bomb_number_code)

# Network Setup to Receive Instructions from Player 2
HOST = "localhost"
PORT = 5555
received_message = "Waiting for expert..."

def receive_data():
    global received_message
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for Player 2 (Expert) to connect...")
        conn, addr = s.accept()
        with conn:
            print(f"Connected to {addr}")
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                received_message = data  # Update displayed message

# Start networking thread
threading.Thread(target=receive_data, daemon=True).start()

# Input box state
input_active = False

# Game Loop
running = True
first_wire_cut = None  # Track the first wire cut
bomb_defused = False  # Track if bomb has been successfully defused
correct_wire_bool = False

while running:
    screen.fill(WHITE)

    # Outer shell of the bomb
    bomb_outer = pygame.draw.rect(screen, (153, 143, 96), (50, 50, 1266, 668))
    bomb_inner = pygame.draw.rect(screen, (115, 107, 72), (60, 60, 1246, 648))

    # Draw box for clock
    clock_outer = pygame.draw.rect(screen, (255, 0, 0), ((WIDTH / 2) - 100, 300, 197, 80))
    clock_inner = pygame.draw.rect(screen, (0, 0, 0), ((WIDTH / 2) - 95, 305, 187, 70))

    # Calculate remaining time
    elapsed_time = time.time() - start_time
    remaining_time = max(0, bomb_timer - int(elapsed_time))
    minutes = remaining_time // 60
    seconds = remaining_time % 60

    # Split digits for minutes and seconds
    min_tens = minutes // 10
    min_ones = minutes % 10
    sec_tens = seconds // 10
    sec_ones = seconds % 10

    # Draw countdown timer using images
    screen.blit(digit_images[min_tens], ((WIDTH / 2) - 90, 310))
    screen.blit(digit_images[min_ones], ((WIDTH / 2) - 50, 310))
    screen.blit(digit_images[sec_tens], ((WIDTH / 2), 310))
    screen.blit(digit_images[sec_ones], ((WIDTH / 2) + 43, 310))

    if remaining_time == 0:
        pygame.mouse.set_visible(True)
        screen.fill(RED)
        defused_text = big_font.render("BOOM! You didn't defuse the bomb in time!", True, WHITE)
        screen.blit(defused_text, (WIDTH // 2 - 550, HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.delay(3000)  # Pause for 3 seconds
        running = False  # End game (Bomb explodes)

    # Display instructions from Player 2
    instruction_text = font.render(received_message, True, BLACK)
    screen.blit(instruction_text, (50, 100))

    # Draw Wonky Wires
    mouse_on_wire = False
    for wire in wires:
        if not wire["cut"]:
            pygame.draw.lines(screen, wire["color"], False, wire["points"], 6)
        else:
            # Draw the cut wire with a gap in the middle
            mid_idx = len(wire["points"]) // 2
            pygame.draw.lines(screen, wire["color"], False, wire["points"][:mid_idx], 6)
            pygame.draw.lines(screen, wire["color"], False, wire["points"][mid_idx + 1:], 6)

        # Check if mouse is hovering over a wire
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for px, py in wire["points"]:
            if abs(px - mouse_x) < 10 and abs(py - mouse_y) < 10:
                mouse_on_wire = True

    wires_left_terminal = pygame.draw.rect(screen, (0, 0, 0), (90, 175, 10, 155))
    wires_right_terminal = pygame.draw.rect(screen, (0, 0, 0), (370, 175, 10, 155))

    # Change cursor to scissor if hovering over a wire
    if mouse_on_wire:
        pygame.mouse.set_visible(False)
        screen.blit(scissor_cursor, (mouse_x, mouse_y))
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.mouse.set_visible(True)

    # Draw Symbol Keypad
    for idx, symbol in enumerate(symbols):
        pygame.draw.rect(screen, GRAY, (symbol_positions[idx][0], symbol_positions[idx][1], 75, 75))
        text = font.render(symbol, True, BLACK)
        screen.blit(text, (symbol_positions[idx][0] + 15, symbol_positions[idx][1] + 15))

    # Draw Number Code Area
    bomb_code_text = font.render(f"Input Code:", True, BLUE)
    screen.blit(bomb_code_text, (1000, 250))

    # Draw input box for number entry
    input_box = pygame.draw.rect(screen, GRAY if input_active else DARK_GRAY, (990, 300, 200, 60))
    if code_correct:
        pygame.draw.rect(screen, GREEN, (990, 300, 200, 60))
    pygame.draw.rect(screen, WHITE, (990, 300, 200, 60), 3)
    input_text = font.render(player_input_code, True, WHITE)
    screen.blit(input_text, (1000, 310))

    # Draw Submit Button
    submit_button = pygame.Rect(990, 370, 200, 50)
    pygame.draw.rect(screen, BLUE, submit_button)
    submit_text = font.render("Submit", True, WHITE)
    screen.blit(submit_text, (submit_button.x + 45, submit_button.y + 10))

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # Wire Cutting
            for wire in wires:
                for px, py in wire["points"]:  # Check all points in the wire
                    if abs(px - x) < 10 and abs(py - y) < 10:  # Click near wire
                        if not wire["cut"]:  # Only process uncut wires
                            wire["cut"] = True
                            print(f"Wire {wire['id']} cut!")


                            if first_wire_cut is None:
                                first_wire_cut = wire["id"]  # Track first wire cut

                            # Check if wrong wire was cut first
                            if first_wire_cut != correct_wire:
                                pygame.mouse.set_visible(True)
                                screen.fill(RED)
                                defused_text = big_font.render("BOOM! You cut the wrong wire first!", True, BLACK)
                                screen.blit(defused_text, (WIDTH // 2 - 470, HEIGHT // 2 - 50))
                                pygame.display.flip()
                                pygame.time.delay(3000)  # Pause for 3 seconds
                                running = False  # End game (Bomb explodes)
                            correct_wire_bool = True

                        break

            # Symbol Keypad Interaction
            for idx, pos in enumerate(symbol_positions):
                symbol_rect = pygame.Rect(pos[0], pos[1], 75, 75)
                if symbol_rect.collidepoint(x, y):
                    pressed_symbols.append(symbols[idx])
                    print(f"Pressed {symbols[idx]}")

                    # Check if pressed order is correct
                    if len(pressed_symbols) == len(correct_symbol_order):
                        if pressed_symbols == correct_symbol_order:
                            print("Correct Keypad Entry!")
                            symbols_completed = True
                        else:
                            print("Incorrect Keypad Entry! Resetting...")
                            pressed_symbols = []

            # Keypad entering
            if input_box.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False

            if submit_button.collidepoint(event.pos):
                if len(player_input_code) == 4:
                    if player_input_code == bomb_number_code:
                        print("Correct Code Entered!")
                        code_correct = True
                    else:
                        print("Wrong Code! Try Again.")
                    player_input_code = ""

        elif event.type == pygame.KEYDOWN and input_active:
            if event.key == pygame.K_BACKSPACE:
                player_input_code = player_input_code[:-1]
            elif event.unicode.isdigit() and len(player_input_code) < 4:
                player_input_code += event.unicode

    # Check if all tasks are completed
    if correct_wire_bool and symbols_completed and code_correct:
        bomb_defused = True

    # Display Bomb Defused Message
    if bomb_defused:
        screen.fill(GREEN_BRIGHT)
        defused_text = big_font.render("BOMB DEFUSED!", True, BLACK)
        screen.blit(defused_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
        pygame.display.flip()
        pygame.time.delay(3000)  # Pause for 3 seconds
        running = False  # End game

    pygame.display.flip()

pygame.quit()
sys.exit()