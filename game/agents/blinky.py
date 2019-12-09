class Blinky:
    id = 3

    def __init__(self, game, spawnLocation):
        self._game = game
        self._spawn_location = spawnLocation
        self._last_location = spawnLocation
        self._current_location = spawnLocation
        self._been_through_gate = False
        self._has_spawned_fruit = False

    def handle_move(self, move):
        proposed_location = self.calculate_move_location(move)

        if self.is_valid_location(proposed_location):
            self._last_location = proposed_location
            self._current_location = proposed_location

        if not self._has_spawned_fruit and not self._game._is_ghost_mode:
            if self._game.state[self._current_location[1]][self._current_location[0]] == 0 and self._game.count_nuggets_left() == 165:
                self._game.state[self._current_location[1]][self._current_location[0]] = 10
                self._has_spawned_fruit = True

        return self._current_location

    def calculate_move_location(self, move):
        if move == 'U':
            return self._game.normalise_coordinates(
                [self._current_location[0], self._current_location[1] - 1])
        elif move == 'D':
            return self._game.normalise_coordinates(
                [self._current_location[0], self._current_location[1] + 1])
        elif move == 'L':
            return self._game.normalise_coordinates(
                [self._current_location[0] - 1, self._current_location[1]])
        elif move == 'R':
            return self._game.normalise_coordinates(
                [self._current_location[0] + 1, self._current_location[1]])
        elif move == '':
            return self._current_location

        raise Exception('Invalid Move Identifier')

    def is_valid_location(self, location):
        location = self._game.normalise_coordinates(location)
        if self._been_through_gate:
            return self._game.state[location[1]][location[0]] in [0, 8, 9, 10]
        return self._game.state[location[1]][location[0]] in [0, 7, 8, 9, 10]
