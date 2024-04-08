import pygame
import sys
import random
import tkinter as tk
from tkinter import messagebox

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
BACKGROUND_COLOR = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PACMAN_RADIUS = 30
GHOST_RADIUS = 30
PELLET_RADIUS = 20

# List of words
word_list = ['SPRINT', 'CLIMB', 'LUNGE', 'HURDLE', 'PEDAL', 'SWING', 'PLANK', 'DANCE', 'STRETCH', 'BOXING']


# Randomly select a target word
target_word = random.choice(word_list)
pellet_letters = list(target_word)
pellet_positions = [(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(len(pellet_letters))]
pellet_index = 0

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Pac-Man initial position and speed
pacman_x, pacman_y = 0, 0
pacman_speed = 5

# Ghosts
num_ghosts = 5
ghost_speed = 1  # Slowed down ghost speed
ghosts = []

# Function to generate a random position for a ghost within screen boundaries
def generate_ghost_position():
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    return x, y

# Generate initial positions for ghosts
for _ in range(num_ghosts):
    ghosts.append({
        'position': generate_ghost_position(),
        'direction': random.choice(['horizontal', 'vertical']),  # Initial random direction
    })

# Set Pac-Man's initial position away from ghosts
while True:
    pacman_x, pacman_y = random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)
    if all(pygame.Rect(pacman_x - PACMAN_RADIUS, pacman_y - PACMAN_RADIUS, PACMAN_RADIUS * 2, PACMAN_RADIUS * 2).colliderect(
            (ghost['position'][0] - GHOST_RADIUS * 2, ghost['position'][1] - GHOST_RADIUS * 2, GHOST_RADIUS * 4, GHOST_RADIUS * 4)) == False for ghost in ghosts):
        break

# Game over flag
game_over = False
#exit_game = False  # Flag to exit the game
exit_game = {'exit_game': False}

# Previous frame space key state
prev_space_pressed = False

# Function to update the result message and send it to the Flask server
def update_result_message(message):
    print(message)  # Print to terminal for debugging purposes
    # emit('update_result_message', {'message': message}, namespace='/game')

def close_game():
    exit_game['exit_game'] = True
    root.destroy()

def show_game_outcome_message(outcome):
    global exit_game,root # Use the global variable

    root = tk.Tk()
    root.withdraw()  # Hide the main window

    if outcome == "win":
        title = "Congratulations!"
        message = "You won the game!"
        color = "green"
    elif outcome == "caught_by_ghost":
        title = "Game Over!"
        message = "Got caught by a ghost."
        color = "red"
    elif outcome == "wrong_pellet":
        title = "Game Over!"
        message = "Wrong pellet eaten."
        color = "red"

    # Create a custom message box
    custom_box = tk.Toplevel(root)
    custom_box.title(title)

    # Customize the appearance
    custom_box.geometry("400x200")  # Adjust the size as needed
    custom_box.configure(bg=color)

    # Create a label with a larger font
    label = tk.Label(custom_box, text=message, font=("Arial", 18), fg="white", bg=color)
    label.pack(pady=20)

    # Add an OK button to close the message box and set the exit_game flag
    ok_button = tk.Button(custom_box, text="OK", command=lambda: [custom_box.destroy(), close_game()], font=("Arial", 14), bg="white")
    ok_button.pack()

    # Center the message box on the screen
    custom_box.update_idletasks()
    screen_width = custom_box.winfo_screenwidth()
    screen_height = custom_box.winfo_screenheight()
    x = (screen_width - custom_box.winfo_width()) // 2
    y = (screen_height - custom_box.winfo_height()) // 2
    custom_box.geometry("+{}+{}".format(x, y))

    # Set the protocol to close the game
    custom_box.protocol("WM_DELETE_WINDOW", close_game)

    # Run the Tkinter event loop
    root.mainloop()



# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            exit_game.exit_game = True  # Set exit_game to True when closing the window

    keys = pygame.key.get_pressed()
    pacman_x += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * pacman_speed
    pacman_y += (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * pacman_speed

    # Wrap Pac-Man around the screen
    pacman_x = (pacman_x + WIDTH) % WIDTH
    pacman_y = (pacman_y + HEIGHT) % HEIGHT

    # Check collision with ghosts
    for ghost in ghosts:
        ghost_x, ghost_y = ghost['position']

        # Move ghosts within screen boundaries and wrap around
        if ghost['direction'] == 'horizontal':
            ghost_x += ghost_speed
            if ghost_x >= WIDTH + GHOST_RADIUS:
                ghost_x = -GHOST_RADIUS
            elif ghost_x <= -GHOST_RADIUS:
                ghost_x = WIDTH + GHOST_RADIUS
        elif ghost['direction'] == 'vertical':
            ghost_y += ghost_speed
            if ghost_y >= HEIGHT + GHOST_RADIUS:
                ghost_y = -GHOST_RADIUS
            elif ghost_y <= -GHOST_RADIUS:
                ghost_y = HEIGHT + GHOST_RADIUS

        ghost['position'] = (ghost_x, ghost_y)

        # Check collision with Pac-Man
        if pygame.Rect(ghost_x - GHOST_RADIUS, ghost_y - GHOST_RADIUS, GHOST_RADIUS * 2, GHOST_RADIUS * 2).colliderect(
                (pacman_x - PACMAN_RADIUS, pacman_y - PACMAN_RADIUS, PACMAN_RADIUS * 2, PACMAN_RADIUS * 2)):
            show_game_outcome_message("caught_by_ghost")
            game_over = True

    # Check collision with pellets
    for i, (pellet_x, pellet_y) in enumerate(pellet_positions):
        if pygame.Rect((pellet_x - PELLET_RADIUS, pellet_y - PELLET_RADIUS, PELLET_RADIUS * 2, PELLET_RADIUS * 2)).colliderect(
                (pacman_x - PACMAN_RADIUS, pacman_y - PACMAN_RADIUS, PACMAN_RADIUS * 2, PACMAN_RADIUS * 2)):

            # Get the letter of the eaten pellet
            eaten_letter = pellet_letters[i] if pellet_letters and i < len(pellet_letters) else None

            if keys[pygame.K_SPACE] and not prev_space_pressed:  # Space key pressed and not pressed in the previous frame
                print(f"Eating pellet: {eaten_letter}")

                # Remove the eaten pellet from the list
                pellet_positions.pop(i)

                if pellet_letters and i < len(pellet_letters):
                    pellet_letters.pop(i)

                if len(pellet_letters) > 0:
                    # Update the next expected letter only if there are more pellets
                    next_expected_letter = pellet_letters[-1]
                    print(f"Next expected letter: {next_expected_letter}")

                if eaten_letter == target_word[len(target_word) - len(pellet_letters) - 1]:
                    # Correct pellet eaten, continue the game
                    if len(pellet_letters) == 0:
                        show_game_outcome_message("win")
                        game_over = True
                else:
                    # Incorrect pellet eaten, end the game
                    show_game_outcome_message("wrong_pellet")
                    game_over = True

    prev_space_pressed = keys[pygame.K_SPACE] # Update the previous frame space key state

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw pellets with letters
    font = pygame.font.Font(None, 36)
    for (pellet_x, pellet_y), letter in zip(pellet_positions, pellet_letters):
        pygame.draw.circle(screen, WHITE, (pellet_x, pellet_y), PELLET_RADIUS)
        text_surface = font.render(letter, True, RED)
        screen.blit(text_surface, (pellet_x - 10, pellet_y - 10))

    # Draw Pac-Man
    pygame.draw.circle(screen, YELLOW, (round(pacman_x), round(pacman_y)), PACMAN_RADIUS)
    pygame.draw.circle(screen, WHITE, (round(pacman_x), round(pacman_y)), PACMAN_RADIUS - 5)

    # Draw Ghosts
    for ghost in ghosts:
        pygame.draw.rect(screen, RED, (ghost['position'][0] - GHOST_RADIUS, ghost['position'][1] - GHOST_RADIUS, GHOST_RADIUS * 2, GHOST_RADIUS * 2))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit the game
pygame.quit()
sys.exit()
