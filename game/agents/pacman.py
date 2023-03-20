class Pacman:
    id = 2
    nuggets_collected = 0

    def __init__(self, game, spawnLocation):
        self._game = game
        self._spawn_location = spawnLocation
        self._last_location = spawnLocation
        self._current_location = spawnLocation
        self._nuggets_collected = 0
        self._fruit_collected = 0
        self._ghost_killing_nuggets_collected = 0
        self._move_direction = ''

    def handle_move(self, move):
        proposed_location = self.calculate_move_location(move)

        if self.is_valid_location(proposed_location):
            self._last_location = self._current_location
            self._current_location = proposed_location

        if self._game.state[
                self._current_location[1]][self._current_location[0]] == 9:
            self._game.state[
                self._current_location[1]][self._current_location[0]] = 0
            self._ghost_killing_nuggets_collected = self._ghost_killing_nuggets_collected + 1
            self._game.enable_ghost_mode()

        if self._game.state[
                self._current_location[1]][self._current_location[0]] == 8:
            self._game.state[
                self._current_location[1]][self._current_location[0]] = 0
            self._nuggets_collected = self._nuggets_collected + 1

        if self._game.state[
                self._current_location[1]][self._current_location[0]] == 10:
            self._game.state[
                self._current_location[1]][self._current_location[0]] = 0
            self._fruit_collected = self._fruit_collected + 1

        return self._current_location

    def calculate_move_location(self, move):
        if move == 'U':
            self._move_direction = 'U'
            return self._game.normalise_coordinates(
                [self._current_location[0], self._current_location[1] - 1])
        elif move == 'D':
            self._move_direction = 'D'
            return self._game.normalise_coordinates(
                [self._current_location[0], self._current_location[1] + 1])
        elif move == 'L':
            self._move_direction = 'L'
            return self._game.normalise_coordinates(
                [self._current_location[0] - 1, self._current_location[1]])
        elif move == 'R':
            self._move_direction = 'R'
            return self._game.normalise_coordinates(
                [self._current_location[0] + 1, self._current_location[1]])
        elif move == '':
            self._move_direction = ''
            return self._current_location

        raise Exception('Invalid Move Identifier')

    def is_valid_location(self, location):
        location = self._game.normalise_coordinates(location)
        return self._game.state[location[1]][location[0]] in [0, 8, 9, 10]
