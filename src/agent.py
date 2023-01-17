import numpy as np
import random
from collections import defaultdict
import pygame
import pickle


def def_value():
    return 0.0


class Agent:
    def __init__(self, game):
        self.q_table = defaultdict(def_value)
        self.actions = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]  # straight, right, left
        self.train_agent = False
        self.stop = False

        # set values
        self.learning_rate = 0.01
        self.discount_factor = 0.9

        self.n_episodes = 8000
        self.max_steps = 4000

        # exploration parameters
        self.epsilon = 1.0
        self.max_epsilon = 1.0
        self.min_epsilon = 0.01
        self.decay_rate = 0.0009

        self.env = game

    def max_q_value(self, st):
        q_values = {(1, 0, 0): self.q_table[(st, (1, 0, 0))], (0, 1, 0): self.q_table[(st, (0, 1, 0))], (0, 0, 1): self.q_table[(st, (0, 0, 1))]}

        return max(q_values, key=q_values.get)

    def save_table(self, name):
        # save q_table
        with open(name + 'table.pkl', 'wb') as pickled_table:
            pickle.dump(self.q_table, pickled_table)

    def load_table(self, name):
        # load q_table
        try:
            with open(name + 'table.pkl', 'rb') as pickled_table:
                self.q_table = pickle.load(pickled_table)
        except:
            self.q_table = defaultdict(def_value)

    def run_agent(self):
        # load q table
        self.load_table("-".join(self.env.rules))

        if self.train_agent:
            self.train()
            self.save_table("-".join(self.env.rules))
        else:
            while True:
                self.play()

                if self.stop:
                    break

    def train(self):
        self.stop = False

        # Q learning algorithm
        for episode in range(self.n_episodes):

            # interrupt training
            if self.stop:
                break

            # reset the environment
            state = self.env.reset()

            done = False
            step = 0

            for step in range(self.max_steps):
                # Policy implementation: get action to play considering exploration and exploitation tradeoff
                tradeoff = random.uniform(0, 1)

                if tradeoff > self.epsilon:
                    # exploitation
                    action = self.max_q_value(state)
                else:
                    # exploration (random action)
                    action = random.choice(self.actions)

                # get new state, reward and if the step is finished
                new_state, reward, done = self.env.play_step(action, episode, self.epsilon)

                # Bellman equation
                optimal_action = self.q_table[(new_state, self.max_q_value(new_state))]
                target_q = reward + self.discount_factor * optimal_action
                self.q_table[(state, action)] += self.learning_rate * (target_q - self.q_table[(state, action)])

                # update the state
                state = new_state

                # while the snake is moving check the following conditions
                for event in pygame.event.get():
                    # if the user quits the game, the game is over
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    # if user presses a key
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.stop = True
                            done = True

                if done is True:
                    break

            # reduce the exploration rate
            self.epsilon = self.min_epsilon + (self.max_epsilon - self.min_epsilon) * np.exp(-self.decay_rate * episode)

    def play(self):
        self.stop = False
        # reset the environment
        state = self.env.reset()

        # Q learning algorithm
        while True:

            action = self.max_q_value(state)

            # get new state, reward and if the episode is finished
            new_state, reward, done = self.env.play_step(action, 0, self.epsilon)

            # update the state
            state = new_state

            # while the snake is moving check the following conditions
            for event in pygame.event.get():
                # if the user quits the game, the game is over
                if event.type == pygame.QUIT:
                    pygame.quit()

                # if user presses a key
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.stop = True
                        done = True

            if done is True:
                break
