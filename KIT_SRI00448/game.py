from typing import KeysView
import pygame
import random

pygame.init()

# Get the screen width and height
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

# Set the window size to match the screen size
WINDOW_WIDTH = SCREEN_WIDTH
WINDOW_HEIGHT = SCREEN_HEIGHT
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Puzzle Game')

FPS = 10
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CRIMSON = (220, 20, 60)
ORANGE = (255, 127, 0)
LIGHT_BLUE = (173, 216, 230)  # Change this color to sky blue/light blue
GREEN=(0,255,0)
level_images = {
    1: 'static\\img\\Level1.jpg',
    2: 'static\\img\\Level2.jpg',
    3: 'static\\img\\Level3.jpg',
}

current_level = 1

bg_home = pygame.image.load('static\\img\\Background.jpg')  # Add your home background image
bg_home = pygame.transform.scale(bg_home, (WINDOW_WIDTH, WINDOW_HEIGHT))
bg_home_rect = bg_home.get_rect()

bg = pygame.image.load(level_images[current_level])
bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
bg_rect = bg.get_rect()

font_title = pygame.font.Font('static\\Hello Avocado.ttf', 64)
font_content = pygame.font.Font('static\\Hello Avocado.ttf', 40)

# start screen
title_text = font_title.render('Puzzle Game', True, RED)  # Change font color to sky blue/light blue
title_rect = title_text.get_rect()
title_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80)

choose_text = font_content.render('Choose your level', True, ORANGE)  # Change font color to sky blue/light blue
choose_rect = choose_text.get_rect()
choose_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20)

# Rounded button for Level 1
level1_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 40, 200, 50)
pygame.draw.rect(screen, GREEN, level1_button_rect, border_radius=10)
level1_text = font_content.render("1- Level 1", True, LIGHT_BLUE)
level1_text_rect = level1_text.get_rect(center=level1_button_rect.center)

# Add vertical offset for Level 2 button
vertical_offset_level2 = 20  # Adjust this value to set the gap between Level 1 and Level 2
level2_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 90 + vertical_offset_level2, 200, 50)
pygame.draw.rect(screen, GREEN, level2_button_rect, border_radius=10)
level2_text = font_content.render("2 - Level 2", True, LIGHT_BLUE)
level2_text_rect = level2_text.get_rect(center=level2_button_rect.center)

# Add vertical offset for Level 3 button
vertical_offset_level3 = 40  # Adjust this value to set the gap between Level 2 and Level 3
level3_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 140 + vertical_offset_level3, 200, 50)
pygame.draw.rect(screen, GREEN, level3_button_rect, border_radius=10)
level3_text = font_content.render("3- Level 3", True, LIGHT_BLUE)
level3_text_rect = level3_text.get_rect(center=level3_button_rect.center)

# end screen
play_again_text = font_title.render('Play Again?', True, WHITE)
play_again_rect = play_again_text.get_rect()
play_again_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

continue_text = font_content.render('Press Space', True, WHITE)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50)

selected_img = None
is_game_over = False
game_completed = False  # Initialize game completion status
show_start_screen = True  # Initial state is the start screen

# ... (previous code)

rows = None
cols = None

cell_width = None
cell_height = None

cells = []


