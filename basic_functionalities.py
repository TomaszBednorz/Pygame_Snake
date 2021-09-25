import pygame
from pygame.math import Vector2
from enum import IntEnum

# Dimensions of the screen
cell_size = 30
cells_on_surface = 24  # 20 cells for game screen and 4 for edges
surface_size = cell_size * cells_on_surface

# Screen initialization
screen = pygame.display.set_mode((surface_size, surface_size))

# Load font
font96 = pygame.font.Font('Font/Ballerick.otf', 96)
font64 = pygame.font.Font('Font/Ballerick.otf', 64)
font32 = pygame.font.Font('Font/Ballerick.otf', 32)

# Colors
red_color = pygame.Color(225, 0, 0)
black_color = pygame.Color(0, 0, 0)
pink_color = pygame.Color(225, 0, 126)
light_green_color = pygame.Color(0, 221, 0)
dark_green_color = pygame.Color(0, 94, 0)
dark_blue_color = pygame.Color(0, 0, 144)
orange_color = pygame.Color(248, 65, 73)
gold_color = pygame.Color(219, 247, 0)
silver_color = pygame.Color(216, 223, 219)
brown_color = pygame.Color(198, 76, 9)
dark_brown_color = pygame.Color(135, 85, 9)


# Players in game
class Players(IntEnum):
    ONE_PLAYER = 1
    TWO_PLAYERS = 2


# This function draw basic board
# 1. Brown sides
# 2. Black edges
# 3. Green board in the center
def draw_board():
    # Fill the screen with dark brown color
    screen.fill(dark_brown_color)

    # Draw black edges around the game screen
    rect = pygame.Rect(cell_size * 2 - 10, cell_size * 2 - 10, 20 + cell_size * 20, 20 + cell_size * 20)
    pygame.draw.rect(screen, black_color, rect)

    # Draw the board in 2 different types of green color
    start_square = Vector2(2, 2)
    chunks_in_row = 5  # Number of chunks in columns
    chunks_in_col = 5  # Number of chunks in rows
    chunk_height = 4 * cell_size
    chunk_width = 4 * cell_size

    for i in range(chunks_in_row):
        for j in range(chunks_in_col):
            rect = pygame.Rect(start_square.x * cell_size, start_square.y * cell_size, chunk_width, chunk_height)
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, light_green_color, rect)
            else:
                pygame.draw.rect(screen, dark_green_color, rect)

            if start_square.x < 2 + chunks_in_row * 3 - 1:
                start_square.x += 4
            else:
                start_square.x = 2
                start_square.y += 4


# Draw a string on the default screen, x and y are the center of the string
def draw_string(font: pygame.font.Font, string: str, color: pygame.Color, x: int, y: int):
    text = font.render(string, True, color)
    text_center = text.get_rect(center=(x, y))
    screen.blit(text, text_center)