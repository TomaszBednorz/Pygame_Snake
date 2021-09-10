import pygame
import random
from pygame.math import Vector2
from enum import IntEnum

# Local imports



# Pygame library initialization
pygame.init()

# Dimensions of the screen
cell_size = 30
cells_on_surface = 24  # 20 cells for game screen and 4 for edges
surface_size = cell_size * cells_on_surface

# Screen initialization
screen = pygame.display.set_mode((surface_size, surface_size))

# Caption and Icon
pygame.display.set_caption("Snake Game")
icon = pygame.image.load('Graphics/snake.png')
pygame.display.set_icon(icon)

# Load font
font = pygame.font.Font('Font/Ballerick.otf', 96)


# States in game
class GameStates(IntEnum):
    PLAY_GAME = 1
    RESULTS = 2
    GAME_RULES = 3
    CREDITS = 4
    EXIT_GAME = 5


# This function draw the main menu board
# 1. Brown sides
# 2. Black edges
# 3. Green board in the center
def draw_board():
    global screen

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
    chunk_color_1 = pygame.Color((0, 221, 0))  # Light green
    chunk_color_2 = pygame.Color((0, 94, 0))  # Dark green
    for i in range(chunks_in_row):
        for j in range(chunks_in_col):
            rect = pygame.Rect(start_square.x * cell_size, start_square.y * cell_size, chunk_width, chunk_height)
            if (i + j) % 2 == 0:
                pygame.draw.rect(screen, chunk_color_1, rect)
            else:
                pygame.draw.rect(screen, chunk_color_2, rect)

            if start_square.x < 2 + chunks_in_row * 3 - 1:
                start_square.x += 4
            else:
                start_square.x = 2
                start_square.y += 4


# This function draw options to choose in the main menu board
def draw_menu_options(state: GameStates):
    states_txt = ["Play game", "Results", "Game rules", "Credits", "Exit game"]

    font_current_state = pygame.Color(225, 0, 0)  # Red color
    font_other_states = pygame.Color(0, 0, 0)  # Black color

    start_x = surface_size / 2
    start_y = cell_size * 4
    offset_y = cell_size * 4

    for i in range(len(states_txt)):
        if i + 1 == state:
            text = font.render(states_txt[i], True, font_current_state)
            text_center = text.get_rect(center=(start_x, start_y + offset_y * i))
            screen.blit(text, text_center)
        else:
            text = font.render(states_txt[i], True, font_other_states)
            text_center = text.get_rect(center=(start_x, start_y + offset_y * i))
            screen.blit(text, text_center)





if __name__ == "__main__":
    game_state = GameStates.PLAY_GAME  # Set beginning  state of game

    draw_board()
    draw_menu_options(game_state)

    game_enable = True

    # Start of the infinity loop
    while game_enable:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                game_enable = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:  # Go down in main menu
                    if game_state < GameStates.EXIT_GAME:
                        game_state += 1
                        draw_menu_options(game_state)

                if event.key == pygame.K_UP:  # Go up in main menu
                    if game_state > GameStates.PLAY_GAME:
                        game_state -= 1
                        draw_menu_options(game_state)

                if event.key == pygame.K_RETURN:
                    if game_state == GameStates.PLAY_GAME:
                        pass
                    elif game_state == GameStates.RESULTS:
                        pass
                    elif game_state == GameStates.GAME_RULES:
                        pass
                    elif game_state == GameStates.CREDITS:
                        pass
                    elif game_state == GameStates.EXIT_GAME:
                        game_enable = False




        pygame.display.update()
    # End of an infinity loop

