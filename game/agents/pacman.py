class Pacman:
    id = 2
    nuggets_collected = 0

    def __init__(self, game, spawnLocation):
        self._game = game
        self._location = spawnLocation
        self._nuggets_collected = 0

    def handle_move(self, move):
        proposed_location = self.calculate_move_location(move)

        if self.is_valid_location(proposed_location):
            self._location = proposed_location

        if self._game.state[self._location[1]][self._location[0]] == 8:
            self._game.state[self._location[1]][self._location[0]] = 0
            self._nuggets_collected = self._nuggets_collected + 1

        return self._location

    def calculate_move_location(self, move):
        if move == 'U':
            return [self._location[0], self._location[1] - 1]

        if move == 'D':
            return [self._location[0], self._location[1] + 1]

        if move == 'L':
            return [self._location[0] - 1, self._location[1]]

        if move == 'R':
            return [self._location[0] + 1, self._location[1]]

        if move == '':
            return self._location

        raise Exception('Invalid Move Identifier')

    def is_valid_location(self, location):
        return self._game.state[location[1]][location[0]] in [0, 8]
