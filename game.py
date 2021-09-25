import pygame
import sys
import random
from pygame.math import Vector2
from enum import IntEnum

from basic_functionalities import Players, font96, font64, font32, red_color, black_color, gold_color, silver_color, \
    brown_color, screen, light_green_color, dark_green_color, dark_blue_color, orange_color, surface_size, cell_size, \
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
        self.body = [Vector2(7, 12), Vector2(7 * snake_num, 11), Vector2(7 * snake_num, 10)]
        self.snake_number = snake_num
        self.grass_offset = 60
        self.change_direction = True  # One changing of direction per frame

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

        pygame.draw.circle(screen, snake_color, (int(self.grass_offset + self.body[-1].x * cell_size + cell_size / 2),
                                                 int(self.grass_offset + self.body[-1].y * cell_size + cell_size / 2)),
                           int(cell_size / 2 - 1))

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
            self.change_direction = False  # One changing of direction per frame: disable direction changing

    def update_position(self):
        for i in range(len(self.body) - 1):
            self.body[i] = self.body[i + 1]
        self.body[-1] = self.body[-1] + self.direction
        self.change_direction = True  # One changing of direction per frame: enable direction changing

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
        pygame.draw.circle(screen, red_color, (int(self.grass_offset + self.pos.x * cell_size + cell_size / 2),
                                               int(self.grass_offset + self.pos.y * cell_size + cell_size / 2)),
                           int(cell_size / 2 - 1))


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

        # Sounds
        self.eat_sound = 'Sound/eat.mp3'
        self.game_over_sound = 'Sound/game_over.mp3'
        self.background_sound = 'Sound/background.mp3'

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

        self.play_music(self.background_sound)  # Play background sound

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
            draw_string(font96, "Player 1", dark_blue_color, surface_size / 2, self.grass_start_Y + self.grass_size * 3)

            # 2nd player title
            if self.players_num == Players.TWO_PLAYERS:
                draw_string(font96, "Player 2", orange_color, surface_size / 2,
                            self.grass_start_Y + self.grass_size * 10)

            # 1 & 2 player nicknames
            draw_string(font96, self.player1_name, black_color, surface_size / 2,
                        self.grass_start_Y + self.grass_size * 7)
            draw_string(font96, self.player2_name, black_color, surface_size / 2,
                        self.grass_start_Y + self.grass_size * 14)

            pygame.display.update()  # Update screen

        return True  # Nicknames initialized correctly

    def play_music(self, song):
        pygame.mixer.music.load(song)
        pygame.mixer.music.play()

    def stop_music(self, song):
        pygame.mixer.music.load(song)
        pygame.mixer.music.stop()

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
            self.play_music(self.eat_sound)
        # Apple 2
        if snake.body[-1] == self.apples[1].pos:
            self.points += 1
            self.apple_new_position(1)
            self.apples[1].draw()
            snake.grow_up()
            snake.draw()
            self.play_music(self.eat_sound)

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
        self.apples[0].draw()  # Draw apple
        self.check_apple_collision(self.snake1)  # Check apple collision
        snake1_collision = self.check_snakes_wall_collision(self.snake1)  # Check snake collision

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

        self.stop_music(self.background_sound)  # Disable background sound
        self.play_music(self.game_over_sound)  # Play game over sound


        # fill name fields, if they are empty
        if self.player1_name == "":
            self.player1_name = "xyz"

        if self.players_num == Players.TWO_PLAYERS:
            if self.player2_name == "":
                self.player2_name = "xyz"

        # Save result to file
        result = self.player1_name + " " + self.player2_name + " " + str(self.points) + "\n"

        file = None
        if self.players_num == Players.ONE_PLAYER:
            file = open('Results_one_player_mode.txt', 'a')
        elif self.players_num == Players.TWO_PLAYERS:
            file = open('Results_two_players_mode.txt', 'a')
        file.write(result)
        file.close()

        if self.players_num == Players.ONE_PLAYER:
            file = open('Results_one_player_mode.txt', 'r')
        elif self.players_num == Players.TWO_PLAYERS:
            file = open('Results_two_players_mode.txt', 'r')

        lines = file.readlines()
        file.close()

        best_results_points = []
        best_results_nicknames = []

        # Draw 5 best results
        for line in lines:
            one_of_results = line.split()

            if self.players_num == Players.ONE_PLAYER:
                best_results_points.append(int(one_of_results[1]))
                best_results_nicknames.append(one_of_results[0])
            elif self.players_num == Players.TWO_PLAYERS:
                best_results_points.append(int(one_of_results[2]))
                best_results_nicknames.append(one_of_results[0] + " " + one_of_results[1])

        for i in range(1, 4):
            color = black_color
            if i == 1:
                color = gold_color
            if i == 2:
                color = silver_color
            if i == 3:
                color = brown_color

            max_value = max(best_results_points)
            max_index = best_results_points.index(max_value)

            if self.players_num == Players.ONE_PLAYER:
                draw_string(font64, str(i) + ".", color, cell_size * 4,
                            cell_size * 6 + (cell_size + 5) * i * 3)  # Place
                draw_string(font64, best_results_nicknames[max_index], color, cell_size * 12,
                            cell_size * 6 + (cell_size + 5) * i * 3)  # Nickname
                draw_string(font64, str(best_results_points[max_index]), color, cell_size * 20,
                            cell_size * 6 + (cell_size + 5) * i * 3)  # Score
            elif self.players_num == Players.TWO_PLAYERS:
                nicknames = best_results_nicknames[max_index].split()
                draw_string(font64, str(i) + ".", color, cell_size * 4,
                            cell_size * 6 + (cell_size + 5) * i * 3)  # Place
                draw_string(font32, nicknames[0], color, cell_size * 12,
                            cell_size * 6 - 17 + (cell_size + 5) * i * 3)  # Nickname 1
                draw_string(font32, nicknames[1], color, cell_size * 12,
                            cell_size * 6 + 17 + (cell_size + 5) * i * 3)  # Nickname 2
                draw_string(font64, str(best_results_points[max_index]), color, cell_size * 20,
                            cell_size * 6 + (cell_size + 5) * i * 3)  # Score

            del best_results_points[max_index]
            del best_results_nicknames[max_index]

        draw_string(font64, "Your result: " + str(self.points), black_color, surface_size / 2,
                    self.grass_start_Y + self.grass_size * 2)
        draw_string(font64, "TOP SCORES", black_color, surface_size / 2,
                    self.grass_start_Y + self.grass_size * 5)

        # Exit text
        draw_string(font64, "Exit", red_color, surface_size / 2, self.grass_start_Y + self.grass_size * 18)

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

    def game_pause(self):
        # Pause text
        draw_string(font64, "PAUSE", red_color, surface_size / 2, surface_size / 2)
        pygame.display.update()

        end_of_loop = False
        while not end_of_loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Quit the game
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p or event.key == pygame.K_RETURN:
                        # Disable pause
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
    frame_iteration = 0
    game_speed = 300
    pygame.time.set_timer(SCREEN_UPDATE, game_speed)

    # Start of the PLAY_GAME loop
    while not end_of_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                sys.exit()
            if event.type == SCREEN_UPDATE:  # Update game screen
                if game.game_routine():
                    end_of_loop = True
                frame_iteration += 1
                if frame_iteration >= 50 and game_speed > 100:  # Speed will be higher every fifty frames
                    game_speed -= 10
                    pygame.time.set_timer(SCREEN_UPDATE, game_speed)
                    frame_iteration = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Back to main menu
                    end_of_loop = True
                if event.key == pygame.K_p:  # Pause the game
                    game.game_pause()
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
