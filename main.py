import pygame
import random
from pygame.math import Vector2
from enum import Enum

# Local imports
from menu import main_menu


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


# States in game
class GameStates(Enum):
    MAIN_MENU = 1
    PLAY_GAME = 2
    RESULTS = 3
    GAME_RULES = 4
    CREDITS = 5
    EXIT_GAME = 6


# This function draw slim black edges around the game map
def draw_edges():
    edges_color = pygame.Color((0, 0, 0))  # Black edges
    rect_1 = pygame.Rect(50, 50, 620, 10)
    rect_2 = pygame.Rect(50, 50, 10, 620)
    rect_3 = pygame.Rect(660, 50, 10, 620)
    rect_4 = pygame.Rect(50, 660, 620, 10)
    pygame.draw.rect(screen, edges_color, rect_1)
    pygame.draw.rect(screen, edges_color, rect_2)
    pygame.draw.rect(screen, edges_color, rect_3)
    pygame.draw.rect(screen, edges_color, rect_4)

if __name__ == "__main__":
    game_state = GameStates.MAIN_MENU  # Set beginning  state of game

    screen.fill((135, 85, 9))  # Fill the screen with brown color
    draw_edges()

    game_enable = True

    # Start of the infinity loop
    while game_enable:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_enable = False

        if game_state == GameStates.MAIN_MENU:
            main_menu()

        pygame.display.update()
    # End of an infinity loop

