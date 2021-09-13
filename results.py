import pygame
import sys
from basic_functionalities import Players, font96, font64, font32, red_color, black_color, gold_color, silver_color, \
    brown_color, screen, pink_color, dark_green_color, dark_blue_color, orange_color, surface_size, cell_size, \
    draw_board, draw_string


def draw_results_state(players_mode: Players):
    draw_board()  # Reset screen

    file = None
    if players_mode == Players.ONE_PLAYER:
        file = open('Results_one_player_mode.txt', 'r')
    elif players_mode == Players.TWO_PLAYERS:
        file = open('Results_two_players_mode.txt', 'r')

    lines = file.readlines()
    file.close()

    best_results_points = []
    best_results_nicknames = []

    for line in lines:
        one_of_results = line.split()

        if players_mode == Players.ONE_PLAYER:
            best_results_points.append(int(one_of_results[1]))
            best_results_nicknames.append(one_of_results[0])
        elif players_mode == Players.TWO_PLAYERS:
            best_results_points.append(int(one_of_results[2]))
            best_results_nicknames.append(one_of_results[0] + " " + one_of_results[1])

    # Draw 5 best results
    for i in range(1, 6):
        color = black_color
        if i == 1:
            color = gold_color
        if i == 2:
            color = silver_color
        if i == 3:
            color = brown_color

        max_value = max(best_results_points)
        max_index = best_results_points.index(max_value)

        if players_mode == Players.ONE_PLAYER:
            draw_string(font64, str(i) + ".", color, cell_size * 4, cell_size * 5 + (cell_size + 5) * i * 2)  # Place
            draw_string(font64, best_results_nicknames[max_index], color, cell_size * 12,
                        cell_size * 5 + (cell_size + 5) * i * 2)  # Nickname
            draw_string(font64, str(best_results_points[max_index]), color, cell_size * 20,
                        cell_size * 5 + (cell_size + 5) * i * 2)  # Score
        elif players_mode == Players.TWO_PLAYERS:
            nicknames = best_results_nicknames[max_index].split()
            draw_string(font64, str(i) + ".", color, cell_size * 4, cell_size * 5 + (cell_size + 5) * i * 2)  # Place
            draw_string(font32, nicknames[0], color, cell_size * 12,
                        cell_size * 5 - 17 + (cell_size + 5) * i * 2)  # Nickname 1
            draw_string(font32, nicknames[1], color, cell_size * 12,
                        cell_size * 5 + 17 + (cell_size + 5) * i * 2)  # Nickname 2
            draw_string(font64, str(best_results_points[max_index]), color, cell_size * 20,
                        cell_size * 5 + (cell_size + 5) * i * 2)  # Score

        del best_results_points[max_index]
        del best_results_nicknames[max_index]

    if players_mode == Players.ONE_PLAYER:
        draw_string(font64, "1 player", pink_color, surface_size / 2 - cell_size * 6, cell_size * 20)
        draw_string(font64, "2 players", black_color, surface_size / 2 + cell_size * 6, cell_size * 20)
    elif players_mode == Players.TWO_PLAYERS:
        draw_string(font64, "1 player", black_color, surface_size / 2 - cell_size * 6, cell_size * 20)
        draw_string(font64, "2 players", pink_color, surface_size / 2 + cell_size * 6, cell_size * 20)

    # Top scores
    draw_string(font96, "TOP SCORES", black_color, surface_size / 2, cell_size * 4)

    # Exit text
    draw_string(font64, "Exit", red_color, surface_size / 2, cell_size * 20)


def results_loop():
    end_of_loop = False

    mode = Players.ONE_PLAYER

    draw_results_state(mode)
    pygame.display.update()

    # Start of the CREDITS loop
    while not end_of_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:  # Back to main menu
                    end_of_loop = True
                if event.key == pygame.K_RIGHT:
                    mode = Players.TWO_PLAYERS
                if event.key == pygame.K_LEFT:
                    mode = Players.ONE_PLAYER

                draw_results_state(mode)
                pygame.display.update()

    # End of the CREDITS loop
