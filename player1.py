import os
import pygame
import sys
import time
import socket
import threading
import random
import textwrap
from game_state import GameState
from player2 import small_font
from utility import write_puzzle_info

# Initialize pygame
pygame.init()

game_state = GameState()
game_state.initialize()

write_puzzle_info(game_state.correct_wire, game_state.correct_symbol_order, game_state.bomb_number_code)

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

# Load background
background_image = pygame.image.load("graphics/motherboard.jpg")
# background_image = pygame.transform.scale(background_image, (1266, 668))
screen.blit(background_image, (0, 0))

# Load bomb background
bomb_background_image = pygame.image.load("graphics/bomb_background1.jpg")
bomb_background_image = pygame.transform.scale(bomb_background_image, (1246, 648))

# Load images
scissor_cursor = pygame.image.load("graphics/scissor_cursor.png")
scissor_cursor = pygame.transform.scale(scissor_cursor, (40, 40))

screw = pygame.image.load("graphics/screw.png")
screw = pygame.transform.scale(screw, (20, 20))

detonator_img = pygame.image.load("graphics/detonate_button.png")
detonator_img = pygame.transform.scale(detonator_img, (250, 250))

timer_background = pygame.image.load("graphics/timer_background.png")
timer_background = pygame.transform.scale(timer_background, (300, 165))

battery = pygame.image.load("graphics/battery.png")
battery = pygame.transform.scale(battery, (120, 105))

explosive = pygame.image.load("graphics/explosive1.png")
explosive = pygame.transform.scale(explosive, (320, 80))

# Wires
red_wire = pygame.image.load("graphics/redwire.png")
red_wire = pygame.transform.scale(red_wire, (225, 25))

red_wire_cut = pygame.image.load("graphics/redwirecutted.png")
red_wire_cut = pygame.transform.scale(red_wire_cut, (225, 25))

blue_wire = pygame.image.load("graphics/bluewire.png")
blue_wire = pygame.transform.scale(blue_wire, (225,25))

blue_wire_cut = pygame.image.load("graphics/bluewirecutted.png")
blue_wire_cut = pygame.transform.scale(blue_wire_cut, (225, 25))

green_wire = pygame.image.load("graphics/greenwire.png")
green_wire = pygame.transform.scale(green_wire, (225,25))

green_wire_cut = pygame.image.load("graphics/greenwirecutted.png")
green_wire_cut = pygame.transform.scale(green_wire_cut, (225,25))

# Background wires
cable_blue = pygame.image.load("graphics/blue.png")
cable_black = pygame.image.load("graphics/black.png")
cable_black_frayed = pygame.image.load("graphics/black_frayed.png")
cable_black_frayed_2 = pygame.image.load("graphics/black_frayed_2.png")
cable_white_frayed = pygame.image.load("graphics/white_frayed.png")

# cable_blue = pygame.transform.scale(cable_blue, (100,25))
# cable_black = pygame.transform.scale(cable_black, (100,25))
# cable_black_frayed = pygame.transform.scale(cable_black_frayed, (100,25))
# cable_black_frayed_2 = pygame.transform.scale(cable_black_frayed_2, (100,25))
# cable_white_frayed = pygame.transform.scale(cable_white_frayed, (100,25))



# Phone
phone = pygame.image.load("graphics/phone2.png")
phone = pygame.transform.scale(phone, (300, 200))

# Load countdown digit images (0-9)
digit_images = []
for i in range(10):
    image_path = os.path.join("graphics/numbers", f"0{i}.png")
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (50, 68))  # Adjust image size here
    digit_images.append(image)

# Timer
bomb_timer = 300  # 5-minute countdown
start_time = time.time()
time_reduced = False

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
    generate_wonky_wire(100, 300, 300, RED, "red"),
    generate_wonky_wire(100, 350, 300, GREEN, "green"),
    generate_wonky_wire(100, 400, 300, BLUE, "blue"),
]

wire_colors = ["red", "green", "blue"]

# Symbol Keypad Module
symbols = ["%", "!", ";", "&"]
symbol_positions = [(100, 500), (200, 500), (300, 500), (400, 500)]
pressed_symbols = []
symbols_completed = False

# Number Code Module
bomb_number_code = game_state.bomb_number_code
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

# Keypad clicked state
keypad_active = False

# Input box state
input_active = False

# Game Loop
running = True
first_wire_cut = None  # Track the first wire cut
bomb_defused = False  # Track if bomb has been successfully defused
correct_wire_bool = False

