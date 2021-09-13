import pygame
import sys

from basic_functionalities import surface_size, screen, font32, font96, draw_board, red_color, black_color, draw_string


def draw_credits_state():
    credits_txt = ["Snake icon made by Freepik from www.flaticon.com",
                   "Arrows icon made by Smashicons from www.flaticon.com",
                   "AWSD icon made by Smashicons from www.flaticon.com"]

    offset_Y = 120

    draw_string(font32, credits_txt[0], black_color, surface_size / 2, surface_size / 6)
    draw_string(font32, credits_txt[1], black_color, surface_size / 2, surface_size / 6 + offset_Y)
    draw_string(font32, credits_txt[2], black_color, surface_size / 2, surface_size / 6 + 2 * offset_Y)
    draw_string(font96, "Exit", red_color, surface_size / 2, surface_size - surface_size / 6)


# Loop of CREDITS state
def credits_loop():
    end_of_loop = False

    draw_board()  # Reset screen
    draw_credits_state()

    pygame.display.update()

    # Start of the CREDITS loop
    while not end_of_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:  # Back to main menu
                    end_of_loop = True
    # End of the CREDITS loop
