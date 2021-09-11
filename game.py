import pygame
import sys
import random
from pygame.math import Vector2
from enum import IntEnum

from basic_functionalities import Players, font96, font64, font32, red_color, black_color, gold_color, silver_color, \
    brown_color, screen, light_green_color,dark_green_color, dark_blue_color, orange_color, surface_size, cell_size,\
    draw_board, draw_string


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
        self.change_direction = True  # 1 direction changing per frame

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
                                                 self.grass_offset + self.body[-1].y * cell_size + cell_size / 2),
                           cell_size / 2 - 1)

    def turn_direction(self, new_direction: SnakeDirection):
        if self.change_direction:
            if new_direction == SnakeDirection.DOWN:
                if self.direction != Vector2(0, -1):
                    self.direction = Vector2(0, 1)
            elif new_direction == SnakeDirection.UP:
                if self.direction != Vector2(0, 1):
                    self.direction = Vector2(0, -1)
            elif new_direction == SnakeDirection.RIGHT:
                if self.direction != Vector2(-1, 0):
                    self.direction = Vector2(1, 0)
            elif new_direction == SnakeDirection.LEFT:
                if self.direction != Vector2(1, 0):
                    self.direction = Vector2(-1, 0)
            self.change_direction = False

    def update_position(self):
        for i in range(len(self.body) - 1):
            self.body[i] = self.body[i + 1]
        self.body[-1] = self.body[-1] + self.direction
        self.change_direction = True

    def grow_up(self):
        first_block = self.body[0]  # End of snake tail
        second_block = self.body[1]
        diff = first_block - second_block

        self.body.insert(0, self.body[0] + diff)


class Apple:
    def __init__(self):
        self.pos = Vector2(0, 0)
        self.grass_offset = 60

    def random_position(self):
        self.pos.x = random.randint(0, 19)
        self.pos.y = random.randint(0, 19)

    def draw(self):
        pygame.draw.circle(screen, red_color, (self.grass_offset + self.pos.x * cell_size + cell_size / 2,
                                               self.grass_offset + self.pos.y * cell_size + cell_size / 2),
                           cell_size / 2 - 1)


