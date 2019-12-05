class Inky:
    id = 5

    def __init__(self, game, spawnLocation):
        self._game = game
        self._spawn_location = spawnLocation
        self._last_location = spawnLocation
        self._current_location = spawnLocation
        self._is_ghost_mode = False

    def handle_move(self, move):
        proposed_location = self.calculate_move_location(move)

        if self.is_valid_location(proposed_location):
            self._last_location = proposed_location
            self._current_location = proposed_location

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
        return self._game.state[location[1]][location[0]] in [0, 8, 9]
