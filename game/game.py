import copy
import time

from agents.blinky import Blinky
from agents.pinky import Pinky
from agents.inky import Inky
from agents.clyde import Clyde
from agents.pacman import Pacman


class Game:
    complete = False

    def normalise_coordinates(self, location):
        x, y = location

        if x < 0:
            x = self.get_num_cols() + x
        elif x >= self.get_num_cols():
            x = x - self.get_num_cols()
        if y < 0:
            y = self.get_num_rows() + y
        elif y >= self.get_num_rows():
            y = y - self.get_num_rows()

        return [x, y]

    def get_num_rows(self):
        return len(self.state)

    def get_num_cols(self):
        return len(self.state[0])

    def __init__(
        self,
        board_state,
        pacman_current_location,
        blinky_current_location,
        pinky_current_location,
        inky_current_location,
        clyde_current_location
    ):
        self.state = board_state
        self.blinky = Blinky(self, blinky_current_location)
        self.pinky = Pinky(self, pinky_current_location)
        self.inky = Inky(self, inky_current_location)
        self.clyde = Clyde(self, clyde_current_location)
        self.pacman = Pacman(self, pacman_current_location)
        self.pacman_lives = 3

    def handle_moves(
        self,
        pacman_move,
        blinky_move,
        pinky_move,
        inky_move,
        clyde_move
    ):
        self.blinky.handle_move(blinky_move)
        self.pinky.handle_move(pinky_move)
        self.inky.handle_move(inky_move)
        self.clyde.handle_move(clyde_move)
        self.pacman.handle_move(pacman_move)

        nuggets_left = self.count_nuggets_left()
        print('Nuggets left', nuggets_left)

        if nuggets_left == 0:
            self.complete = True

        ghost_killing_nuggets_left = self.count_ghost_killing_nuggets_left()
        print('Ghost Killing Nuggets Remaining', ghost_killing_nuggets_left)
        print('blinky ghost status', self.blinky._is_ghost_mode)
        print('clyde ghost status', self.clyde._is_ghost_mode)
        print('inky ghost status', self.inky._is_ghost_mode)
        print('pinky ghost status', self.pinky._is_ghost_mode)

        ghost_last_location = [
            self.blinky._last_location,
            self.clyde._last_location,
            self.inky._last_location,
            self.pinky._last_location
        ]
        ghost_current_location = [
            self.blinky._current_location,
            self.clyde._current_location,
            self.inky._current_location,
            self.pinky._current_location
        ]

        if self.pacman._last_location in ghost_last_location:
            self.pacman_lives = self.pacman_lives - 1
            print('Lives left', self.pacman_lives)
            self.reset_agent_positions()

        if self.pacman._current_location in ghost_current_location:
            self.pacman_lives = self.pacman_lives - 1
            print('Lives left', self.pacman_lives)
            self.reset_agent_positions()

        if self.pacman_lives <= 0:
            self.complete = True

    def reset_agent_positions(self):
        self.blinky._current_location = self.blinky._spawn_location
        self.clyde._current_location = self.clyde._spawn_location
        self.inky._current_location = self.inky._spawn_location
        self.pinky._current_location = self.pinky._spawn_location
        self.pacman._current_location = self.pacman._spawn_location

    def count_nuggets_left(self):
        nuggets = 0

        for y in self.state:
            for x in y:
                if x == 8:
                    nuggets = nuggets + 1

        return nuggets

    def count_ghost_killing_nuggets_left(self):
        # reduce to 4 and remove 1 nugget from board when merging to master - only to speed up debug
        ghost_killing_nuggets = 5

        for y in self.state:
            for x in y:
                if x == 9:
                    self.enable_ghost_mode()
                    ghost_killing_nuggets = ghost_killing_nuggets - 1

        return ghost_killing_nuggets

    def enable_ghost_mode(self):
        t_end = time.time() + 0.1
        while time.time() < t_end:
            self.blinky._is_ghost_mode = True
            self.clyde._is_ghost_mode = True
            self.inky._is_ghost_mode = True
            self.pinky._is_ghost_mode = True

        self.blinky._is_ghost_mode = False
        self.clyde._is_ghost_mode = False
        self.inky._is_ghost_mode = False
        self.pinky._is_ghost_mode = False

    def calculate_board(self):
        current_state = copy.deepcopy(self.state)
        current_state[self.blinky._current_location[1]][self.blinky._current_location[0]] = self.blinky.id
        current_state[self.pinky._current_location[1]][self.pinky._current_location[0]] = self.pinky.id
        current_state[self.inky._current_location[1]][self.inky._current_location[0]] = self.inky.id
        current_state[self.clyde._current_location[1]][self.clyde._current_location[0]] = self.clyde.id
        current_state[self.pacman._current_location[1]][self.pacman._current_location[0]] = self.pacman.id

        return current_state