class Game:
    def __init__(self, players: Players):
        self.player1_name = ""
        self.player2_name = ""
        self.points = 0
        self.apples = [Apple(), Apple()]
        self.snake1 = Snake(Players.ONE_PLAYER)
        self.snake2 = Snake(Players.TWO_PLAYERS)
        self.players_num = players

        # Positions
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

    def enter_names(self):
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
                            current_player = Players.TWO_PLAYERS
                            if self.players_num == Players.ONE_PLAYER:  # End this section if in game is only 1 player
                                end_of_loop = True
                        else:
                            if len(self.player1_name) <= 7:  # Nickname max 8 letters
                                self.player1_name += event.unicode
                    elif current_player == Players.TWO_PLAYERS:  # 2nd player
                        if event.key == pygame.K_BACKSPACE:
                            self.player2_name = self.player2_name[:-1]
                        elif event.key == pygame.K_RETURN:
                            end_of_loop = True
                        else:
                            if len(self.player2_name) <= 7:
                                self.player2_name += event.unicode

                    if event.key == pygame.K_ESCAPE:  # Back to main menu
                        return False

            # 1st player title
            text = font96.render("Player 1", True, dark_blue_color)
            text_center = text.get_rect(center=(surface_size / 2, self.grass_start_Y + self.grass_size * 3))
            screen.blit(text, text_center)

            # 2nd player title
            if self.players_num == Players.TWO_PLAYERS:
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

    def apple_new_position(self, apple_num: int):
        self.apples[apple_num].random_position()
        overlap_snake_1 = True
        overlap_snake_2 = True

        while overlap_snake_1 or overlap_snake_2:
            # Apple shouldn't overlap snake 1 & 2
            overlap_snake_1 = False
            overlap_snake_2 = False

            for el in self.snake1.body:
                if el == self.apples[apple_num].pos:
                    overlap_snake_1 = True
                    self.apples[apple_num].random_position()

            if self.players_num == Players.TWO_PLAYERS:
                for el in self.snake2.body:
                    if el == self.apples[apple_num].pos:
                        overlap_snake_2 = True
                        self.apples[apple_num].random_position()

    def game_init(self):
        self.apple_new_position(0)  # Generate new position for apple 1

        if self.players_num == Players.TWO_PLAYERS:
            self.apple_new_position(1)  # Generate new position for apple 2

    def check_apple_collision(self, snake: Snake):
        # Apple 1
        if snake.body[-1] == self.apples[0].pos:
            self.points += 1
            self.apple_new_position(0)
            self.apples[0].draw()  # Show apple in new position
            snake.grow_up()  # Cover old apple by snake body
            snake.draw()
        # Apple 2
        if snake.body[-1] == self.apples[1].pos:
            self.points += 1
            self.apple_new_position(1)
            self.apples[1].draw()
            snake.grow_up()
            snake.draw()

    def check_snakes_wall_collision(self, snake: Snake):
        # Wall
        if snake.body[-1].x < 0 or snake.body[-1].x > 19 or snake.body[-1].y < 0 or snake.body[-1].y > 19:
            return True  # Collision detected

        # Snake preparation
        snake1_cpy = self.snake1.body[:]
        snake2_cpy = self.snake2.body[:]

        if snake == self.snake1:
            snake1_cpy.pop()
        elif snake == self.snake2:
            snake2_cpy.pop()

        # Snake 1
        for el in snake1_cpy:
            if el == snake.body[-1]:
                return True  # Collision detected
        # Snake 2
        if self.players_num == Players.TWO_PLAYERS:
            for el in snake2_cpy:
                if el == snake.body[-1]:
                    return True  # Collision detected
        return False  # No collision detected

    def show_score(self):
        draw_string(font64, "Score: " + str(self.points), black_color, self.grass_size * 5, self.grass_size - 3)

    def game_routine(self):
        snake1_collision = False
        snake2_collision = False

        draw_board()
        self.draw_grass()  # Update grass
        self.snake1.update_position()  # Update snake position
        self.snake1.draw()  # Draw updated snake
        self.apples[0].draw()
        self.check_apple_collision(self.snake1)  # Check apple collision
        snake1_collision = self.check_snakes_wall_collision(self.snake1)

        # TWO_PLAYERS mode
        if self.players_num == Players.TWO_PLAYERS:
            self.snake2.update_position()
            self.snake2.draw()
            self.apples[1].draw()
            self.check_apple_collision(self.snake2)
            snake2_collision = self.check_snakes_wall_collision(self.snake2)

        self.show_score()
        if snake1_collision or snake2_collision:
            self.game_over()
            return True
        else:
            return False

    def game_over(self):
        draw_board()
        self.draw_grass()  # Clear the screen

        if self.player1_name == "":
            self.player1_name = "xyz"

        if self.players_num == Players.TWO_PLAYERS:
            if self.player2_name == "":
                self.player2_name = "xyz"

        # Save result to file
        result = self.player1_name + " " + self.player2_name + " " + str(self.points)

        file = None
        if self.players_num == Players.ONE_PLAYER:
            file = open('Results_one_player_mode.txt', 'a')
        elif self.players_num == Players.TWO_PLAYERS:
            file = open('Results_two_players_mode.txt', 'a')
        file.write(result + "\n")
        file.close()

        if self.players_num == Players.ONE_PLAYER:
            file = open('Results_one_player_mode.txt', 'r')
        elif self.players_num == Players.TWO_PLAYERS:
            file = open('Results_two_players_mode.txt', 'r')

        # Select 3 the best results in particular category
        lines = file.readlines()
        file.close()

        best_results_points = [2, 1, 0]
        best_results_nicknames = ['xyz xyz', 'xyz xyz', 'xyz xyz']

        for line in lines:
            one_of_results = line.split()
            if self.players_num == Players.ONE_PLAYER:
                one_of_results_points = int(one_of_results[1])
                if one_of_results_points > best_results_points[0]:
                    best_results_points[1], best_results_nicknames[1] = best_results_points[0], \
                                                                        best_results_nicknames[0]
                    best_results_points[2], best_results_nicknames[2] = best_results_points[1], \
                                                                        best_results_nicknames[1]
                    best_results_points[0] = one_of_results_points
                    best_results_nicknames[0] = one_of_results[0]
                elif one_of_results_points > best_results_points[1]:
                    best_results_points[2], best_results_nicknames[2] = best_results_points[1], \
                                                                        best_results_nicknames[1]
                    best_results_points[1] = one_of_results_points
                    best_results_nicknames[1] = one_of_results[0]
                elif one_of_results_points > best_results_points[2]:
                    best_results_points[2] = one_of_results_points
                    best_results_nicknames[2] = one_of_results[0]
            elif self.players_num == Players.TWO_PLAYERS:
                one_of_results_points = int(one_of_results[2])
                if one_of_results_points > best_results_points[0]:
                    best_results_points[1], best_results_nicknames[1] = best_results_points[0], \
                                                                        best_results_nicknames[0]
                    best_results_points[2], best_results_nicknames[2] = best_results_points[1], \
                                                                        best_results_nicknames[1]
                    best_results_points[0] = one_of_results_points
                    best_results_nicknames[0] = one_of_results[0] + " " + one_of_results[1]
                elif one_of_results_points > best_results_points[1]:
                    best_results_points[2], best_results_nicknames[2] = best_results_points[1], \
                                                                        best_results_nicknames[1]
                    best_results_points[1] = one_of_results_points
                    best_results_nicknames[1] = one_of_results[0] + " " + one_of_results[1]
                elif one_of_results_points > best_results_points[2]:
                    best_results_points[2] = one_of_results_points
                    best_results_nicknames[2] = one_of_results[0] + " " + one_of_results[1]

        # Show achieved result and 3 the best results

        draw_string(font64, "Your result: " + str(self.points), black_color, surface_size / 2,
                    self.grass_start_Y + self.grass_size * 1)
        draw_string(font64, "TOP SCORES", black_color, surface_size / 2,
                    self.grass_start_Y + self.grass_size * 4)

        if self.players_num == Players.ONE_PLAYER:
            # Place 1
            draw_string(font64, "1.", gold_color, self.grass_start_X + self.grass_size * 2,
                        self.grass_start_Y + self.grass_size * 7)  # Place
            draw_string(font64, best_results_nicknames[0], gold_color, self.grass_start_X + self.grass_size * 8,
                        self.grass_start_Y + self.grass_size * 7)  # Nickname
            draw_string(font64, str(best_results_points[0]), gold_color, self.grass_start_X + self.grass_size * 17,
                        self.grass_start_Y + self.grass_size * 7)  # Score

            # Place 2
            draw_string(font64, "2.", silver_color, self.grass_start_X + self.grass_size * 2,
                        self.grass_start_Y + self.grass_size * 11)
            draw_string(font64, best_results_nicknames[1], silver_color, self.grass_start_X + self.grass_size * 8,
                        self.grass_start_Y + self.grass_size * 11)
            draw_string(font64, str(best_results_points[1]), silver_color, self.grass_start_X + self.grass_size * 17,
                        self.grass_start_Y + self.grass_size * 11)

            # Place 3
            draw_string(font64, "3.", brown_color, self.grass_start_X + self.grass_size * 2,
                        self.grass_start_Y + self.grass_size * 15)
            draw_string(font64, best_results_nicknames[2], brown_color, self.grass_start_X + self.grass_size * 8,
                        self.grass_start_Y + self.grass_size * 15)
            draw_string(font64, str(best_results_points[2]), brown_color, self.grass_start_X + self.grass_size * 17,
                        self.grass_start_Y + self.grass_size * 15)
        elif self.players_num == Players.TWO_PLAYERS:
            # Place 1
            nicknames_place_1 = best_results_nicknames[0].split()
            draw_string(font96, "1.", gold_color, self.grass_start_X + self.grass_size * 2,
                        self.grass_start_Y + self.grass_size * 7)  # Place
            draw_string(font64, nicknames_place_1[0], gold_color, self.grass_start_X + self.grass_size * 8,
                        self.grass_start_Y + self.grass_size * 6)  # Nickname 1
            draw_string(font64, nicknames_place_1[1], gold_color, self.grass_start_X + self.grass_size * 8,
                        self.grass_start_Y + self.grass_size * 8)  # Nickname 2
            draw_string(font96, str(best_results_points[0]), gold_color, self.grass_start_X + self.grass_size * 17,
                        self.grass_start_Y + self.grass_size * 7)  # Score

            # Place 2
            nicknames_place_2 = best_results_nicknames[1].split()
            draw_string(font96, "2.", silver_color, self.grass_start_X + self.grass_size * 2,
                        self.grass_start_Y + self.grass_size * 11)
            draw_string(font64, nicknames_place_2[0], silver_color, self.grass_start_X + self.grass_size * 8,
                        self.grass_start_Y + self.grass_size * 10)
            draw_string(font64, nicknames_place_2[1], silver_color, self.grass_start_X + self.grass_size * 8,
                        self.grass_start_Y + self.grass_size * 12)
            draw_string(font96, str(best_results_points[1]), silver_color, self.grass_start_X + self.grass_size * 17,
                        self.grass_start_Y + self.grass_size * 11)

            # Place 3
            nicknames_place_3 = best_results_nicknames[2].split()
            draw_string(font96, "3.", brown_color, self.grass_start_X + self.grass_size * 2,
                        self.grass_start_Y + self.grass_size * 15)
            draw_string(font64, nicknames_place_3[0], brown_color, self.grass_start_X + self.grass_size * 8,
                        self.grass_start_Y + self.grass_size * 14)
            draw_string(font64, nicknames_place_3[1], brown_color, self.grass_start_X + self.grass_size * 8,
                        self.grass_start_Y + self.grass_size * 16)
            draw_string(font96, str(best_results_points[2]), brown_color, self.grass_start_X + self.grass_size * 17,
                        self.grass_start_Y + self.grass_size * 15)

        # Exit text
        draw_string(font64, "Exit", red_color, surface_size / 2, self.grass_start_Y + self.grass_size * 19)

        pygame.display.update()
        end_of_loop = False
        while not end_of_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the game
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Back to main menu
                        end_of_loop = True
                    if event.key == pygame.K_RETURN:  # Back to main menu
                        end_of_loop = True


