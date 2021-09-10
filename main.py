import pygame
from enum import IntEnum

pygame.init()  # Pygame library initialization at the beginning

# Local imports
from basic_functionalities import cell_size, surface_size, screen, font96, draw_board, red_color, black_color, Players
from game import game_loop
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
            text = font96.render(states_txt[i], True, red_color)
            text_center = text.get_rect(center=(start_x, start_y + offset_y * i))
            screen.blit(text, text_center)
        else:
            text = font96.render(states_txt[i], True, black_color)
            text_center = text.get_rect(center=(start_x, start_y + offset_y * i))
            screen.blit(text, text_center)


if __name__ == "__main__":
    game_state = GameStates.PLAY_GAME  # Set beginning  state of game
    players = Players.ONE_PLAYER  # Set beginning amount of players

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

                if event.key == pygame.K_UP:  # Go up in main menu
                    if game_state > GameStates.PLAY_GAME:
                        game_state -= 1

                if event.key == pygame.K_RETURN:
                    if game_state == GameStates.PLAY_GAME:
                        game_loop()
                    elif game_state == GameStates.RESULTS:
                        pass
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
