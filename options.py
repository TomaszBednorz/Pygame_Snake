import pygame
import sys

from basic_functionalities import surface_size, screen, font64, font96, draw_board, red_color, black_color, \
                                  pink_color, Players, draw_string


def draw_options_state(players: Players):
    text_X1 = 240  # 1/3 of surface
    text_X2 = 480  # 2/3 of surface

    text_Y = 120  # Start position of first squares line
    offset_Y = 120  # Size of one edge in square

    # Exit text
    draw_string(font96, "Exit", red_color, surface_size / 2, surface_size - surface_size / 6)

    # Arrows image
    arrows_img = pygame.image.load("Graphics/keyboard_arrows.png")
    arrows_center = arrows_img.get_rect(center=(text_X1 - 40, text_Y + offset_Y + 10))
    screen.blit(arrows_img, arrows_center)

    # AWSD image
    awsd_img = pygame.image.load("Graphics/keyboard_awsd.png")
    awsd_center = awsd_img.get_rect(center=(text_X2 + 40, text_Y + offset_Y + 10))
    screen.blit(awsd_img, awsd_center)

    # Texts connected with players
    players_txt = ["Player 1", "Player 2", "Amount of players", "1", "2"]

    draw_string(font64, players_txt[0], black_color, text_X1 - 40, text_Y - 15)
    draw_string(font64, players_txt[1], black_color, text_X2 + 40, text_Y - 15)
    draw_string(font64, players_txt[2], black_color, surface_size / 2, text_Y + 3 * offset_Y - 90)

    current_color = black_color
    if players == Players.ONE_PLAYER:
        current_color = pink_color

    draw_string(font96, players_txt[3], current_color, text_X1, text_Y + offset_Y * 3)

    if players == Players.TWO_PLAYERS:
        current_color = pink_color
    else:
        current_color = black_color

    draw_string(font96, players_txt[4], current_color, text_X2, text_Y + offset_Y * 3)


# Loop of OPTIONS state, return number of players
def options_loop(players: Players):
    end_of_loop = False

    draw_board()  # Reset screen

    draw_options_state(players)

    # Start of the OPTIONS loop
    while not end_of_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:  # Back to main menu
                    end_of_loop = True
                elif event.key == pygame.K_LEFT:  # 1 player option
                    players = Players.ONE_PLAYER
                elif event.key == pygame.K_RIGHT:  # 2 players option
                    players = Players.TWO_PLAYERS

                draw_options_state(players)  # Update screen

        pygame.display.update()
    # End of the OPTIONS loop
    return players
