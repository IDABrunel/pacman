from game import Game
from rgb_mapper import board_to_rgb
from moves import ValidRandomWithMomentem
import gym
from gym import spaces
import numpy as np

INIT_BOARD_STATE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 8, 1, 8, 1, 8, 1, 1, 1, 8, 1, 1, 1, 8, 1, 0, 1, 8, 1, 8, 0, 1, 0, 1, 1, 1, 0, 1, 0, 8, 0, 1, 1, 8, 1, 8, 1, 1, 0, 1, 1, 1, 0, 8, 1, 8, 1, 8, 1],
    [1, 8, 0, 8, 1, 8, 0, 8, 1, 8, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 8, 1, 8, 1, 8, 0, 8, 1, 8, 0, 8, 1, 1, 0, 1, 0, 0, 0, 8, 0, 8, 1, 8, 0, 8, 0, 8, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 8, 0, 8, 1, 8, 1, 8, 1, 8, 1, 0, 1, 8, 1, 0, 1, 8, 1, 0, 1, 8, 1, 1, 0, 1, 0, 1, 0, 8, 0, 1, 0, 8, 0, 0, 0, 8, 1, 8, 1, 1, 0, 8, 0, 1, 0, 1, 0, 8, 1, 1, 1],
    [0, 8, 0, 8, 0, 8, 0, 8, 1, 1, 0, 8, 0, 8, 0, 8, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 8, 1, 8, 1, 1, 1, 8, 1, 8, 0, 8, 1, 1, 0, 8, 0, 8, 1, 8, 0, 8, 1, 8, 0, 8, 0, 8, 0, 8],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 8, 1, 1, 0, 1, 1, 8, 1, 1, 1, 8, 1, 1, 0, 8, 1, 0, 1, 8, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 8, 0, 1, 1, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 1, 8, 1, 1, 1],
    [1, 8, 0, 8, 1, 8, 0, 8, 0, 8, 0, 1, 1, 8, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 8, 1, 8, 0, 8, 1, 8, 0, 8, 0, 0, 0, 1, 0, 1, 1, 1, 1, 8, 1, 1, 0, 1, 0, 8, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 8, 0, 8, 0, 8, 0, 8, 1, 0, 1, 8, 1, 8, 1, 8, 1, 0, 1, 8, 1, 8, 1, 1, 0, 1, 0, 8, 0, 1, 0, 8, 0, 1, 1, 8, 1, 8, 0, 8, 0, 8, 0, 1, 0, 8, 0, 8, 0, 8, 1],
    [1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 8, 1, 8, 1, 1, 1, 8, 1, 1, 1, 8, 1, 1, 0, 1, 0, 1, 1, 1, 1, 8, 1, 8, 1, 1, 1, 1, 0, 1],
    [1, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

INIT_BLINKY_LOCATION = [26, 4]
INIT_PINKY_LOCATION = [26, 5]
INIT_INKY_LOCATION = [26, 6]
INIT_CLYDE_LOCATION = [26, 7]

INIT_PACMAN_LOCATION = [26, 10]


class PacmanEnv(gym.Env):

    def __init__(self):
        self.observation_space = spaces.Box(low=0, high=255, shape=(12, 60, 1), dtype=np.uint8)
        self.action_space = spaces.Discrete(5)
        pass

    def render(self):
        return self.board.calculate_board()

    def step(self, action):
        self.board.handle_moves(
            ['', 'R', 'L', 'U', 'D'][action],
            self.blinky_move_factory.generate_move(self.board.blinky),
            self.pinky_move_factory.generate_move(self.board.pinky),
            self.inky_move_factory.generate_move(self.board.inky),
            self.clyde_move_factory.generate_move(self.board.clyde)
        )

        reward = (176 - self.board.count_nuggets_left()) - self.last_score
        self.last_score = 176 - self.board.count_nuggets_left()

        return self.board.calculate_board(), reward, self.board.complete, {"ale.lives": self.board.pacman_lives}

    def reset(self):
        self.board = Game(
            INIT_BOARD_STATE,
            INIT_PACMAN_LOCATION,
            INIT_BLINKY_LOCATION,
            INIT_PINKY_LOCATION,
            INIT_INKY_LOCATION,
            INIT_CLYDE_LOCATION
        )

        self.blinky_move_factory = ValidRandomWithMomentem()
        self.pinky_move_factory = ValidRandomWithMomentem()
        self.inky_move_factory = ValidRandomWithMomentem()
        self.clyde_move_factory = ValidRandomWithMomentem()

        self.last_score = 0

        return np.array(self.board.calculate_board())
