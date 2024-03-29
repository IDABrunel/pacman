import copy
import random

from logger import Logger

from agents.blinky import Blinky
from agents.pinky import Pinky
from agents.inky import Inky
from agents.clyde import Clyde
from agents.pacman import Pacman


class Game:
    complete = False
    _is_scatter_mode = True
    _is_ghost_mode = False
    _num_time_blinky_caught = 0
    _num_time_clyde_caught = 0
    _num_time_inky_caught = 0
    _num_time_pinky_caught = 0
    _ghost_caught_at_tick = 0
    _current_tick = 0
    _cooldown_tick = 0
    _ghost_mode_total_duration_in_ticks = 60
    _ghost_mode_total_flickering_duration_in_ticks = 30

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
        clyde_current_location,
        logging_enabled=False
    ):
        self.state = board_state
        self.blinky = Blinky(self, blinky_current_location)
        self.pinky = Pinky(self, pinky_current_location)
        self.inky = Inky(self, inky_current_location)
        self.clyde = Clyde(self, clyde_current_location)
        self.pacman = Pacman(self, pacman_current_location)
        self.pacman_lives = 3
        self._initial_total_nuggets_on_board = self.count_nuggets_left()

        self.logging_enabled = logging_enabled
        if self.logging_enabled:
            self.logger = Logger(game=self)

    def handle_moves(
        self,
        pacman_move,
        blinky_move,
        pinky_move,
        inky_move,
        clyde_move
    ):
        self._current_tick = self._current_tick + 1
        self._cooldown_tick = self._cooldown_tick + 1
        counter = self._current_tick
        sub_counter = 0
        if counter % 28 < 7:
            self._is_scatter_mode = True
        elif counter % 28 < 27:
            if sub_counter % 20 == 0:
                self._is_scatter_mode = False
            sub_counter += 1
        else:
            sub_counter = 0

        self.blinky.handle_move(blinky_move)
        self.pinky.handle_move(pinky_move)
        self.inky.handle_move(inky_move)
        self.clyde.handle_move(clyde_move)
        self.pacman.handle_move(pacman_move)

        if self.logging_enabled:
            self.logger.log_move(pacman_move, blinky_move, pinky_move, inky_move, clyde_move)

        nuggets_left = self.count_nuggets_left()

        if nuggets_left == 0:
            self.complete = True

        self.check_if_ghost_has_been_through_gate()

        if self._is_ghost_mode:
            self.has_pacman_eaten_ghost()

            if self._current_tick == self._ghost_caught_at_tick + self._ghost_mode_total_duration_in_ticks:
                self.disable_ghost_mode()
                self.set_ghosts_to_default_id()
            else:
                self.visualise_active_ghost_mode_on_board()

        else:
            self.has_ghost_eaten_pacman()

    def reset_agent_positions(self):
        self.blinky._current_location = self.blinky._spawn_location
        self.clyde._current_location = self.clyde._spawn_location
        self.inky._current_location = self.inky._spawn_location
        self.pinky._current_location = self.pinky._spawn_location
        self.pacman._current_location = self.pacman._spawn_location

        self.blinky._been_through_gate = False
        self.clyde._been_through_gate = False
        self.inky._been_through_gate = False
        self.pinky._been_through_gate = False

    def count_nuggets_left(self):
        nuggets = 0

        for y in self.state:
            for x in y:
                if x == 8:
                    nuggets = nuggets + 1

        return nuggets

    def enable_ghost_mode(self):
        self._is_ghost_mode = True
        self._ghost_caught_at_tick = self._current_tick

    def disable_ghost_mode(self):
        self._is_ghost_mode = False

    def calc_score(self):
        nuggets_score = ((self._initial_total_nuggets_on_board - self.count_nuggets_left()) * 5)
        fruit_score = ((self.pacman._fruit_collected) * 100)
        caught_ghosts = ((self._num_time_blinky_caught * 40) + (self._num_time_clyde_caught * 40) + (self._num_time_inky_caught * 40) + (self._num_time_pinky_caught * 40))

        return nuggets_score + fruit_score + caught_ghosts

    def calculate_board(self):
        current_state = copy.deepcopy(self.state)

        current_state[self.pacman._current_location[1]][self.pacman._current_location[0]] = self.pacman.id

        agent_locations = [
            (self.blinky, tuple(self.blinky._current_location)),
            (self.pinky, tuple(self.pinky._current_location)),
            (self.inky, tuple(self.inky._current_location)),
            (self.clyde, tuple(self.clyde._current_location))
        ]

        coordinate_counts = {}
        for agent, location in agent_locations:
            if location in coordinate_counts:
                coordinate_counts[location].append(agent)
            else:
                coordinate_counts[location] = [agent]

        for location, agents in coordinate_counts.items():
            if len(agents) > 1:
                random.shuffle(agents)
                x, y = location
                current_state[y][x] = agents[0].id
            else:
                x, y = location
                current_state[y][x] = agents[0].id

        return current_state

    def change_all_ghost_id(self, new_id):
        self.blinky.id = new_id
        self.pinky.id = new_id
        self.inky.id = new_id
        self.clyde.id = new_id

    def set_ghosts_to_default_id(self):
        self.blinky.id = 3
        self.pinky.id = 4
        self.inky.id = 5
        self.clyde.id = 6

    def check_if_ghost_has_been_through_gate(self):
        if self.blinky._current_location == [26, 2]:
            self.blinky._been_through_gate = True
        elif self.clyde._current_location == [26, 2]:
            self.clyde._been_through_gate = True
        elif self.inky._current_location == [26, 2]:
            self.inky._been_through_gate = True
        elif self.pinky._current_location == [26, 2]:
            self.pinky._been_through_gate = True

    def has_ghost_eaten_pacman(self):
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

        if self.pacman._current_location in ghost_current_location or self.pacman._last_location in ghost_last_location:
            self.pacman_lives = self.pacman_lives - 1
            self._cooldown_tick = 0
            if self.pacman_lives <= 0:
                self.complete = True
            self.reset_agent_positions()
            self.disable_ghost_mode()

    def has_pacman_eaten_ghost(self):
        if self.pacman._current_location == self.blinky._current_location or self.pacman._last_location == self.blinky._last_location:
            self.blinky._current_location = self.blinky._spawn_location
            self.blinky._been_through_gate = False
            self._num_time_blinky_caught = self._num_time_blinky_caught + 1
        if self.pacman._current_location == self.clyde._current_location or self.pacman._last_location == self.clyde._last_location:
            self.clyde._current_location = self.clyde._spawn_location
            self.clyde._been_through_gate = False
            self._num_time_clyde_caught = self._num_time_clyde_caught + 1
        if self.pacman._current_location == self.inky._current_location or self.pacman._last_location == self.inky._last_location:
            self.inky._current_location = self.inky._spawn_location
            self.inky._been_through_gate = False
            self._num_time_inky_caught = self._num_time_inky_caught + 1
        if self.pacman._current_location == self.pinky._current_location or self.pacman._last_location == self.pinky._last_location:
            self.pinky._current_location = self.pinky._spawn_location
            self.pinky._been_through_gate = False
            self._num_time_pinky_caught = self._num_time_pinky_caught + 1

    def visualise_active_ghost_mode_on_board(self):
        if self._current_tick > self._ghost_caught_at_tick + self._ghost_mode_total_flickering_duration_in_ticks:
            if self._current_tick % 2 == 0:
                self.change_all_ghost_id(11)
            else:
                self.change_all_ghost_id(12)
        else:
            self.change_all_ghost_id(11)

    def get_current_tick(self, tick):
        return tick
