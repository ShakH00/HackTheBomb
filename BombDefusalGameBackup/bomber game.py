import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bomb Generation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Bomb class
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.timer = random.randint(5, 20)  # Random timer between 5 to 20 seconds

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            print("Boom!")  # Replace this with your defusal mechanic or explosion effect
            self.kill()

# Function to generate bombs
def generate_bombs(num_bombs):
    bomb_group = pygame.sprite.Group()
    for _ in range(num_bombs):
        x = random.randint(0, WIDTH - 30)
        y = random.randint(0, HEIGHT - 30)
        bomb = Bomb(x, y)
        bomb_group.add(bomb)
    return bomb_group

# Main loop
running = True
clock = pygame.time.Clock()
bombs = generate_bombs(5)  # Generate 5 bombs initially

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update

    # Draw
    SCREEN.fill(WHITE)
    bombs.update()
    bombs.draw(SCREEN)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
