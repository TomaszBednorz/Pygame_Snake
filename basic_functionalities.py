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
light_green_color = pygame.Color((0, 221, 0))
dark_green_color = pygame.Color((0, 94, 0))
dark_blue_color = pygame.Color((0, 0, 144))
orange_color = pygame.Color((248, 65, 73))


# Players in game
class Players(IntEnum):
    ONE_PLAYER = 1
    TWO_PLAYER = 2


# This function draw basic board
# 1. Brown sides
# 2. Black edges
# 3. Green board in the center
def draw_board():
    # Fill the screen with brown color
    screen.fill((135, 85, 9))

    # Draw black edges
    edges_color = pygame.Color((0, 0, 0))  # Black edges
    rect_1 = pygame.Rect(50, 50, 620, 10)
    rect_2 = pygame.Rect(50, 50, 10, 620)
    rect_3 = pygame.Rect(660, 50, 10, 620)
    rect_4 = pygame.Rect(50, 660, 620, 10)
    pygame.draw.rect(screen, edges_color, rect_1)
    pygame.draw.rect(screen, edges_color, rect_2)
    pygame.draw.rect(screen, edges_color, rect_3)
    pygame.draw.rect(screen, edges_color, rect_4)

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