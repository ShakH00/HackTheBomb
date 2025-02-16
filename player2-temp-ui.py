import pygame
import sys
import socket
import threading
import time

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bomb Defusal - Player 2 (Expert)")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
LIGHT_GRAY = (200, 200, 200)
BLUE = (0, 100, 255)

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 48)

# Network Setup
HOST = "localhost"
PORT = 5555
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Module states and information
current_module = "wires"
modules = ["wires", "symbols", "code"]
message_to_send = ""
manual_pages = {
    "wires": ["3-6 wires, color-coded", "Check wire colors", "Press correct contacts"],
    "symbols": ["5 musical symbols", "Convert morse code", "Match symbols"],
    "code": ["5-letter code", "Add consecutive digits", "Match with table"]
}

# Button class for interactive elements
class Button:
    def __init__(self, x, y, width, height, text, color=LIGHT_GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover = False

    def draw(self, surface):
        color = GRAY if self.hover else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        text_surface = font.render(self.text, True, BLACK)
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

# Quick message buttons
quick_messages = [
    Button(300, 50, 300, 50, "Check wire colors"),
    Button(300, 120, 300, 50, "Look for matching symbols"),
    Button(300, 190, 300, 50, "Enter the code carefully"),
    Button(300, 260, 300, 50, "Take your time")
]

# Custom message input
input_rect = pygame.Rect(50, HEIGHT - 100, 400, 40)
send_button = Button(460, HEIGHT - 100, 100, 40, "Send")
input_text = ""
input_active = False

def send_message(message):
    try:
        client_socket.send(message.encode())
    except:
        print("Error sending message")

def main():
    global input_text, input_active, current_module
    
    # Connect to Player 1
    try:
        client_socket.connect((HOST, PORT))
        print("Connected to Player 1")
    except:
        print("Could not connect to Player 1")
        return

    running = True
    while running:
        screen.fill(WHITE)
        
        # Draw module selection
        title = title_font.render("Expert Console", True, BLACK)
        screen.blit(title, (WIDTH//2 - 100, 10))

        # Draw all buttons
        for button in module_buttons + quick_messages:
            button.draw(screen)

        # Draw input box
        pygame.draw.rect(screen, LIGHT_GRAY if input_active else WHITE, input_rect)
        pygame.draw.rect(screen, BLACK, input_rect, 2)
        text_surface = font.render(input_text, True, BLACK)
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        send_button.draw(screen)

        # Draw current module info
        module_info = manual_pages.get(current_module, [])
        for i, info in enumerate(module_info):
            info_text = font.render(info, True, BLACK)
            screen.blit(info_text, (700, 50 + i * 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Handle button clicks
            for i, button in enumerate(module_buttons):
                if button.handle_event(event):
                    current_module = modules[i]
                    
            for button in quick_messages:
                if button.handle_event(event):
                    send_message(button.text)

            if send_button.handle_event(event):
                if input_text:
                    send_message(input_text)
                    input_text = ""

            # Handle text input
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_active = input_rect.collidepoint(event.pos)

            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    send_message(input_text)
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        pygame.display.flip()

    client_socket.close()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
