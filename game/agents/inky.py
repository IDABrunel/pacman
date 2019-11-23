class Inky:
    id = 5

    def __init__(self, game, spawnLocation):
        self._game = game
        self._location = spawnLocation

    def handle_move(self, move):
        proposed_location = self.calculate_move_location(move)

        if self.is_valid_location(proposed_location):
            self._location = proposed_location

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
