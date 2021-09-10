import pygame
import sys
import random
from pygame.math import Vector2
from enum import IntEnum

from basic_functionalities import Players, font96, red_color, black_color, surface_size, screen, light_green_color, \
    dark_green_color, dark_blue_color, orange_color, surface_size, cell_size


# Snake directions
class SnakeDirection(IntEnum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


class Snake:
    def __init__(self, snake_num: Players):
        self.direction = Vector2(0, -1)
        self.body = [Vector2(7 * snake_num, 12), Vector2(7 * snake_num, 11), Vector2(7 * snake_num, 10)]
        self.snake_number = snake_num
        self.grass_offset = 60

    def draw(self):
        if self.snake_number == Players.ONE_PLAYER:
            snake_color = dark_blue_color  # Player 1 color for snake
        else:
            snake_color = orange_color  # Player 2 color for snake

        # Draw tail
        for el in self.body[:-1]:
            rect = pygame.Rect(self.grass_offset + el.x * cell_size, self.grass_offset + el.y * cell_size,
                               cell_size, cell_size)
            pygame.draw.rect(screen, black_color, rect)

            rect = pygame.Rect(self.grass_offset + el.x * cell_size + 2, self.grass_offset + el.y * cell_size + 2,
                               cell_size - 4, cell_size - 4)
            pygame.draw.rect(screen, snake_color, rect)

        # Draw head
        rect = pygame.Rect(self.grass_offset + self.body[-1].x * cell_size,
                           self.grass_offset + self.body[-1].y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, black_color, rect)

        pygame.draw.circle(screen, snake_color, (self.grass_offset + self.body[-1].x * cell_size + cell_size / 2,
                           self.grass_offset + self.body[-1].y * cell_size + cell_size / 2), cell_size / 2 - 1)

    def turn_direction(self, new_direction: SnakeDirection):
        if new_direction == SnakeDirection.DOWN:
            if self.direction != SnakeDirection.UP:
                self.direction = Vector2(0, 1)
        elif new_direction == SnakeDirection.UP:
            if self.direction != SnakeDirection.DOWN:
                self.direction = Vector2(0, -1)
        elif new_direction == SnakeDirection.RIGHT:
            if self.direction != SnakeDirection.LEFT:
                self.direction = Vector2(1, 0)
        elif new_direction == SnakeDirection.LEFT:
            if self.direction != SnakeDirection.RIGHT:
                self.direction = Vector2(-1, 0)

    def update_position(self):
        pass  # Pierwszy ma nową pozycję, a każdy kolejny pozycje tego przed nim

    def grow_up(self):
        pass


class Apple:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.amount = 0

    def random_position(self):
        self.pos.x = random.randint(0, 20)
        self.pos.y = random.randint(0, 20)


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

    def enter_names(self, players: Players):
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
                            if players == Players.ONE_PLAYER:  # End this section if in game is only 1 player
                                end_of_loop = True
                        else:
                            self.player1_name += event.unicode
                    elif current_player == Players.TWO_PLAYER:  # 2nd player
                        if event.key == pygame.K_BACKSPACE:
                            self.player2_name = self.player2_name[:-1]
                        elif event.key == pygame.K_RETURN:
                            end_of_loop = True
                        else:
                            self.player2_name += event.unicode

                    if event.key == pygame.K_ESCAPE:  # Back to main menu
                        return False

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

        return True  # Nicknames initialized correctly

# clock = pygame.time.Clock()


# Loop of PLAY_GAME state
def game_loop(players: Players):
    end_of_loop = False
    random.seed(None)

    # Create 2 snakes, but only 1 will be used if one player was selected
    snake1 = Snake(Players.ONE_PLAYER)
    snake2 = Snake(Players.TWO_PLAYER)

    game = Game()  # Create the game

    game.draw_grass()  # Draw grass on the board

    if not game.enter_names(players):  # Enter player/s name/s
        end_of_loop = True  # Player clicked ESCAPE during method execution, back to main menu

    game.draw_grass()

    snake1.draw()
    if players == Players.TWO_PLAYER:
        snake2.draw()

    # Start of the PLAY_GAME loop
    while not end_of_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Back to main menu
                    end_of_loop = True
        pygame.display.update()
    # End of the PLAY_GAME loop
