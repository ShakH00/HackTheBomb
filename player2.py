import pygame
import sys
import socket
import time
import random
from game_state import GameState
from utility import read_puzzle_info

# Initialize pygame
pygame.init()

game_state = GameState()

def initialize_from_file():
    if not game_state.load_puzzle_info():
        print("Waiting for puzzle information file...")
        return False
    return True

# Window settings
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bomb Defusal - Player 2 (Expert)")

# Terminal style Colors
BLACK      = (0, 0, 0)
DARK_GRAY  = (30, 30, 30)
GREEN      = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
RED        = (255, 50, 50)
# When a button is hovered, use a slightly lighter gray:
LIGHT_GRAY = (100, 100, 100)
WHITE      = (255, 255, 255)  # (not used extensively)

# Monospaced Fonts (using Consolas if available)
font       = pygame.font.Font(pygame.font.match_font("consolas"), 28)
title_font = pygame.font.Font(pygame.font.match_font("consolas"), 40)
small_font = pygame.font.Font(pygame.font.match_font("consolas"), 20)

# Network Setup
HOST = "localhost"
PORT = 5555
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Module states and information
current_module = "wires"
modules = ["wires", "symbols", "code"]
message_to_send = ""

# Detailed manual pages with puzzle mechanics
manual_pages = {
    "wires": [
        "Wire Module Instructions:",
        "1. You will receive an encrypted wire color using Caesar cipher",
        "2. Use the provided encrypted 'A' to determine the shift",
        "3. Possible wire colors: red, blue, green",
        "4. The defuser must cut the correct wire first",
        "5. Example: If you get 'ylk' and 'H', the shift is 7",
        "   (A -> H means 7 shift, so 'ylk' -> 'red')",
        "WARNING: Cutting wrong wire will detonate the bomb!"
    ],
    "symbols": [
        "Symbol Module Instructions:",
        "1. Four symbols must be pressed in correct order: %, !, ;, &",
        "2. You will receive logical clues about their order",
        "3. Common clues include:",
        "   - Order relationships (X comes before/after Y)",
        "   - Position constraints (X is not last)",
        "   - Relative positions (X is before Y)",
        "4. Analyze all clues to determine the exact sequence",
        "5. Incorrect sequence will reset the module"
    ],
    "code": [
        "Code Module Instructions:",
        "1. You will receive four math equations",
        "2. Each equation's solution is one digit of the code",
        "3. Equations use basic operations (+, -, *, /)",
        "4. Solve equations in order to get the 4-digit code",
        "5. Example:",
        "   3 + 4 = ? (7)",
        "   12 - 4 = ? (8)",
        "   3 * 3 = ? (9)",
        "   10 / 2 = ? (5)",
        "   Final code: 7895"
    ]
}

