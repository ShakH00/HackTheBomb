import pygame
import sys
import time
import zipfile
import os

# Initialize Pygame
pygame.init()


# Set up the main screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 1000
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Main Window")

with zipfile.ZipFile('digital-dismay.zip', 'r') as zip_ref:
    zip_ref.extractall()

# Set up font
font_file_path = os.path.join(".", "Digital Dismay.otf")  # Update with the actual font file path
font = pygame.font.Font(font_file_path, 100)

# Set up child windows
CHILD_WIDTH, CHILD_HEIGHT = 700, 650
child_screen1 = pygame.Surface((CHILD_WIDTH, CHILD_HEIGHT), pygame.SRCALPHA)  # Enable per-pixel alpha
child_screen2 = pygame.Surface((CHILD_WIDTH, CHILD_HEIGHT), pygame.SRCALPHA)  # Enable per-pixel alpha

# Fill child windows with transparent color
child_screen1.fill((0, 0, 0, 0))  # Transparent black color
child_screen2.fill((0, 0, 0, 0))  # Transparent black color

# Load the background image
background_image = pygame.image.load("Untitled.jpeg").convert()


# Function to update child window positions
def update_child_positions():
    # Resize the background image
    scaled_background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Draw the background image
    screen.blit(scaled_background_image, (0, 0))
    # Update child window positions
    child_screen1_pos = (40, 50)  # Position relative to main window
    child_screen2_pos = (SCREEN_WIDTH - CHILD_WIDTH - 40, 50)  # Position relative to main window
    screen.blit(child_screen1, child_screen1_pos)
    screen.blit(child_screen2, child_screen2_pos)
    pygame.draw.rect(screen, (128, 128, 128),
                     (child_screen1_pos[0] - 1, child_screen1_pos[1] - 1, CHILD_WIDTH + 2, CHILD_HEIGHT + 2), 2)
    pygame.draw.rect(screen, (128, 128, 128),
                     (child_screen2_pos[0] - 1, child_screen2_pos[1] - 1, CHILD_WIDTH + 2, CHILD_HEIGHT + 2), 2)


