import pygame
import sys

from basic_functionalities import surface_size, screen, font32, font96, draw_board, red_color, black_color


def draw_credits_state():
    credits_txt = "Snake icon made by Freepik from www.flaticon.com"
    exit_txt = "Exit"

    text = font32.render(credits_txt, True, black_color)
    text_center = text.get_rect(center=(surface_size / 2, surface_size / 6))
    screen.blit(text, text_center)

    text = font96.render(exit_txt, True, red_color)
    text_center = text.get_rect(center=(surface_size / 2, surface_size - surface_size / 6))
    screen.blit(text, text_center)


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
                if event.key == pygame.K_RETURN:  # Back to main menu
                    end_of_loop = True
    # End of the CREDITS loop