# Loop of PLAY_GAME state
def game_loop(players: Players):
    end_of_loop = False
    random.seed(None)

    game = Game(players)  # Create the game

    game.draw_grass()  # Clear the screen
    if not game.enter_names():  # Enter player/s name/s
        end_of_loop = True  # Player clicked ESCAPE during method execution, back to main menu

    game.game_init()

    # New event
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 200)

    # Start of the PLAY_GAME loop
    while not end_of_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                sys.exit()
            if event.type == SCREEN_UPDATE:  # Update game screen
                if game.game_routine():
                    end_of_loop = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Back to main menu
                    end_of_loop = True
                # Snake 1 movement
                if event.key == pygame.K_UP:
                    game.snake1.turn_direction(SnakeDirection.UP)
                if event.key == pygame.K_DOWN:
                    game.snake1.turn_direction(SnakeDirection.DOWN)
                if event.key == pygame.K_LEFT:
                    game.snake1.turn_direction(SnakeDirection.LEFT)
                if event.key == pygame.K_RIGHT:
                    game.snake1.turn_direction(SnakeDirection.RIGHT)
                # Snake 2 movement
                if players == Players.TWO_PLAYERS:
                    if event.key == pygame.K_w:
                        game.snake2.turn_direction(SnakeDirection.UP)
                    if event.key == pygame.K_s:
                        game.snake2.turn_direction(SnakeDirection.DOWN)
                    if event.key == pygame.K_a:
                        game.snake2.turn_direction(SnakeDirection.LEFT)
                    if event.key == pygame.K_d:
                        game.snake2.turn_direction(SnakeDirection.RIGHT)

        pygame.display.update()
    # End of the PLAY_GAME loop
