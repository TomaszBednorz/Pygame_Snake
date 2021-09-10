import pygame
import sys

# from main import screen, cell_size, surface_size, font


class Game:
    pass


# Loop of PLAY_GAME state
def game_loop():
    end_of_loop = False

    # Start of the PLAY_GAME loop
    while not end_of_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                sys.exit()

        pass
    # End of the PLAY_GAME loop