def start_game(mode):
    global cells, cell_width, cell_height, show_start_screen, game_completed, rows, cols

    rows = mode
    cols = mode
    num_cells = rows * cols

    cell_width = WINDOW_WIDTH // rows
    cell_height = WINDOW_HEIGHT // cols

    cell = []
    rand_indexes = list(range(0, num_cells))

    for i in range(num_cells):
        x = (i % rows) * cell_width
        y = (i // cols) * cell_height
        rect = pygame.Rect(x, y, cell_width, cell_height)
        rand_pos = random.choice(rand_indexes)
        rand_indexes.remove(rand_pos)
        cells.append({'rect': rect, 'border': WHITE, 'order': i, 'pos': rand_pos})

    show_start_screen = False


# ... (previous code)
minimize_icon = pygame.font.Font(None, 36).render('-', True, (0, 0, 0))
#maximize_icon = pygame.font.Font(None, 36).render('x', True, (255, 0, 0))

minimize_rect = minimize_icon.get_rect(topleft=(WINDOW_WIDTH - 60, 10))
#maximize_rect = maximize_icon.get_rect(topleft=(WINDOW_WIDTH - 30, 10))

# Add a close button
close_icon = pygame.font.Font(None, 36).render('X', True, (255, 0, 0))
close_rect = close_icon.get_rect(topleft=(WINDOW_WIDTH - 90, 10))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle events for minimize, maximize, and close icons
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if minimize_rect.collidepoint(mouse_pos):
                pygame.display.iconify()  # Minimize the window  # Toggle fullscreen
            elif close_rect.collidepoint(mouse_pos):
                running = False  # Handle the close button event
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False   # Handle the close button event
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # Handle space bar key press
            if event.key == pygame.K_SPACE:
                if is_game_over or game_completed:
                    # If the game is over or completed, transition to the start screen
                    is_game_over = False
                    show_start_screen = True
                    game_completed = False  # Reset game completion status
                    selected_img = None  # Reset selected image
                    cells = []  # Reset cells list

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not is_game_over:
            mouse_pos = pygame.mouse.get_pos()

            # Check if the game is in the start screen mode
            if show_start_screen:
                # Check if Level 1 button is clicked
                if level1_button_rect.collidepoint(mouse_pos):
                    current_level = 1
                    bg = pygame.image.load(level_images[current_level])
                    bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
                    start_game(3)
                    selected_img = None  # Reset selected image

                # Check if Level 2 button is clicked
                elif level2_button_rect.collidepoint(mouse_pos):
                    current_level = 2
                    bg = pygame.image.load(level_images[current_level])
                    bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
                    start_game(4)
                    selected_img = None  # Reset selected image

                # Check if Level 3 button is clicked
                elif level3_button_rect.collidepoint(mouse_pos):
                    current_level = 3
                    bg = pygame.image.load(level_images[current_level])
                    bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
                    start_game(5)
                    selected_img = None  # Reset selected image
            else:
                # If the game is not in the start screen mode, handle the puzzle piece clicks
                for cell in cells:
                    rect = cell['rect']
                    order = cell['order']

                    if rect.collidepoint(mouse_pos):
                        if not selected_img:
                            selected_img = cell
                            cell['border'] = RED
                        else:
                            current_img = cell
                            if current_img['order'] != selected_img['order']:
                                # swap images
                                temp = selected_img['pos']
                                cells[selected_img['order']]['pos'] = cells[current_img['order']]['pos']
                                cells[current_img['order']]['pos'] = temp

                                cells[selected_img['order']]['border'] = WHITE
                                selected_img = None

                                # check if the puzzle is solved
                                is_game_over = all(cell['order'] == cell['pos'] for cell in cells)

    if show_start_screen:
        screen.blit(bg_home, bg_home_rect)
        screen.blit(title_text, title_rect)
        screen.blit(choose_text, choose_rect)
        pygame.draw.rect(screen, ORANGE, level1_button_rect, border_radius=10)
        screen.blit(level1_text, level1_text_rect)
        pygame.draw.rect(screen, ORANGE, level2_button_rect, border_radius=10)
        screen.blit(level2_text, level2_text_rect)
        pygame.draw.rect(screen, ORANGE, level3_button_rect, border_radius=10)
        screen.blit(level3_text, level3_text_rect)
    else:
        screen.fill(WHITE)

        if not is_game_over:
            for i, val in enumerate(cells):
                pos = cells[i]['pos']
                img_area = pygame.Rect(cells[pos]['rect'].x, cells[pos]['rect'].y, cell_width, cell_height)
                screen.blit(bg, cells[i]['rect'], img_area)
                pygame.draw.rect(screen, cells[i]['border'], cells[i]['rect'], 1)
        else:
            screen.blit(bg, bg_rect)
            screen.blit(play_again_text, play_again_rect)
            screen.blit(continue_text, continue_rect)
            game_completed = True  # Mark the game as completed

    screen.blit(minimize_icon, minimize_rect)
    
    screen.blit(close_icon, close_rect)
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
