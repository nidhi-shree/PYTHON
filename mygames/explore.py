import pygame
import random
import sys
from tkinter import Tk, filedialog

# Initialize Pygame
pygame.init()

# Screen settings
screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Image Puzzle Game - Select Difficulty")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Button settings
button_width, button_height = 100, 40  # Decreased button size
button_gap = 10
buttons = {
    "Easy": pygame.Rect((screen_width / 2 - button_width - button_gap, 150), (button_width, button_height)),
    "Intermediate": pygame.Rect((screen_width / 2 - button_width / 2, 150), (button_width, button_height)),
    "Difficult": pygame.Rect((screen_width / 2 + button_gap, 150), (button_width, button_height)),
}

# Font
font = pygame.font.Font(None, 36)

# Function to display buttons
def draw_buttons():
    screen.fill(WHITE)
    title_text = font.render("Select Difficulty", True, BLACK)
    screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, 50))
    
    for level, rect in buttons.items():
        pygame.draw.rect(screen, GRAY, rect)
        text = font.render(level, True, BLACK)
        screen.blit(text, (rect.x + (button_width - text.get_width()) / 2, rect.y + (button_height - text.get_height()) / 2))

# Function to let user select an image file
def select_image():
    root = Tk()
    root.withdraw()  # Hide Tkinter main window
    file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg *.png *.jpeg")])
    if not file_path:
        print("No file selected. Exiting.")
        sys.exit()
    return file_path

# Game setup
selected_difficulty = None
running = True

# Main loop for selecting difficulty
while running:
    draw_buttons()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for level, rect in buttons.items():
                if rect.collidepoint(event.pos):
                    selected_difficulty = level
                    running = False  # Exit loop after selection

    pygame.display.flip()

# Set grid size based on difficulty selection
if selected_difficulty == "Easy":
    grid_size = 3
elif selected_difficulty == "Intermediate":
    grid_size = 4
elif selected_difficulty == "Difficult":
    grid_size = 5

# Select image
image_path = select_image()

# Load and prepare the image
original_image = pygame.image.load(image_path)
image_width, image_height = original_image.get_size()
piece_width = image_width // grid_size
piece_height = image_height // grid_size

# Update display to match image dimensions for the puzzle
screen = pygame.display.set_mode((image_width, image_height))

# Create puzzle pieces
pieces = []
original_positions = []

# Generate pieces
for row in range(grid_size):
    for col in range(grid_size):
        piece_rect = pygame.Rect(col * piece_width, row * piece_height, piece_width, piece_height)
        piece = original_image.subsurface(piece_rect).copy()
        original_positions.append(piece_rect.topleft)
        pieces.append((piece, piece_rect.topleft))

# Shuffle pieces to create the puzzle (avoid completely matching original positions)
shuffled_positions = original_positions[:]
random.shuffle(shuffled_positions)
pieces = [(pieces[i][0], shuffled_positions[i]) for i in range(len(pieces))]

# Game variables
dragging = False
dragged_piece_index = None
dragged_piece_offset = (0, 0)

# Helper functions for game logic
def is_near(pos1, pos2, threshold=10):
    return abs(pos1[0] - pos2[0]) < threshold and abs(pos1[1] - pos2[1]) < threshold

def check_win():
    return all(pieces[i][1] == original_positions[i] for i in range(len(pieces)))

# Main game loop
running = True
while running:
    screen.fill(WHITE)  # Background color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, (piece, pos) in enumerate(pieces):
                piece_rect = piece.get_rect(topleft=pos)
                if piece_rect.collidepoint(event.pos):
                    dragging = True
                    dragged_piece_index = i
                    dragged_piece_offset = (event.pos[0] - pos[0], event.pos[1] - pos[1])
                    break

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                dragging = False
                current_pos = pieces[dragged_piece_index][1]
                correct_pos = original_positions[dragged_piece_index]
                if is_near(current_pos, correct_pos):
                    pieces[dragged_piece_index] = (pieces[dragged_piece_index][0], correct_pos)

        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                new_pos = (event.pos[0] - dragged_piece_offset[0], event.pos[1] - dragged_piece_offset[1])
                pieces[dragged_piece_index] = (pieces[dragged_piece_index][0], new_pos)

    # Draw puzzle pieces
    for piece, pos in pieces:
        screen.blit(piece, pos)

    # Check for win condition
    if check_win():
        font = pygame.font.Font(None, 74)
        text = font.render("Puzzle Complete!", True, (0, 255, 0))
        screen.blit(text, (50, image_height // 2))

    pygame.display.flip()

