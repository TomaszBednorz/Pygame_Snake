import pygame
from enum import IntEnum

pygame.init()  # Pygame library initialization at the beginning
pygame.font.init()
pygame.mixer.init()

# Local imports
from basic_functionalities import cell_size, surface_size, screen, font96, draw_board, red_color, black_color, \
    Players, draw_string
from game import game_loop
from results import results_loop
from options import options_loop
from credits import credits_loop


# Caption and Icon
pygame.display.set_caption("Snake Game")
icon = pygame.image.load('Graphics/snake.png')
pygame.display.set_icon(icon)


# States in game
class GameStates(IntEnum):
    PLAY_GAME = 1
    RESULTS = 2
    OPTIONS = 3
    CREDITS = 4
    EXIT_GAME = 5


# This function draw options to choose in the main menu board
def draw_menu_options(state: GameStates):
    states_txt = ["Play game", "Results", "Options", "Credits", "Exit game"]

    start_x = surface_size / 2
    start_y = cell_size * 4
    offset_y = cell_size * 4

    for i in range(len(states_txt)):
        if i + 1 == state:
            draw_string(font96, states_txt[i], red_color, start_x, start_y + offset_y * i)
        else:
            draw_string(font96, states_txt[i], black_color, start_x, start_y + offset_y * i)


if __name__ == "__main__":
    game_state = GameStates.PLAY_GAME  # Set beginning  state of game
    players = Players.ONE_PLAYER  # Set beginning amount of players

    draw_board()
    draw_menu_options(game_state)

    pygame.mixer.music.load('Sound/intro.mp3')
    pygame.mixer.music.play()

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
                elif event.key == pygame.K_UP:  # Go up in main menu
                    if game_state > GameStates.PLAY_GAME:
                        game_state -= 1
                elif event.key == pygame.K_ESCAPE:  # Quit game
                    game_enable = False
                elif event.key == pygame.K_RETURN:
                    if game_state == GameStates.PLAY_GAME:
                        #intro_sound.stop()
                        game_loop(players)
                        #intro_sound.play()
                    elif game_state == GameStates.RESULTS:
                        results_loop()
                    elif game_state == GameStates.OPTIONS:
                        players = options_loop(players)
                    elif game_state == GameStates.CREDITS:
                        credits_loop()
                    elif game_state == GameStates.EXIT_GAME:
                        game_enable = False

                    # Reset screen after back to main menu
                    draw_board()
                draw_menu_options(game_state)

        pygame.display.update()
    # End of an infinity loop