while running:
    # screen.fill(WHITE)

    # Outer shell of the bomb
    bomb_outer = pygame.draw.rect(screen, (153, 143, 96), (50, 50, 1266, 668))
    # bomb_inner = pygame.draw.rect(screen, (115, 107, 72), (60, 60, 1246, 648))
    screen.blit(bomb_background_image, (60, 60))

    # Screws
    screen.blit(screw, (70, 70))
    screen.blit(screw, (70, 678))
    screen.blit(screw, (1275, 70))
    screen.blit(screw, (1275, 678))

    # Background cables
    cable_blue_rotated = pygame.transform.rotate(cable_blue, -45)
    screen.blit(cable_blue_rotated, (570, 150))
    screen.blit(cable_black, (265, 210))
    cable_black_frayed_rotated = pygame.transform.rotate(cable_black_frayed, -25)
    screen.blit(cable_black_frayed_rotated, (655, 100))
    cable_white_frayed_rotated = pygame.transform.rotate(cable_white_frayed, 75)
    screen.blit(cable_white_frayed_rotated, (330, 130))

    # Phone
    screen.blit(phone, (50, 40))

    # Timer background
    timer_rect = timer_background.get_rect(center=(WIDTH - 683, 160))
    screen.blit(timer_background, timer_rect.topleft)

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

    # Back color rect
    timer_back_rect = pygame.draw.rect(screen, (16, 79, 51), (550, 100, 280, 85))

    # Draw countdown timer using images
    screen.blit(digit_images[min_tens], ((WIDTH / 2) - 100, 106))
    screen.blit(digit_images[min_ones], ((WIDTH / 2) - 50, 106))
    screen.blit(digit_images[sec_tens], ((WIDTH / 2) + 5, 106))
    screen.blit(digit_images[sec_ones], ((WIDTH / 2) + 55, 106))


    if remaining_time <= 0:
        pygame.mouse.set_visible(True)
        screen.fill(RED)
        defused_text = big_font.render("BOOM! You didn't defuse the bomb in time!", True, WHITE)
        text_rect = defused_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(defused_text, text_rect.topleft)
        pygame.display.flip()
        pygame.time.delay(3000)  # Pause for 3 seconds
        running = False  # End game (Bomb explodes)

    # Dynamite
    screen.blit(explosive, (830, 80))

    # Battery
    screen.blit(battery, (413, 100))

    # Display instructions from Player 2
    small_font = pygame.font.SysFont(None, 20)
    instruction_text = small_font.render(received_message, True, GREEN)
    screen.blit(instruction_text, (95, 125))

    # Detonator button
    detonator_rect = detonator_img.get_rect(center=(WIDTH - 250, 400))
    screen.blit(detonator_img, detonator_rect.topleft)

    # Rails
    wires_left_terminal = pygame.draw.rect(screen, (0, 0, 0), (105, 290, 10, 145))
    wires_right_terminal = pygame.draw.rect(screen, (0, 0, 0), (313, 290, 10, 145))

    # Draw Wires as Images
    mouse_on_wire = False

    for wire in wires:
        wire_x, wire_y = wire["points"][0]  # Get wire position

        # Display the correct wire image based on cut status
        if wire["cut"]:
            if wire["id"] == "red":
                screen.blit(red_wire_cut, (wire_x, wire_y))
            elif wire["id"] == "blue":
                screen.blit(blue_wire_cut, (wire_x, wire_y))
            elif wire["id"] == "green":
                screen.blit(green_wire_cut, (wire_x, wire_y))
        else:
            if wire["id"] == "red":
                screen.blit(red_wire, (wire_x, wire_y))
            elif wire["id"] == "blue":
                screen.blit(blue_wire, (wire_x, wire_y))
            elif wire["id"] == "green":
                screen.blit(green_wire, (wire_x, wire_y))

        # Update hitbox for detecting mouse hover and clicks
        wire_rect = pygame.Rect(wire_x, wire_y, 225, 25)  # Correct size

        # Check if mouse is over the wire
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if wire_rect.collidepoint(mouse_x, mouse_y):
            mouse_on_wire = True

    # Change cursor to scissors if hovering over a wire
    if mouse_on_wire:
        pygame.mouse.set_visible(False)
        screen.blit(scissor_cursor, (mouse_x - 20, mouse_y - 20))  # Offset to center
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.mouse.set_visible(True)

    # Box for symbols
    box = pygame.draw.rect(screen, DARK_GRAY, (75, 475, 425, 125))

    # Draw Symbol Keypad
    for idx, symbol in enumerate(symbols):
        pygame.draw.rect(screen, GRAY, (symbol_positions[idx][0], symbol_positions[idx][1], 75, 75))
        text = font.render(symbol, True, BLACK)
        screen.blit(text, (symbol_positions[idx][0] + 22, symbol_positions[idx][1] + 20))

    if symbols_completed:
        for idx, symbol in enumerate(symbols):
            pygame.draw.rect(screen, GREEN, (symbol_positions[idx][0], symbol_positions[idx][1], 75, 75))
            text = font.render(symbol, True, BLACK)
            screen.blit(text, (symbol_positions[idx][0] + 22, symbol_positions[idx][1] + 22))

    # Draw Number Code Area
    # bomb_code_text = font.render(f"Input Code:", True, BLACK)
    # screen.blit(bomb_code_text, (610, 400))

    # Draw input box for number entry
    input_box = pygame.draw.rect(screen, GRAY if input_active else DARK_GRAY, (600, 450, 200, 60))
    pygame.draw.rect(screen, WHITE, (600, 450, 200, 60), 3)
    input_text = font.render(player_input_code, True, WHITE)
    screen.blit(input_text, (660, 465))

    # Draw Submit Button
    submit_button = pygame.Rect(600, 520, 200, 50)
    pygame.draw.rect(screen, BLUE, submit_button)
    submit_text = font.render("Submit", True, WHITE)
    screen.blit(submit_text, (submit_button.x + 45, submit_button.y + 10))

    if code_correct:
        pygame.draw.rect(screen, GREEN, (600, 520, 200, 50))
        screen.blit(submit_text, (submit_button.x + 45, submit_button.y + 10))

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        elif event.type == pygame.MOUSEBUTTONDOWN:

            x, y = event.pos

            # Wire Cutting
            for wire in wires:

                wire_x, wire_y = wire["points"][0]

                wire_rect = pygame.Rect(wire_x, wire_y, 200, 30)  # Correct hitbox

                if wire_rect.collidepoint(x, y) and not wire["cut"]:  # Prevents duplicate cutting

                    wire["cut"] = True  # Cut the wire

                    print(f"Wire {wire['id']} cut!")

                    # Check if this is the first wire cut

                    if first_wire_cut is None:
                        first_wire_cut = wire["id"]  # Track the first wire cut

                    # If the first wire cut is WRONG, explode immediately

                    if first_wire_cut != game_state.correct_wire:
                        pygame.mouse.set_visible(True)
                        screen.fill(RED)
                        defused_text = big_font.render("BOOM! You cut the wrong wire first!", True, BLACK)
                        text_rect = defused_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        screen.blit(defused_text, text_rect.topleft)
                        pygame.display.flip()
                        pygame.time.delay(3000)  # Pause for 3 seconds
                        running = False  # End game (Bomb explodes)

                        break  # Stop checking
                    # If the correct wire is cut, update game state
                    correct_wire_bool = True
                    print("Correct wire cut! Proceeding...")

                    break  # Stop checking other wires after cutting one

            # Symbol Keypad Interaction
            for idx, pos in enumerate(symbol_positions):
                symbol_rect = pygame.Rect(pos[0], pos[1], 75, 75)
                if symbol_rect.collidepoint(x, y):
                    pressed_symbols.append(symbols[idx])
                    print(f"Pressed {symbols[idx]}")

                    # Check if pressed order is correct
                    if len(pressed_symbols) == len(game_state.correct_symbol_order):
                        if pressed_symbols == game_state.correct_symbol_order:
                            print("Correct Keypad Entry!")
                            symbols_completed = True
                        else:
                            print("Incorrect Keypad Entry! Resetting...")
                            bomb_timer -= 90
                            pressed_symbols = []

            if event.type == pygame.MOUSEBUTTONDOWN:
                if detonator_rect.collidepoint(event.pos):
                    pygame.mouse.set_visible(True)
                    screen.fill(RED)
                    defused_text = big_font.render("BOOM! You triggered the bomb!", True, WHITE)
                    text_rect = defused_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    screen.blit(defused_text, text_rect.topleft)
                    pygame.display.flip()
                    pygame.time.delay(3000)  # Pause for 3 seconds
                    running = False  # End game (Bomb explodes)

            # Keypad entering
            if input_box.collidepoint(event.pos):
                input_active = True
            else:
                input_active = False

            if submit_button.collidepoint(event.pos):
                if len(player_input_code) == 4:
                    if player_input_code == game_state.bomb_number_code:
                        print("Correct Code Entered!")
                        code_correct = True
                    else:
                        pygame.mouse.set_visible(True)
                        screen.fill(RED)
                        defused_text = big_font.render("BOOM! You put the wrong code!", True, BLACK)
                        text_rect = defused_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                        screen.blit(defused_text, text_rect.topleft)
                        pygame.display.flip()
                        pygame.time.delay(3000)  # Pause for 3 seconds
                        running = False  # End game (Bomb explodes)
                        player_input_code = ""

        elif event.type == pygame.KEYDOWN and input_active:
            if input_active:
                if event.key == pygame.K_BACKSPACE:
                    player_input_code = player_input_code[:-1]
                elif event.unicode.isdigit() and len(player_input_code) < 4:
                    player_input_code += event.unicode
                elif event.key == pygame.K_RETURN:  # Pressing Enter submits the code
                    if len(player_input_code) == 4:
                        if player_input_code == game_state.bomb_number_code:
                            print("Correct Code Entered!")
                            code_correct = True
                        else:
                            print("Wrong Code! Try Again.")
                        player_input_code = ""

    # Check if all tasks are completed
    if correct_wire_bool and symbols_completed and code_correct:
        bomb_defused = True

    # Display Bomb Defused Message
    if bomb_defused:
        pygame.mouse.set_visible(True)
        screen.fill(GREEN_BRIGHT)
        defused_text = big_font.render("CONGRATULATIONS!! BOMB DEFUSED!", True, BLACK)
        text_rect = defused_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(defused_text, text_rect.topleft)
        pygame.display.flip()
        pygame.time.delay(3000)  # Pause for 3 seconds
        running = False  # End game

    pygame.display.flip()

pygame.quit()
sys.exit()