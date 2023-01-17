import random  # used to generate location of food items
import pygame  # used to display the game terminal
from collections import defaultdict
import pickle
import numpy
import sys
from math import sqrt


# Graphics
WHITE = (255, 255, 255)
GREEN = (0, 201, 87)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (105, 105, 105)
ORANGE = (255, 165, 0)

SNAKE_SIZE = 40  # snake square size
clock = pygame.time.Clock()

pygame.init()
score_font = pygame.font.SysFont('ubuntu', 15)              # Font for the score
BG = pygame.image.load("images/BG.jpg")                     # Background of the game window

directions = {
    'up': (0, -SNAKE_SIZE),
    'down': (0, SNAKE_SIZE),
    'right': (SNAKE_SIZE, 0),
    'left': (-SNAKE_SIZE, 0)
}


# levels of speed
LOW = 8
MID = 25
HIGH = 999999999999999999999999999999


# default dictionary's default value
def def_value():
    return [(0, 'player')]


class SnakeEnv:

    def __init__(self, display, width, height):
        self.game_display = display
        self.width = width
        self.height = height
        self.game_closed = False  # Boolean to check if the game terminal is closed
        self.snake_speed = LOW

        self.head = (self.width // 2, self.height // 2)
        self.snake_pixels = []
        self.snake_length = 0
        self.scoreboard = {}
        self.load_scoreboard()
        self.max_score = 0

        self.rules = ['basic']
        self.walls = [(0, 0), (0, height - SNAKE_SIZE), (width - SNAKE_SIZE, 0),
                      (width - SNAKE_SIZE, height - SNAKE_SIZE),
                      (2 * SNAKE_SIZE, 2 * SNAKE_SIZE), (4 * SNAKE_SIZE, 2 * SNAKE_SIZE),
                      (3 * SNAKE_SIZE, 2 * SNAKE_SIZE), (2 * SNAKE_SIZE, 3 * SNAKE_SIZE),
                      (2 * SNAKE_SIZE, 4 * SNAKE_SIZE),
                      (width - 3 * SNAKE_SIZE, height - 3 * SNAKE_SIZE),
                      (width - 4 * SNAKE_SIZE, height - 3 * SNAKE_SIZE),
                      (width - 3 * SNAKE_SIZE, height - 4 * SNAKE_SIZE),
                      (3 * SNAKE_SIZE, width - 4 * SNAKE_SIZE), (4 * SNAKE_SIZE, width - 5 * SNAKE_SIZE),
                      (5 * SNAKE_SIZE, width - 6 * SNAKE_SIZE), (6 * SNAKE_SIZE, width - 7 * SNAKE_SIZE)]

        self.walls_front = [(width // 2, SNAKE_SIZE), (width // 2, 2 * SNAKE_SIZE), (width // 2, 3 * SNAKE_SIZE),
                            (width // 2, height - 2 * SNAKE_SIZE), (width // 2, height - 3 * SNAKE_SIZE),  (width // 2, height - 4 * SNAKE_SIZE),
                            (SNAKE_SIZE, height // 2), (2 * SNAKE_SIZE, height // 2), (3 * SNAKE_SIZE, height // 2),
                            (width - 2 * SNAKE_SIZE, height // 2 - SNAKE_SIZE), (width - 2 * SNAKE_SIZE, height // 2 - 2 * SNAKE_SIZE)]

        self.snake_dir = directions['right']

        self.food = None
        self.food_last_update = 1
        self.update_food()

    # reset environment
    def reset(self):
        self.game_closed = False  # Boolean to check if the game terminal is closed

        self.head = (self.width // 2, self.height // 2)
        self.snake_pixels = []
        self.snake_length = 0

        self.snake_dir = directions['right']

        self.food = None
        self.update_food()

        return self.get_state()

    # render game window
    def render(self, episode, e):
        self.game_display.blit(BG, (0, 0))
        pygame.draw.rect(self.game_display, GREY, [0, self.height, self.width, 40])

        # display the score
        text = score_font.render("Score:" + str(self.snake_length - 1), True, ORANGE)
        self.game_display.blit(text, [5, self.height + 10])
        max_score = score_font.render("Max Score:" + str(self.max_score), True, ORANGE)
        self.game_display.blit(max_score, [120, self.height + 10])
        if episode is not None:
            ep_text = score_font.render("Episode:" + str(episode), True, ORANGE)
            self.game_display.blit(ep_text, [280, self.height + 10])
            e_text = score_font.render("E:" + str(e), True, ORANGE)
            self.game_display.blit(e_text, [420, self.height + 10])

        # draw snake on the game window
        for pixel in self.snake_pixels:
            pygame.draw.rect(self.game_display, WHITE, [pixel[0], pixel[1], SNAKE_SIZE, SNAKE_SIZE])

        # draw food
        pygame.draw.rect(self.game_display, RED, [self.food[0], self.food[1], SNAKE_SIZE, SNAKE_SIZE])

        # draw walls
        if 'walls' in self.rules and "growth" in self.rules:
            for block in self.walls_front:
                pygame.draw.rect(self.game_display, BLACK, [block[0], block[1], SNAKE_SIZE, SNAKE_SIZE])
        elif 'walls' in self.rules:
            for block in self.walls:
                pygame.draw.rect(self.game_display, BLACK, [block[0], block[1], SNAKE_SIZE, SNAKE_SIZE])

        # to prevent the game window to freeze
        for event in pygame.event.get():
            # if the user quits the game, the game is over
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            # if user presses a key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_closed = True

        pygame.display.update()

    # get player move from keyboard
    def player_move(self):
        # while the snake is moving check the following conditions
        for event in pygame.event.get():
            # if the user quits the game, the game is over
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

            # if user presses a key
            if event.type == pygame.KEYDOWN:
                # if key is left
                if event.key == pygame.K_LEFT and self.snake_dir != directions['right']:
                    self.snake_dir = directions['left']
                # if key is right
                elif event.key == pygame.K_RIGHT and self.snake_dir != directions['left']:
                    self.snake_dir = directions['right']
                # if key is up
                elif event.key == pygame.K_UP and self.snake_dir != directions['down']:
                    self.snake_dir = directions['up']
                # if key is down
                elif event.key == pygame.K_DOWN and self.snake_dir != directions['up']:
                    self.snake_dir = directions['down']
                elif event.key == pygame.K_ESCAPE:
                    self.game_closed = True

        self.play_step()

    # play game step
    def play_step(self, action=None, episode=None, e=None):
        self.food_last_update += 1
        # print(self.food_last_update)
        reward = 0
        new_state = None

        # if agent provides action
        if action is not None:
            possible_dir = ['right', 'down', 'left', 'up']
            curr_dir = possible_dir.index(list(directions.keys())[list(directions.values()).index(self.snake_dir)])

            if numpy.array_equal(action, (1, 0, 0)):
                # no change snake goes straight
                new_dir = self.snake_dir
            elif numpy.array_equal(action, (0, 1, 0)):
                # turn right
                new_dir = directions[possible_dir[(curr_dir + 1) % 4]]
            else:
                # turn left
                new_dir = directions[possible_dir[(curr_dir - 1) % 4]]

            self.snake_dir = new_dir

        # update head position
        self.head = (self.head[0] + self.snake_dir[0], self.head[1] + self.snake_dir[1])

        if "borders" in self.rules:
            self.head = (self.head[0] % self.width, self.head[1] % self.height)

        self.snake_pixels.append(self.head)

        if len(self.snake_pixels) > self.snake_length:
            del self.snake_pixels[0]  # moving the snake head

        # if food was not eaten in 200 interactions, update location
        if self.food_last_update % 201 == 0:
            self.update_food()

        # if the snake hits the food move the food location
        if self.food == self.head:
            if 'growth' in self.rules:
                self.head = (self.head[0] + self.snake_dir[0], self.head[1] + self.snake_dir[1])
                self.snake_pixels.append(self.head)

                if "borders" in self.rules:
                    self.head = (self.head[0] % self.width, self.head[1] % self.height)

            self.update_food()
            reward += 50

        if self.check_collision():
            self.game_closed = True

        if self.game_closed:
            self.update_max_score(action)
            reward -= 50
            return new_state, reward, self.game_closed

        self.render(episode, e)
        clock.tick(self.snake_speed)

        new_state = self.get_state()

        return new_state, reward, self.game_closed

    # create new food coordinates
    def update_food(self):
        if self.food_last_update % 201 != 0:
            self.snake_length += 1  # increase the snake length

        self.food_last_update = 1

        x = round(random.randrange(0, self.width - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE  # x coordinate
        y = round(random.randrange(0, self.width - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE  # y coordinate
        self.food = (x, y)

        # check if new food coordinates are on the snake pixels
        if self.food in self.snake_pixels or self.food in self.walls:
            self.update_food()

        # if walls rules are active check if new food coordinates are on walls blocks
        if "growth" in self.rules and "walls" in self.rules and self.food in self.walls_front:
            self.update_food()
        elif "walls" in self.rules and self.food in self.walls:
            self.update_food()

    # detect collision with wall or body
    def check_collision(self, point=None):
        if point is None:
            point = self.head

        # if the snake hits the border walls close the game
        if "borders" not in self.rules and (
                point[0] > self.width - SNAKE_SIZE or point[0] < 0 or point[1] > self.height - SNAKE_SIZE or point[
            1] < 0):
            return True

        # if snake runs into itself
        for pixel in self.snake_pixels[:-1]:
            if pixel == point:
                return True

        # wall collision
        if "walls" in self.rules and "growth" in self.rules:
            if point in self.walls_front:
                return True
        elif "walls" in self.rules:
            if point in self.walls:
                return True

        return False

    # calculate distance from danger
    def check_danger(self, pt, pt_danger, x_axis=None, y_axis=None):

        while True:
            if (pt_danger[0] % self.width, pt_danger[1] % self.height) == self.head:
                # if the danger point is the head it means there are no dangers in that direction
                return SNAKE_SIZE * 100
            elif self.check_collision(pt_danger) or self.check_collision((pt_danger[0] % self.width, pt_danger[1] % self.height)):
                # if the first danger in the specific direction was found
                return int(sqrt((pt[0] - pt_danger[0]) ** 2 + (pt[1] - pt_danger[1]) ** 2))
            else:
                # if no danger was found, move one square in that direction
                if x_axis is False and y_axis is None:
                    pt_danger = (pt_danger[0] - SNAKE_SIZE, pt_danger[1])
                elif x_axis is None and y_axis is False:
                    pt_danger = (pt_danger[0], pt_danger[1] - SNAKE_SIZE)
                elif x_axis is True and y_axis is None:
                    pt_danger = (pt_danger[0] + SNAKE_SIZE, pt_danger[1])
                elif x_axis is None and y_axis is True:
                    pt_danger = (pt_danger[0], pt_danger[1] + SNAKE_SIZE)

    # get environment state
    def get_state(self):
        x = self.head[0]
        y = self.head[1]

        matrix = [
                [(x - SNAKE_SIZE, y - SNAKE_SIZE), (x, (y - SNAKE_SIZE) % self.height), (x + SNAKE_SIZE, y - SNAKE_SIZE)],
                [((x - SNAKE_SIZE) % self.width, y), (x, y), ((x + SNAKE_SIZE) % self.width, y)],
                [(x - SNAKE_SIZE, y + SNAKE_SIZE), (x, (y + SNAKE_SIZE) % self.height), (x + SNAKE_SIZE, y + SNAKE_SIZE)]
            ]

        # distance danger up, down, right, left
        d_dng_up = self.check_danger(matrix[0][1], matrix[0][1], y_axis=False) // SNAKE_SIZE
        d_dng_right = self.check_danger(matrix[1][2], matrix[1][2], x_axis=True) // SNAKE_SIZE
        d_dng_down = self.check_danger(matrix[2][1], matrix[2][1], y_axis=True) // SNAKE_SIZE
        d_dng_left = self.check_danger(matrix[1][0], matrix[1][0], x_axis=False) // SNAKE_SIZE

        # distance of snake's head from the food
        d_food = int(sqrt((self.food[0] - self.head[0]) ** 2 + (self.food[1] - self.head[1]) ** 2)) // 40

        # current direction
        left_dir = (self.snake_dir == directions['left'])
        right_dir = (self.snake_dir == directions['right'])
        up_dir = (self.snake_dir == directions['up'])
        down_dir = (self.snake_dir == directions['down'])

        state = [
            self.food[0] < self.head[0],    # food is left
            self.food[0] > self.head[0],    # food is right
            self.food[1] < self.head[1],    # food is up
            self.food[1] > self.head[1],    # food is down

            d_food,

            # current direction
            left_dir,
            right_dir,
            up_dir,
            down_dir,

            d_dng_up,
            d_dng_down,
            d_dng_right,
            d_dng_left,
        ]

        state = numpy.array(state, dtype=int)

        return tuple(state)

    # update max score
    def update_max_score(self, mode=None):
        key_board = '-'.join(self.rules)
        if (self.snake_length - 1) > min(self.scoreboard[key_board])[0]:
            if mode is not None:
                name = 'agent'
            else:
                name = 'player'

            self.scoreboard[key_board].append((self.snake_length - 1, name))

            self.scoreboard[key_board].sort(reverse=True)
            if len(self.scoreboard[key_board]) > 10:
                del(self.scoreboard[key_board][10])

        if (self.snake_length - 1) > self.max_score:
            self.max_score = self.snake_length - 1

    # load maximum score
    def load_max_score(self):
        key_board = '-'.join(self.rules)
        self.scoreboard[key_board].sort(reverse=True)

        self.max_score = self.scoreboard[key_board][0][0]

    # display the score
    def print_score(self, score):
        text = score_font.render("Score: " + str(score), True, ORANGE)
        max_score = score_font.render("Max Score: " + str(self.max_score), True, ORANGE)
        self.game_display.blit(text, [0, 0])
        self.game_display.blit(max_score, [200, 0])

    # change speed of the snake
    # LOW -> MED -> HIGH ->
    def set_speed(self):
        if self.snake_speed == MID:
            self.snake_speed = HIGH
        elif self.snake_speed == LOW:
            self.snake_speed = MID
        else:
            self.snake_speed = LOW

        # load scoreboard from pickle file

    def load_scoreboard(self):
        try:
            with open('scoreboard.pkl', 'rb') as pickled_scoreboard:
                self.scoreboard = pickle.load(pickled_scoreboard)
        except:
            self.scoreboard = defaultdict(def_value)

        # save current scoreboard to pickle file

    def save_scoreboard(self):
        with open('scoreboard.pkl', 'wb') as pickled_scoreboard:
            pickle.dump(self.scoreboard, pickled_scoreboard)
