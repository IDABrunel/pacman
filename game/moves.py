from random import randint
from baselines import deepq
import numpy as np
import gym


class FullRandom:
    def generate_move(self, _):
        return ['U', 'D', 'L', 'R', ''][randint(0, 4)]


class ValidRandom:
    def generate_move(self, agent):
        possi_moves = ['U', 'D', 'L', 'R', '']
        valid_moves = []

        for move in possi_moves:
            if agent.is_valid_location(agent.calculate_move_location(move)):
                valid_moves.append(move)

        return valid_moves[randint(0, len(valid_moves) - 1)]


class ValidRandomWithMomentem:
    last_move = ''

    def generate_move(self, agent):
        if (
            (self.last_move != '') and agent.is_valid_location(
                agent.calculate_move_location(self.last_move)
            )
        ):
            return self.last_move

        self.last_move = ValidRandom().generate_move(agent)

        return self.last_move


class UserInput:
    def generate_move(self, _):
        return input("Direction U/D/L/R: ")


class FakePacmanEnv(gym.Env):

    def __init__(self, board):
        self.board = board
        self.observation_space = gym.spaces.Box(low=0, high=255, shape=(12, 60, 1), dtype=np.uint8)
        self.action_space = gym.spaces.Discrete(5)
        pass

    def render(self):
        return self.board.calculate_board()

    def step(self, action):
        return self.board.calculate_board(), 0, self.board.complete, {"ale.lives": self.board.pacman_lives}

    def reset(self):
        return np.array(self.board.calculate_board())


class DeepQ:

    def __init__(self, board, model_path):
        self.board = board
        self.model = deepq.learn(
            FakePacmanEnv(board),
            "conv_only",
            convs=[(32, 8, 4), (64, 4, 2), (64, 3, 1)],
            hiddens=[256],
            dueling=True,
            total_timesteps=0,
            exploration_final_eps=0.01,
            load_path=model_path
        )

    def generate_move(self, _):
        action = self.model(self.board.calculate_board())[0]
        return ['', 'R', 'L', 'U', 'D'][action]
