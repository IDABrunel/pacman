class Pacman:
    id = 2
    nuggets_collected = 0

    def __init__(self, game, spawnLocation):
        self._game = game
        self._location = spawnLocation
        self._nuggets_collected = 0

    def handle_move(self, move):

        # print('Pacman\'s Current Location:', self._location)

        proposed_location = self.calculate_move_location(move)

        # print('Pacman\'s proposed location:', proposed_location)

        if self.is_valid_location(proposed_location):
            self._location = proposed_location

        if self._game.state[self._location[1]][self._location[0]] == 8:
            self._game.state[self._location[1]][self._location[0]] = 0
            self._nuggets_collected = self._nuggets_collected + 1

        # print('Pacman\'s New Location:', self._location)
        return self._location

    def calculate_move_location(self, move):
        if move == 'U':
            return [self._location[0], self._location[1] - 1]

        if move == 'D':
            return [self._location[0], self._location[1] + 1]

        if move == 'L':
            if [self._location[0] - 1, self._location[1]] == [0, 5]:
                # print('This is a teleport')
                return [self._location[0] + 58, self._location[1]]
            else:
                return [self._location[0] - 1, self._location[1]]

        if move == 'R':
            if [self._location[0] + 1, self._location[1]] == [60, 5]:
                # print('This is a teleport')
                return [self._location[0] - 59, self._location[1]]
            else:
                return [self._location[0] + 1, self._location[1]]

        if move == '':
            return self._location

        raise Exception('Invalid Move Identifier')

    def is_valid_location(self, location):
        return self._game.state[location[1]][location[0]] in [0, 8]
