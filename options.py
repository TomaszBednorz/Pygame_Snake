import pygame
import sys

from basic_functionalities import surface_size, screen, font64, font96, draw_board, red_color, black_color, \
                                  pink_color, Players


def draw_options_state(players: Players):

    text_X1 = 240  # 1/3 of surface
    text_X2 = 480  # 2/3 od surface

    text_Y = 120  # Start position of first squares line
    offset_Y = 120  # Size of one edge in square

    # Exit text
    exit_txt = "Exit"
    text = font96.render(exit_txt, True, red_color)
    text_center = text.get_rect(center=(surface_size / 2, surface_size - surface_size / 6))
    screen.blit(text, text_center)

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

    text = font64.render(players_txt[0], True, black_color)
    text_center = text.get_rect(center=(text_X1 - 40, text_Y - 15))
    screen.blit(text, text_center)

    text = font64.render(players_txt[1], True, black_color)
    text_center = text.get_rect(center=(text_X2 + 40, text_Y - 15))
    screen.blit(text, text_center)

    text = font64.render(players_txt[2], True, black_color)
    text_center = text.get_rect(center=(surface_size / 2, text_Y + 3 * offset_Y - 90))
    screen.blit(text, text_center)

    current_color = black_color
    if players == Players.ONE_PLAYER:
        current_color = pink_color

    text = font96.render(players_txt[3], True, current_color)
    text_center = text.get_rect(center=(text_X1, text_Y + offset_Y * 3))
    screen.blit(text, text_center)

    if players == Players.TWO_PLAYER:
        current_color = pink_color
    else:
        current_color = black_color

    text = font96.render(players_txt[4], True, current_color)
    text_center = text.get_rect(center=(text_X2, text_Y + offset_Y * 3))
    screen.blit(text, text_center)


# Loop of OPTIONS state
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
                if event.key == pygame.K_RETURN:  # Back to main menu
                    end_of_loop = True

                if event.key == pygame.K_LEFT:  # 1 player option
                    players = Players.ONE_PLAYER

                if event.key == pygame.K_RIGHT:  # 2 players option
                    players = Players.TWO_PLAYER

                draw_options_state(players)  # Update screen

        pygame.display.update()
    # End of the OPTIONS loop
    return players