# Button class for interactive elements (now themed like terminal UI)
class Button:
    def __init__(self, x, y, width, height, text, color=DARK_GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False

    def draw(self, surface):
        # Use a slightly lighter fill when hovered
        fill_color = DARK_GRAY if not self.hover else LIGHT_GRAY
        pygame.draw.rect(surface, fill_color, self.rect)
        pygame.draw.rect(surface, GREEN, self.rect, 2)
        text_surface = font.render(self.text, True, GREEN)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hover:
                return True
        return False

# Create buttons for different modules
module_buttons = [
    Button(50, 50, 200, 50, "Wires Module"),
    Button(50, 120, 200, 50, "Symbols Module"),
    Button(50, 190, 200, 50, "Code Module")
]

# Quick message buttons with more specific instructions
quick_messages = [
    Button(300, 50, 400, 50, "WAIT! Don't cut any wires yet!"),
    Button(300, 120, 400, 50, "Solve equations one at a time"),
    Button(300, 190, 400, 50, "Remember symbol order carefully"),
    Button(300, 260, 400, 50, "Double-check before proceeding")
]

# Puzzle display area
puzzle_rect = pygame.Rect(50, 330, 650, 200)
answer_rect = pygame.Rect(50, 540, 400, 40)
submit_button = Button(460, 540, 100, 40, "Submit")

# Custom message input (kept from original functionality)
input_rect = pygame.Rect(50, HEIGHT - 100, 400, 40)
send_button = Button(460, HEIGHT - 100, 100, 40, "Send")
input_text = ""
input_active = False

# Current puzzle tracking
current_puzzle = None
puzzle_answer = ""
answer_feedback = ""
feedback_timer = 0

def send_message(message):
    try:
        client_socket.send(message.encode())
    except:
        print("Error sending message")

def draw_wrapped_text(surface, text, rect, font, color):
    words = text.split(' ')
    lines = []
    current_line = []
    for word in words:
        current_line.append(word)
        width = font.size(' '.join(current_line))[0]
        if width > rect.width:
            if len(current_line) > 1:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(' '.join(current_line))
    y = rect.top
    for line in lines:
        text_surface = font.render(line, True, color)
        surface.blit(text_surface, (rect.left, y))
        y += font.get_linesize()

def main():
    global input_text, input_active, current_module, current_puzzle, puzzle_answer, answer_feedback, feedback_timer

    # Wait for puzzle info file
    while not initialize_from_file():
        time.sleep(1)
        print("Retrying...")

    print("Puzzle information loaded successfully!")

    try:
        client_socket.connect((HOST, PORT))
        print("Connected to Player 1")
    except:
        print("Could not connect to Player 1")
        return

    running = True
    while running:
        # Terminal background
        screen.fill(BLACK)

        # Draw title in terminal style (centered green text)
        title = title_font.render("Bomb Defusal Expert Console", True, GREEN)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 10))

        # Draw buttons (module_buttons and quick_messages)
        for button in module_buttons + quick_messages:
            button.draw(screen)

        # Draw current module manual in a terminal-style panel
        manual_rect = pygame.Rect(700, 50, 600, HEIGHT - 100)
        pygame.draw.rect(screen, DARK_GRAY, manual_rect)
        pygame.draw.rect(screen, GREEN, manual_rect, 2)
        if current_module in manual_pages:
            for i, line in enumerate(manual_pages[current_module]):
                text = small_font.render(line, True, GREEN)
                screen.blit(text, (710, 60 + i * 25))

        # Draw puzzle area in terminal style
        pygame.draw.rect(screen, DARK_GRAY, puzzle_rect)
        pygame.draw.rect(screen, GREEN, puzzle_rect, 2)
        if current_puzzle:
            draw_wrapped_text(screen, current_puzzle["question"], puzzle_rect, font, GREEN)

        # Draw answer input area in terminal style
        pygame.draw.rect(screen, DARK_GRAY if input_active else BLACK, answer_rect)
        pygame.draw.rect(screen, GREEN, answer_rect, 2)
        text_surface = font.render(puzzle_answer, True, GREEN)
        screen.blit(text_surface, (answer_rect.x + 5, answer_rect.y + 5))
        submit_button.draw(screen)

        # Draw feedback message if present
        if answer_feedback and time.time() < feedback_timer:
            feedback_text = font.render(answer_feedback, True, RED)
            screen.blit(feedback_text, (50, 590))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle module selection via buttons
            for i, button in enumerate(module_buttons):
                if button.handle_event(event):
                    current_module = modules[i]
                    current_puzzle = game_state.get_puzzle(i)
                    puzzle_answer = ""

            # Handle quick messages via buttons
            for button in quick_messages:
                if button.handle_event(event):
                    send_message(button.text)
                    answer_feedback = "Sending to defuser..."
                    feedback_timer = time.time() + 2
                    puzzle_answer = ""

            if submit_button.handle_event(event):
                send_message(input_text)
                input_text = ""
                answer_feedback = "Sending to defuser..."
                feedback_timer = time.time() + 2
                puzzle_answer = ""

            # Activate answer input area if clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_active = answer_rect.collidepoint(event.pos)

            # Handle keyboard input when answer input is active
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    send_message(input_text)
                    input_text = ""
                    answer_feedback = "Sending to defuser..."
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

            # Secondary input handling (for puzzle_answer) – preserved from your original logic
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    #if current_puzzle and puzzle_answer == current_puzzle["answer"]:
                    answer_feedback = "Sending to defuser..."
                    send_message(input_text)
                    input_text = ""
                    current_puzzle = game_state.get_puzzle(modules.index(current_module))
                    #else:
                        #answer_feedback = "Incorrect! Try again."
                    feedback_timer = time.time() + 2
                    puzzle_answer = ""
                elif event.key == pygame.K_BACKSPACE:
                    puzzle_answer = puzzle_answer[:-1]
                else:
                    puzzle_answer += event.unicode

        pygame.display.flip()

    client_socket.close()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
