import pygame
import sys
import time
import socket
import threading
import random

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bomb Defusal - Player 1 (Defuser)")

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

# Timer
bomb_timer = 300  # 5-minute countdown
start_time = time.time()

# Correct wire order
correct_wire = "red"  # Player must cut the red wire first

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
    generate_wonky_wire(500, 250, 300, RED, "red"),
    generate_wonky_wire(500, 300, 300, GREEN, "green"),
    generate_wonky_wire(500, 350, 300, BLUE, "blue"),
]

# Symbol Keypad Module
symbols = ["★", "Ω", "Ψ", "∑"]
symbol_positions = [(600, 500), (700, 500), (800, 500), (900, 500)]
correct_symbol_order = ["Ω", "∑", "Ψ", "★"]
pressed_symbols = []
symbols_completed = False

# Number Code Module
bomb_number_code = "3284"
player_input_code = ""
code_correct = False

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

# Game Loop
running = True
first_wire_cut = None  # Track the first wire cut
bomb_defused = False  # Track if bomb has been successfully defused
correct_wire = False

while running:
    screen.fill(WHITE)

    # Calculate remaining time
    elapsed_time = time.time() - start_time
    remaining_time = max(0, bomb_timer - int(elapsed_time))
    timer_text = font.render(f"Time Left: {remaining_time}s", True, BLACK)
    screen.blit(timer_text, (50, 50))

    # Display instructions from Player 2
    instruction_text = font.render(received_message, True, BLACK)
    screen.blit(instruction_text, (50, 100))

    # Draw Wonky Wires
    for wire in wires:
        if not wire["cut"]:
            pygame.draw.lines(screen, wire["color"], False, wire["points"], 6)

    # Draw Symbol Keypad
    for idx, symbol in enumerate(symbols):
        pygame.draw.rect(screen, GRAY, (symbol_positions[idx][0], symbol_positions[idx][1], 75, 75))
        text = font.render(symbol, True, BLACK)
        screen.blit(text, (symbol_positions[idx][0] + 15, symbol_positions[idx][1] + 15))

    # Draw Number Code Area
    bomb_code_text = font.render(f"Code: {bomb_number_code}", True, BLUE)
    screen.blit(bomb_code_text, (1000, 250))

    # Draw input box for number entry
    pygame.draw.rect(screen, DARK_GRAY, (990, 300, 200, 60))  # Black box for input
    pygame.draw.rect(screen, WHITE, (990, 300, 200, 60), 3)  # White border
    input_text = font.render(player_input_code, True, WHITE)
    screen.blit(input_text, (1010, 310))

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
                            if wire['id'] == "red":
                                correct_wire = True

                            if first_wire_cut is None:
                                first_wire_cut = wire["id"]  # Track first wire cut

                            # Check if wrong wire was cut first
                            if first_wire_cut != correct_wire:
                                print("BOOM! You cut the wrong wire first! 💥")
                                running = False  # End game (Bomb explodes)

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

        elif event.type == pygame.KEYDOWN:
            # Number Code Entry
            if event.key == pygame.K_RETURN:
                if player_input_code == bomb_number_code:
                    print("Correct Code Entered!")
                    code_correct = True
                else:
                    print("Wrong Code! Try Again.")
                player_input_code = ""  # Reset input
            elif event.key == pygame.K_BACKSPACE:
                player_input_code = player_input_code[:-1]
            elif event.unicode.isdigit():
                if len(player_input_code) < 4:
                    player_input_code += event.unicode

    # Check if all tasks are completed
    if correct_wire and symbols_completed and code_correct:
        bomb_defused = True

    # Display Bomb Defused Message
    if bomb_defused:
        screen.fill(GREEN_BRIGHT)
        defused_text = big_font.render("BOMB DEFUSED!", True, BLACK)
        screen.blit(defused_text, (WIDTH//2 - 200, HEIGHT//2 - 50))
        pygame.display.flip()
        pygame.time.delay(3000)  # Pause for 3 seconds
        running = False  # End game

    pygame.display.flip()

pygame.quit()
sys.exit()
