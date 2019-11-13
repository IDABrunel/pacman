import copy
from agents.pacman import Pacman
from agents.pinky import Pinky


class Game:
    complete = False

    def __init__(self, board_state, pacman_location, pinky_location):
        self.state = board_state
        self.pacman = Pacman(self, pacman_location)
        self.pinky = Pinky(self, pinky_location)

    def handle_moves(self, pacman_move, pinkyMove):
        self.pacman.handle_move(pacman_move)

    def calculate_board(self):
        current_state = copy.deepcopy(self.state)
        current_state[self.pacman._location[1]][self.pacman._location[0]] = 9
        return current_state