# Function to add image and button to child screen
def add_content_to_child_screen(child_screen):
    # Add image to child screen
    image = pygame.image.load("hero logo.jpg").convert_alpha()  # Load your image with alpha channel
    image = pygame.transform.scale(image, (450, 450))  # Scale the image as needed
    child_screen.blit(image, (120, 100))  # Adjust position as needed

    # Define image rectangle
    image_rect = image.get_rect(center=(CHILD_WIDTH // 2, CHILD_HEIGHT // 2))  # Center position of the first image

    # If this is the second child screen, add content specific to it
    if child_screen == child_screen2:
        image1 = pygame.image.load("Expertlogo.jpg").convert_alpha()  # Load your image with alpha channel
        image1 = pygame.transform.scale(image1, (450, 450))  # Scale the image as needed
        child_screen.blit(image1, (130, 100))  # Adjust position as needed

        # Define image rectangle for the second image
        image1_rect = image1.get_rect(center=(CHILD_WIDTH // 2, CHILD_HEIGHT // 2))  # Center position of the second image

        # Check for mouse clicks on the second image
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if image1_rect.collidepoint(mouse_pos):
                show_text_window()  # Perform actions when the second image is clicked


def expert_loading_screen():
    screen_info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h

    # Set up the screen in fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Expert Loading Screen")
    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Create a font object
    font = pygame.font.Font(None, 36)
    loading_text1 = font.render("Dr. TinT strikes again!", True, BLACK)
    loading_text2 = font.render("The Unlikely Hero calls you for instructions...", True, BLACK)

    # Calculate positions for the text
    text_rect1 = loading_text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    text_rect2 = loading_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

    # Gradually increase the opacity (alpha) of the text surfaces
    for alpha in range(0, 256, 5):  # Increase alpha by 5 in each iteration
        loading_text1.set_alpha(alpha)
        loading_text2.set_alpha(alpha)

        screen.fill(WHITE)
        screen.blit(loading_text1, text_rect1)
        screen.blit(loading_text2, text_rect2)
        pygame.display.flip()

        # Add a short delay to control the speed of the fade-in effect
        pygame.time.delay(20)

    # Simulate loading time
    time.sleep(2)


def show_text_window():
    # Set up the text window
    text_window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    pygame.display.set_caption("Text Window")

    # Fill the text window with black color
    text_window.fill((0, 0, 0))

    # Render text with typing effect
    font = pygame.font.SysFont(None, 36)
    text = "While on a train, you receive a text message:"
    text_surface = font.render('', True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 6))
    text_window.blit(text_surface, text_rect)
    pygame.display.update()

    # Typing effect for main message
    for i in range(len(text) + 1):
        text_surface = font.render(text[:i], True, (255, 255, 255))
        text_window.blit(text_surface, text_rect)
        pygame.display.update()
        time.sleep(0.03)

    # Wait for a few seconds
    time.sleep(1)

    image = pygame.image.load("phone.jpg").convert_alpha()
    image = pygame.transform.scale(image, (300, 300))  # Adjust size as needed

    for alpha in range(0, 255, 5):  # Increase transparency gradually
        text_window.fill((0, 0, 0))  # Clear the window
        text_window.blit(text_surface, text_rect)  # Re-blit the text
        faded_image = image.copy()  # Create a copy of the image
        faded_image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)  # Apply alpha value
        image_rect = faded_image.get_rect(midright=(SCREEN_WIDTH - 250, SCREEN_HEIGHT // 2))
        text_window.blit(faded_image, image_rect)  # Blit the faded image
        pygame.display.update()
        pygame.time.delay(15)  # Delay for smoother animation

    # Add a button
    button_font = pygame.font.Font(None, 36)
    button_color = (184, 134, 11)
    button_width, button_height = 320, 50
    button_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 2, SCREEN_HEIGHT - 320, button_width, button_height)
    pygame.draw.rect(text_window, button_color, button_rect)
    button_text = button_font.render("OK, I'm calling for help", True, (255, 255, 255))
    text_window.blit(button_text, button_text.get_rect(center=button_rect.center))
    pygame.display.update()

    time.sleep(1)
    # Add additional text below the button
    additional_text = "Civilian count in the blast zone : 250"
    additional_text_surface = font.render(additional_text, True, (255, 255, 255))
    additional_text_rect = additional_text_surface.get_rect(center=(SCREEN_WIDTH // 2, button_rect.bottom + 50))
    text_window.blit(additional_text_surface, additional_text_rect)
    pygame.display.update()
    time.sleep(1)

    # Add one more text below the additional text
    more_text = "Evacuation currently impossible"
    more_text_surface = font.render(more_text, True, (255, 255, 255))
    more_text_rect = more_text_surface.get_rect(center=(SCREEN_WIDTH // 2, additional_text_rect.bottom + 50))
    text_window.blit(more_text_surface, more_text_rect)
    pygame.display.update()

    # Handle button click event
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    game_screen(screen)


def game_screen(screen):
    orange = (236, 88, 0)
    black = (0, 0, 0)
    green = (0, 128, 0)  # Green color
    white = (255, 255, 255)
    red = (255,0,0)

    # Fill the screen with orange color
    screen.fill(orange)

    paint = pygame.image.load("oldpaint.png")
    paint_rect = paint.get_rect()
    paint = pygame.transform.scale(paint, (50,100))
    paint_position = [(0,100),(0,300),(0,500),(0,700),(1550,100),(1550,300),(1550,500),(1550,700)]

    for pos1 in paint_position :
        paint_rect = pos1
        screen.blit(paint,paint_rect)



    # Draw a rounded rectangle for the main window
    main_rect = pygame.Rect(35, 50, screen.get_width() - 70, screen.get_height() - 100)
    pygame.draw.rect(screen, black, main_rect, border_radius=30)

    # Load bomb image and scale it to fit within the main window
    bomb_bg = pygame.image.load("bomb.jpg")
    bomb_bg_rect = bomb_bg.get_rect()
    bomb_bg_rect = (45, 63, screen.get_width() - 70, screen.get_height() - 90)
    bomb_bg = pygame.transform.scale(bomb_bg, (screen.get_width() - 90, screen.get_height() - 130))


    explosive = pygame.image.load("explosive1.png")
    explosive_rect = explosive.get_rect()
    explosive_rect = (930,560,screen.get_width() - 50,screen.get_height() - 95)
    explosive = pygame.transform.scale(explosive,(480,180))

    red_glow = pygame.image.load("down red light.png")
    red_glow_rect = red_glow.get_rect()
    #red_glow_rect = (60,510,screen.get_width()-1000,screen.get_height()-800)
    red_glow = pygame.transform.scale(red_glow,(480,100))
    glowdown_position = [(60,510),(550,510),(1030,510)]

    battery = pygame.image.load("battery.png")
    battery_rect = battery.get_rect()
    battery_rect = (330, 560, screen.get_width() - 50, screen.get_height() - 95)
    battery = pygame.transform.scale(battery, (280, 200))


    # Display the bomb image
    screen.blit(bomb_bg, bomb_bg_rect)

    screen.blit(explosive,explosive_rect)
    screen.blit(battery,battery_rect)

    for pos in glowdown_position :#shows redglow under every module
        red_glow_rect = pos
        screen.blit(red_glow,red_glow_rect)

    glow_images = [
        pygame.image.load("up red light.png").convert_alpha(),
        pygame.image.load("up red light.png").convert_alpha(),
        pygame.image.load("up red light.png").convert_alpha()
    ]

    glow_images = [pygame.transform.scale(img1, (480 , 100)) for img1 in glow_images]

    # Blit puzzle images onto the screen
    screen.blit(glow_images[0], (60,80))
    screen.blit(glow_images[1], (550,80))
    screen.blit(glow_images[2], (1030,80))

    # Calculate dimensions for puzzle windows
    puzzle_width = (bomb_bg_rect[2] - 60) // 3.1  # Divide the remaining width into three parts
    puzzle_height = (bomb_bg_rect[3] - 40) // 2  # Set the height to half of the bomb image's height

    emptywire = pygame.image.load("emptyleft.png")
    emptywire_rect = emptywire.get_rect()
    emptywire_rect = (630, 200, puzzle_width - 50, puzzle_height - 95)
    emptywire = pygame.transform.scale(emptywire, (50, 300))

    wire1 = pygame.image.load("redwire.png")
    wire1_rect = wire1.get_rect()
    wire1_rect = (680, 200, puzzle_width - 50, puzzle_height - 95)
    wire1 = pygame.transform.scale(wire1, (50, 300))

    wire2 = pygame.image.load("bluewire.png")
    wire2_rect = wire2.get_rect()
    wire2_rect = (730, 200, puzzle_width - 50, puzzle_height - 95)
    wire2 = pygame.transform.scale(wire2, (50, 300))

    wire3 = pygame.image.load("greenwire.png")
    wire3_rect = wire3.get_rect()
    wire3_rect = (780, 200, puzzle_width - 50, puzzle_height - 95)
    wire3 = pygame.transform.scale(wire3, (50, 300))

    wire4 = pygame.image.load("bluewire.png")
    wire4_rect = wire4.get_rect()
    wire4_rect = (830, 200, puzzle_width - 50, puzzle_height - 95)
    wire4 = pygame.transform.scale(wire4, (50, 300))

    emptywire1 = pygame.image.load("emptyright.png")
    emptywire1_rect = emptywire1.get_rect()
    emptywire1_rect = (880, 200, puzzle_width - 50, puzzle_height - 95)
    emptywire1 = pygame.transform.scale(emptywire1, (50, 300))

    click_me = pygame.image.load("clickmebtn.png")
    click_me_rect = click_me.get_rect()
    click_me_rect = (130, 200, puzzle_width - 50, puzzle_height - 95)
    click_me = pygame.transform.scale(click_me, (300, 300))

    timerdis = pygame.image.load("timerdisplay.png")
    timerdis_rect = timerdis.get_rect()
    timerdis_rect = (600, 550, puzzle_width - 50, puzzle_height - 95)
    timerdis = pygame.transform.scale(timerdis, (350, 250))


    # Set positions for puzzle windows
    puzzle1_x = 60
    puzzle1_y = 150

    puzzle2_x = 60 + puzzle_width + 20
    puzzle2_y = 150

    puzzle3_x = 60 + 2 * (puzzle_width + 20)
    puzzle3_y = 150

    # Add three child windows for puzzles
    puzzle1_rect = pygame.Rect(puzzle1_x, puzzle1_y, puzzle_width, puzzle_height)
    pygame.draw.rect(screen, black, puzzle1_rect)

    puzzle2_rect = pygame.Rect(puzzle2_x, puzzle2_y, puzzle_width, puzzle_height)
    pygame.draw.rect(screen, black, puzzle2_rect)

    puzzle3_rect = pygame.Rect(puzzle3_x, puzzle3_y, puzzle_width, puzzle_height)
    pygame.draw.rect(screen, black, puzzle3_rect)

    # Load puzzle images
    puzzle_images = [
        pygame.image.load("motherboard.jpg").convert_alpha(),
        pygame.image.load("motherboard.jpg").convert_alpha(),
        pygame.image.load("motherboard.jpg").convert_alpha()
    ]

    # Scale puzzle images to fit within puzzle windows
    puzzle_images = [pygame.transform.scale(img, (puzzle_width , puzzle_height)) for img in puzzle_images]

    button_margin = 10
    # Blit puzzle images onto the screen
    screen.blit(puzzle_images[0], (puzzle1_x + 0, puzzle1_y + 0))
    screen.blit(puzzle_images[1], (puzzle2_x + 0, puzzle2_y + 0))
    screen.blit(puzzle_images[2], (puzzle3_x + 0, puzzle3_y + 0))

    screen.blit(click_me,click_me_rect)#blits click me button on the module

    screen.blit(emptywire,emptywire_rect)
    screen.blit(wire1,wire1_rect)#blits wire to the module
    screen.blit(wire2,wire2_rect)
    screen.blit(wire3, wire3_rect)
    screen.blit(wire4, wire4_rect)
    screen.blit(emptywire1,emptywire1_rect)



    # Draw quit button
    quit_button_width = 100
    quit_button_height = 40
    quit_button_x = screen.get_width() - 850
    quit_button_y = 10
    quit_button_rect = pygame.Rect(quit_button_x, quit_button_y, quit_button_width, quit_button_height)
    pygame.draw.rect(screen, orange, quit_button_rect)
    quit_font = pygame.font.Font(None, 30)
    quit_text = quit_font.render("QUIT", True, black)
    quit_text_rect = quit_text.get_rect(
        center=(quit_button_x + quit_button_width / 2, quit_button_y + quit_button_height / 2))
    screen.blit(quit_text, quit_text_rect)

    start_time = time.time()
    countdown = 600  # 180 seconds = 3 minutes

    # Extract font from zip file


    while countdown > 0:  # Changed to stop at 0

        # Draw bomb timer
        bomb_timer_width = puzzle_width * 1 + 60 + button_margin * 2  # Reduced width
        bomb_time_height = 190
        bomb_time_x = 500
        bomb_time_y = 553
        new_child_rect = pygame.Rect(bomb_time_x + 105, bomb_time_y, bomb_timer_width - 210, bomb_time_height)
        pygame.draw.rect(screen, black, new_child_rect)


        # Calculate minutes and seconds
        minutes = countdown // 60
        seconds = countdown % 60

        # Add leading zeros if necessary
        timer_text = "{:02d}:{:02d}".format(minutes, seconds)

        # Render timer text
        timer_surface = font.render(timer_text, True, red)
        timer_rect = timer_surface.get_rect(
            center=(bomb_time_x + bomb_timer_width / 2, bomb_time_y + bomb_time_height / 2))
        screen.blit(timer_surface, timer_rect)

        screen.blit(timerdis, timerdis_rect)

        # Update the display
        pygame.display.flip()

        # Wait for a moment
        pygame.time.delay(1000)  # 1000 milliseconds = 1 second

        # Update countdown
        elapsed_time = time.time() - start_time
        countdown = max(0, 600 - int(elapsed_time))  # Changed to stop at 0

        # Check for quit button click
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if quit_button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

    # Quit the game when countdown reaches 0
    pygame.quit()
    sys.exit()






    # Wait for user input
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "main_menu"



def add_main_menu_buttons():
    # Draw buttons on main screen
    button_font = pygame.font.Font(None, 36)
    button_color = (211, 211, 211)
    button_width, button_height = 150, 50

    # Button 1
    button1_rect = pygame.Rect((SCREEN_WIDTH - button_width) // 5, SCREEN_HEIGHT - 250, button_width, button_height)
    pygame.draw.rect(screen, button_color, button1_rect)
    button1_text = button_font.render("How to play", True, (0, 0, 0))
    screen.blit(button1_text, button1_text.get_rect(center=button1_rect.center))

    # Button 2
    button2_rect = pygame.Rect((3 * SCREEN_WIDTH - button_width) // 4, SCREEN_HEIGHT - 250, button_width, button_height)
    pygame.draw.rect(screen, button_color, button2_rect)
    button2_text = button_font.render("Quit", True, (0, 0, 0))
    screen.blit(button2_text, button2_text.get_rect(center=button2_rect.center))

    # Check for mouse events
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button1_rect.collidepoint(mouse_pos):
                print("How to play button clicked!")
                # Add your code to handle the "How to play" button click here
            elif button2_rect.collidepoint(mouse_pos):
                pygame.quit()
                sys.exit()
                # Add your code to handle the "Quit" button click here
def appendix1():
    # Get the screen width and height
    screen_info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h

    # Set up the screen in fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Fullscreen Image")

    # Load the image
    image = pygame.image.load("bomb_fundamental.png")

    # Get the image rectangle
    image_rect = image.get_rect()

    # Set the image position to the center of the screen
    image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Define button properties
    button_width = 20
    button_height = 50
    button_margin = 20
    button_x = 20
    button_y = 20

    # Create a font object
    font = pygame.font.Font(None, 36)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if the mouse click is inside the button
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    return  # Exit the function to return to the fullscreen_with_buttons() function

        # Draw everything
        screen.fill((255, 255, 255))  # Fill the screen with white color
        screen.blit(image, image_rect)  # Blit the image onto the screen at the specified position

        # Draw button
        pygame.draw.rect(screen, (85, 85, 85),
                         (button_x, button_y, button_width, button_height))  # Grey button rectangle
        button_text = font.render("<", True, (0, 0, 0))  # Black button text
        button_text_rect = button_text.get_rect(
            center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(button_text, button_text_rect)  # Blit the button text onto the button rectangle

        pygame.display.flip()

def intro():
    # Get the screen width and height
    screen_info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h

    # Set up the screen in fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Fullscreen Image")

    # Load the image
    image = pygame.image.load("expert_intro.png")

    # Get the image rectangle
    image_rect = image.get_rect()

    # Set the image position to the center of the screen
    image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Define button properties
    button_width = 20
    button_height = 50
    button_margin = 20
    button_x = 20
    button_y = 20

    # Create a font object
    font = pygame.font.Font(None, 36)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if the mouse click is inside the button
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    return  # Exit the function to return to the fullscreen_with_buttons() function

        # Draw everything
        screen.fill((255, 255, 255))  # Fill the screen with white color
        screen.blit(image, image_rect)  # Blit the image onto the screen at the specified position

        # Draw button
        pygame.draw.rect(screen, (85, 85, 85),
                         (button_x, button_y, button_width, button_height))  # Grey button rectangle
        button_text = font.render("<", True, (0, 0, 0))  # Black button text
        button_text_rect = button_text.get_rect(
            center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(button_text, button_text_rect)  # Blit the button text onto the button rectangle

        pygame.display.flip()

def modoperands():
    # Get the screen width and height
    screen_info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h

    # Set up the screen in fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Fullscreen Image")

    # Load the image
    image = pygame.image.load("modoperands.png")

    # Get the image rectangle
    image_rect = image.get_rect()

    # Set the image position to the center of the screen
    image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Define button properties
    button_width = 20
    button_height = 50
    button_margin = 20
    button_x = 20
    button_y = 20

    # Create a font object
    font = pygame.font.Font(None, 36)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if the mouse click is inside the button
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    return  # Exit the function to return to the fullscreen_with_buttons() function

        # Draw everything
        screen.fill((255, 255, 255))  # Fill the screen with white color
        screen.blit(image, image_rect)  # Blit the image onto the screen at the specified position

        # Draw button
        pygame.draw.rect(screen, (85, 85, 85),
                         (button_x, button_y, button_width, button_height))  # Grey button rectangle
        button_text = font.render("<", True, (0, 0, 0))  # Black button text
        button_text_rect = button_text.get_rect(
            center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(button_text, button_text_rect)  # Blit the button text onto the button rectangle

        pygame.display.flip()

def letters_code():
    # Initialize Pygame
    pygame.init()

    # Get the screen width and height
    screen_info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h

    # Set up the screen in fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Fullscreen Image")

    # Load the image
    image = pygame.image.load("module_5_letter.png")

    # Get the image rectangle
    image_rect = image.get_rect()

    # Set the image position to the center of the screen
    image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Define button properties
    button_width = 20
    button_height = 50
    button_margin = 20
    button_x = 20
    button_y = 20

    # Create a font object
    font = pygame.font.Font(None, 36)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if the mouse click is inside the button
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    return  # Exit the function to return to the fullscreen_with_buttons() function

        # Draw everything
        screen.fill((255, 255, 255))  # Fill the screen with white color
        screen.blit(image, image_rect)  # Blit the image onto the screen at the specified position

        # Draw button
        pygame.draw.rect(screen, (85, 85, 85),
                         (button_x, button_y, button_width, button_height))  # Grey button rectangle
        button_text = font.render("<", True, (0, 0, 0))  # Black button text
        button_text_rect = button_text.get_rect(
            center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(button_text, button_text_rect)  # Blit the button text onto the button rectangle

        pygame.display.flip()

def clickmebutton():
    # Initialize Pygame
    pygame.init()

    # Get the screen width and height
    screen_info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h

    # Set up the screen in fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Fullscreen Image")

    # Load the image
    image = pygame.image.load("Clickme.png")

    # Get the image rectangle
    image_rect = image.get_rect()

    # Set the image position to the center of the screen
    image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Define button properties
    button_width = 20
    button_height = 50
    button_margin = 20
    button_x = 20
    button_y = 20

    # Create a font object
    font = pygame.font.Font(None, 36)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if the mouse click is inside the button
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    return  # Exit the function to return to the fullscreen_with_buttons() function

        # Draw everything
        screen.fill((255, 255, 255))  # Fill the screen with white color
        screen.blit(image, image_rect)  # Blit the image onto the screen at the specified position

        # Draw button
        pygame.draw.rect(screen, (85, 85, 85),
                         (button_x, button_y, button_width, button_height))  # Grey button rectangle
        button_text = font.render("<", True, (0, 0, 0))  # Black button text
        button_text_rect = button_text.get_rect(
            center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(button_text, button_text_rect)  # Blit the button text onto the button rectangle

        pygame.display.flip()

def wiretrap():
    # Initialize Pygame
    pygame.init()

    # Get the screen width and height
    screen_info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h

    # Set up the screen in fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Fullscreen Image")

    # Load the image
    image = pygame.image.load("wire_table1.png")

    # Get the image rectangle
    image_rect = image.get_rect()

    # Set the image position to the center of the screen
    image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Define button properties
    button_width = 20
    button_height = 50
    button_margin = 20
    button_x = 20
    button_y = 20
    button1_width = 50
    button1_height = 100
    button1_x = 1500
    button1_y = 500

    # Create a font object
    font = pygame.font.Font(None, 36)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if the mouse click is inside the button
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    return  # Exit the function to return to the fullscreen_with_buttons() function
                elif button1_x <= mouse_x <= button1_x + button1_width and button1_y <= mouse_y <= button1_y + button1_height:
                    wiretrap2()  # Call the wiretrap2 function when the second button is clicked

        # Draw everything
        screen.fill((255, 255, 255))  # Fill the screen with white color
        screen.blit(image, image_rect)  # Blit the image onto the screen at the specified position

        # Draw first button
        pygame.draw.rect(screen, (85, 85, 85),
                         (button_x, button_y, button_width, button_height))  # Grey button rectangle
        button_text = font.render("<", True, (0, 0, 0))  # Black button text
        button_text_rect = button_text.get_rect(
            center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(button_text, button_text_rect)  # Blit the button text onto the button rectangle

        # Draw second button
        button2_x = button1_x + button_width + button_margin  # Calculate x-coordinate for second button
        pygame.draw.rect(screen, (85, 85, 85),
                         (button2_x, button1_y, button1_width, button1_height))  # Grey button rectangle
        button2_text = font.render(">", True, (0, 0, 0))  # Black button text
        button2_text_rect = button2_text.get_rect(
            center=(button2_x + button1_width // 2, button1_y + button1_height // 2))
        screen.blit(button2_text, button2_text_rect)  # Blit the button text onto the button rectangle

        pygame.display.flip()

def wiretrap2():
    # Initialize Pygame
    pygame.init()

    # Get the screen width and height
    screen_info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h

    # Set up the screen in fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Fullscreen Image")

    # Load the image
    image = pygame.image.load("wirtetable2.jpg")

    # Get the image rectangle
    image_rect = image.get_rect()

    # Adjusting image position and size
    image_rect.center = (SCREEN_WIDTH // 2.3 + 100, SCREEN_HEIGHT // 3 + 100)  # Move the image 100 pixels right and 100 pixels down
    new_width = 500 # New width for the image
    new_height = 500  # New height for the image
    image_rect.size = (new_width, new_height)  # Resize the image

    # Define button properties
    button_width = 20
    button_height = 50
    button_x = 20
    button_y = 20

    # Create a font object
    font = pygame.font.Font(None, 36)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if the mouse click is inside the button
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    return  # Exit the function to return to the fullscreen_with_buttons() function

        # Draw everything
        screen.fill((255, 255, 255))  # Fill the screen with white color
        screen.blit(image, image_rect)  # Blit the image onto the screen at the specified position

        # Draw button
        pygame.draw.rect(screen, (85, 85, 85),
                         (button_x, button_y, button_width, button_height))  # Grey button rectangle
        button_text = font.render("<", True, (0, 0, 0))  # Black button text
        button_text_rect = button_text.get_rect(
            center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(button_text, button_text_rect)  # Blit the button text onto the button rectangle

        pygame.display.flip()

def musicnode():
    # Initialize Pygame
    pygame.init()

    # Get the screen width and height
    screen_info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h

    # Set up the screen in fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Fullscreen Image")

    # Load the image
    image = pygame.image.load("musicnode.png")

    # Get the image rectangle
    image_rect = image.get_rect()

    # Set the image position to the center of the screen
    image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Define button properties
    button_width = 20
    button_height = 50
    button_margin = 20
    button_x = 20
    button_y = 20

    # Create a font object
    font = pygame.font.Font(None, 36)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if the mouse click is inside the button
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    return  # Exit the function to return to the fullscreen_with_buttons() function

        # Draw everything
        screen.fill((255, 255, 255))  # Fill the screen with white color
        screen.blit(image, image_rect)  # Blit the image onto the screen at the specified position

        # Draw button
        pygame.draw.rect(screen, (85, 85, 85),
                         (button_x, button_y, button_width, button_height))  # Grey button rectangle
        button_text = font.render("<", True, (0, 0, 0))  # Black button text
        button_text_rect = button_text.get_rect(
            center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(button_text, button_text_rect)  # Blit the button text onto the button rectangle

        pygame.display.flip()


def appendix2():
    # Get the screen width and height
    screen_info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h

    # Set up the screen in fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Fullscreen Image")

    # Load the image
    image = pygame.image.load("bomb_manual.png")

    # Get the image rectangle
    image_rect = image.get_rect()

    # Set the image position to the center of the screen
    image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # Define button properties
    button_width = 20
    button_height = 50
    button_margin = 20
    button_x = 20
    button_y = 20

    # Create a font object
    font = pygame.font.Font(None, 36)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if the mouse click is inside the button
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    return  # Exit the function to return to the fullscreen_with_buttons() function

        # Draw everything
        screen.fill((255, 255, 255))  # Fill the screen with white color
        screen.blit(image, image_rect)  # Blit the image onto the screen at the specified position

        # Draw button
        pygame.draw.rect(screen, (85, 85, 85),
                         (button_x, button_y, button_width, button_height))  # Grey button rectangle
        button_text = font.render("<", True, (0, 0, 0))  # Black button text
        button_text_rect = button_text.get_rect(
            center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(button_text, button_text_rect)  # Blit the button text onto the button rectangle

        pygame.display.flip()

def appendix3():
            # Get the screen width and height
            screen_info = pygame.display.Info()
            SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h

            # Set up the screen in fullscreen mode
            screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            pygame.display.set_caption("Fullscreen Image")

            # Load the image
            image = pygame.image.load("Appendix2.png")

            # Get the image rectangle
            image_rect = image.get_rect()

            # Set the image position to the center of the screen
            image_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

            # Define button properties
            button_width = 20
            button_height = 50
            button_margin = 20
            button_x = 20
            button_y = 20

            # Create a font object
            font = pygame.font.Font(None, 36)

            # Main loop
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        # Check if the mouse click is inside the button
                        if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                            return  # Exit the function to return to the fullscreen_with_buttons() function

                # Draw everything
                screen.fill((255, 255, 255))  # Fill the screen with white color
                screen.blit(image, image_rect)  # Blit the image onto the screen at the specified position

                # Draw button
                pygame.draw.rect(screen, (85, 85, 85),
                                 (button_x, button_y, button_width, button_height))  # Grey button rectangle
                button_text = font.render("<", True, (0, 0, 0))  # Black button text
                button_text_rect = button_text.get_rect(
                    center=(button_x + button_width // 2, button_y + button_height // 2))
                screen.blit(button_text, button_text_rect)  # Blit the button text onto the button rectangle

                pygame.display.flip()

def expert_gamescreen():
    # Initialize Pygame
    pygame.init()

    # Get the screen width and height
    screen_info = pygame.display.Info()
    SCREEN_WIDTH, SCREEN_HEIGHT = screen_info.current_w, screen_info.current_h

    # Set up the screen in fullscreen mode
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Fullscreen with Buttons")

    # Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Create a font object
    font = pygame.font.Font(None, 36)

    # Define button properties
    button_width = 500
    button_height = 50
    button_margin = 20

    # Define button positions
    button1_x = (SCREEN_WIDTH - button_width) // 2
    button1_y = (SCREEN_HEIGHT - (2 * button_height + button_margin)) // 1.1

    button2_x = (SCREEN_WIDTH - button_width) // 2
    button2_y = button1_y + button_height + button_margin

    introbtn_x = (SCREEN_WIDTH - button_width) // 2
    introbtn_y = (SCREEN_HEIGHT - (2 * button_height + button_margin)) // 1.4

    modoperand_x = (SCREEN_WIDTH - button_width) // 2
    modoperand_y = (SCREEN_HEIGHT - (2 * button_height + button_margin)) // 1.3

    appendix1_x = (SCREEN_WIDTH - button_width) // 2
    appendix1_y = (SCREEN_HEIGHT - (2 * button_height + button_margin)) // 1.2

    # Load the image
    flogo = pygame.image.load("5_letter_logo.jpg")
    slogo = pygame.image.load("ClickMe_logo.jpg")
    tlogo = pygame.image.load("wire_logo.jpg")
    fourlogo = pygame.image.load("music_logo.jpg")

    # Define the position and size of the image
    letter_logo_width = 250  # Adjust as needed
    letter_logo_height = 200  # Adjust as needed
    letter_logo_x = 500  # Adjust the X position of the image
    letter_logo_y = 100  # Adjust the Y position of the image
    image_rect = pygame.Rect(letter_logo_x, letter_logo_y, letter_logo_width, letter_logo_height)

    clickme_logo_width = 250  # Adjust as needed
    clickme_logo_height = 200  # Adjust as needed
    clickme_logo_x = 900  # Adjust the X position of the image
    clickme_logo_y = 100  # Adjust the Y position of the image
    simage_rect = pygame.Rect(clickme_logo_x, clickme_logo_y, clickme_logo_width, clickme_logo_height)

    wire_logo_width = 250  # Adjust as needed
    wire_logo_height = 200  # Adjust as needed
    wire_logo_x = 500  # Adjust the X position of the image
    wire_logo_y = 350  # Adjust the Y position of the image
    timage_rect = pygame.Rect(wire_logo_x, wire_logo_y, wire_logo_width, wire_logo_height)

    music_logo_width = 250  # Adjust as needed
    music_logo_height = 200  # Adjust as needed
    music_logo_x = 900  # Adjust the X position of the image
    music_logo_y = 350  # Adjust the Y position of the image
    fourimage_rect = pygame.Rect(music_logo_x, music_logo_y, music_logo_width, music_logo_height)

    # You can also adjust the size of the image using pygame.transform.scale
    flogo = pygame.transform.scale(flogo, (letter_logo_width, letter_logo_height))
    slogo = pygame.transform.scale(slogo, (clickme_logo_width, clickme_logo_height))
    tlogo = pygame.transform.scale(tlogo, (wire_logo_width, wire_logo_height))
    fourlogo = pygame.transform.scale(fourlogo, (music_logo_width, music_logo_height))

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Check if the mouse click is inside button 1
                if button1_x <= mouse_x <= button1_x + button_width and button1_y <= mouse_y <= button1_y + button_height:
                    appendix2()
                # Check if the mouse click is inside button 2
                elif button2_x <= mouse_x <= button2_x + button_width and button2_y <= mouse_y <= button2_y + button_height:
                    appendix3()
                elif introbtn_x <= mouse_x <= introbtn_x + button_width and introbtn_y <= mouse_y <= introbtn_y + button_height:
                    intro()
                elif modoperand_x <= mouse_x <= modoperand_x + button_width and modoperand_y <= mouse_y <= modoperand_y + button_height:
                    modoperands()
                elif appendix1_x <= mouse_x <= appendix1_x + button_width and appendix1_y <= mouse_y <= appendix1_y + button_height:
                    appendix1()
                elif image_rect.collidepoint(mouse_x, mouse_y):
                    letters_code()
                elif simage_rect.collidepoint(mouse_x, mouse_y):
                    clickmebutton()
                elif timage_rect.collidepoint(mouse_x, mouse_y):
                    wiretrap()
                elif fourimage_rect.collidepoint(mouse_x, mouse_y):
                    musicnode()

        # Draw everything
        screen.fill(WHITE)

        # Draw the image
        screen.blit(flogo, image_rect)
        screen.blit(slogo,simage_rect)
        screen.blit(tlogo,timage_rect)
        screen.blit(fourlogo,fourimage_rect)

        # Draw buttons with text
        pygame.draw.rect(screen, WHITE, (introbtn_x, introbtn_y, button_width, button_height))
        button_text1 = font.render("Intro", True, BLACK)
        button_text1_rect = button_text1.get_rect(center=(introbtn_x + button_width // 2, introbtn_y+ button_height // 2))
        screen.blit(button_text1, button_text1_rect)

        pygame.draw.rect(screen, WHITE, (modoperand_x, modoperand_y, button_width, button_height))
        button_text1 = font.render("Dr. TiNT – modus operandi ", True, BLACK)
        button_text1_rect = button_text1.get_rect(center=(modoperand_x + button_width // 2, modoperand_y + button_height // 2))
        screen.blit(button_text1, button_text1_rect)

        pygame.draw.rect(screen, WHITE, (appendix1_x, appendix1_y, button_width, button_height))
        button_text1 = font.render("Appendix 1  bomb defusal - fundamentals ", True, BLACK)
        button_text1_rect = button_text1.get_rect(center=(appendix1_x + button_width // 2, appendix1_y + button_height // 2))
        screen.blit(button_text1, button_text1_rect)

        pygame.draw.rect(screen, WHITE, (button1_x, button1_y, button_width, button_height))
        button_text1 = font.render("Appendix 2 Types of initiating explosives", True, BLACK)
        button_text1_rect = button_text1.get_rect(center=(button1_x + button_width // 2, button1_y + button_height // 2))
        screen.blit(button_text1, button_text1_rect)

        pygame.draw.rect(screen, WHITE, (button2_x, button2_y, button_width, button_height))
        button_text2 = font.render("Appendix 3 The morse alphabet", True, BLACK)
        button_text2_rect = button_text2.get_rect(center=(button2_x + button_width // 2, button2_y + button_height // 2))
        screen.blit(button_text2, button_text2_rect)

        pygame.display.flip()


# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # Resize the main screen
            SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check for mouse click on child screens
            mouse_pos = pygame.mouse.get_pos()
            if child_screen1.get_rect(topleft=(10, 50)).collidepoint(mouse_pos):
                print("Clicked on Child Screen 1!")
            elif child_screen2.get_rect(topleft=(SCREEN_WIDTH - CHILD_WIDTH - 10, 50)).collidepoint(mouse_pos):
                expert_loading_screen()
                expert_gamescreen()

    screen.fill((255, 255, 255))  # Fill the screen with white before drawing the background
    update_child_positions()

    # Add main menu buttons
    add_main_menu_buttons()

    # Add content to child screens
    add_content_to_child_screen(child_screen1)
    add_content_to_child_screen(child_screen2)

    # Update the display
    pygame.display.flip()

pygame.quit()
sys.exit()