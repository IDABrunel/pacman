import copy
from functools import reduce
from agents.blinky import Blinky
from agents.pinky import Pinky
from agents.inky import Inky
from agents.clyde import Clyde
from agents.pacman import Pacman


class Game:
    complete = False

    def __init__(self, board_state, pacman_location, blinky_location, pinky_location, inky_location, clyde_location):
        self.state = board_state
        self.blinky = Blinky(self, blinky_location)
        self.pinky = Pinky(self, pinky_location)
        self.inky = Inky(self, inky_location)
        self.clyde = Clyde(self, clyde_location)
        self.pacman = Pacman(self, pacman_location)

    def handle_moves(self, pacman_move, blinky_move, pinky_move, inky_move, clyde_move):
        self.blinky.handle_move(blinky_move)
        self.pinky.handle_move(pinky_move)
        self.inky.handle_move(inky_move)
        self.clyde.handle_move(clyde_move)
        self.pacman.handle_move(pacman_move)

        nuggets_left = self.count_nuggets_left()
        print('Nuggets left', nuggets_left)

        if nuggets_left == 0:
            self.complete = True

    def count_nuggets_left(self):
        nuggets = 0

        for y in self.state:
            for x in y:
                if x == 8: nuggets = nuggets + 1

        return nuggets

    def calculate_board(self):
        current_state = copy.deepcopy(self.state)
        current_state[self.blinky._location[1]][self.blinky._location[0]] = self.blinky.id
        current_state[self.pinky._location[1]][self.pinky._location[0]] = self.pinky.id
        current_state[self.inky._location[1]][self.inky._location[0]] = self.inky.id
        current_state[self.clyde._location[1]][self.clyde._location[0]] = self.clyde.id
        current_state[self.pacman._location[1]][self.pacman._location[0]] = self.pacman.id
        return current_state
