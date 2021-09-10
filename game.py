import pygame
import sys
import random
from pygame.math import Vector2

from basic_functionalities import Players, font96, red_color, black_color, surface_size, screen, light_green_color, \
    dark_green_color, dark_blue_color, orange_color, surface_size


class Snake:
    def __init__(self, snake_num):
        self.direction = Vector2(0, 1)
        self.body = [Vector2(7 * snake_num, 12), Vector2(7 * snake_num, 11), Vector2(7 * snake_num, 10)]


class Apple:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.amount = 0

    def random_position(self):
        x = random.randint(0, 20)
        y = random.randint(0, 20)
        self.pos = Vector2(x, y)


class Game:
    def __init__(self):
        self.player1_name = ""
        self.player2_name = ""
        self.points = 0
        self.grass_start_X = 60
        self.grass_start_Y = 60
        self.grass_size = 30
        self.grass_number = 20

    def draw_grass(self):
        for i in range(self.grass_number):
            for j in range(self.grass_number):
                pos_x = self.grass_start_X + i * self.grass_size
                pos_y = self.grass_start_Y + j * self.grass_size
                rect = pygame.Rect(pos_x, pos_y, self.grass_size, self.grass_size)
                if (i + j) % 2 == 0:
                    pygame.draw.rect(screen, light_green_color, rect)
                else:
                    pygame.draw.rect(screen, dark_green_color, rect)

    def enter_names(self, players):
        end_of_loop = False
        current_player = Players.ONE_PLAYER  # Player one chooses nickname firstly

        while not end_of_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the game
                    sys.exit()
                if event.type == pygame.KEYDOWN:  # Update nickname
                    self.draw_grass()  # Reset screen before update text
                    if current_player == Players.ONE_PLAYER:  # 1st player
                        if event.key == pygame.K_BACKSPACE:
                            self.player1_name = self.player1_name[:-1]
                        elif event.key == pygame.K_RETURN:
                            current_player = Players.TWO_PLAYER
                        else:
                            self.player1_name += event.unicode
                    elif current_player == Players.TWO_PLAYER:  # 2nd player
                        if players == Players.ONE_PLAYER:  # End this section if in game is only 1 player
                            end_of_loop = True
                        if event.key == pygame.K_BACKSPACE:
                            self.player2_name = self.player2_name[:-1]
                        elif event.key == pygame.K_RETURN:
                            end_of_loop = True
                        else:
                            self.player2_name += event.unicode

                    if event.key == pygame.K_ESCAPE:  # Back to main menu
                        end_of_loop = True

            # 1st player title
            text = font96.render("Player 1", True, dark_blue_color)
            text_center = text.get_rect(center=(surface_size / 2, self.grass_start_Y + self.grass_size * 3))
            screen.blit(text, text_center)

            # 2nd player title
            if players == Players.TWO_PLAYER:
                text = font96.render("Player 2", True, orange_color)
                text_center = text.get_rect(center=(surface_size / 2, self.grass_start_Y + self.grass_size * 10))
                screen.blit(text, text_center)

            # 1 & 2 player nicknames
            text = font96.render(self.player1_name, True, black_color)
            text_center = text.get_rect(center=(surface_size / 2, self.grass_start_Y + self.grass_size * 7))
            screen.blit(text, text_center)

            text = font96.render(self.player2_name, True, black_color)
            text_center = text.get_rect(center=(surface_size / 2, self.grass_start_Y + self.grass_size * 14))
            screen.blit(text, text_center)

            pygame.display.update()  # Update screen


# clock = pygame.time.Clock()


# Loop of PLAY_GAME state
def game_loop(players):
    end_of_loop = False

    random.seed(None)

    game = Game()  # Create the game

    game.draw_grass()  # Draw grass on the board
    game.enter_names(players)  # Enter player/s name/s

    # Start of the PLAY_GAME loop
    while not end_of_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                sys.exit()
            if event.key == pygame.K_ESCAPE:  # Back to main menu
                end_of_loop = True
        pygame.display.update()
    # End of the PLAY_GAME loop
