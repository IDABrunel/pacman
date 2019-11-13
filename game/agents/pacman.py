class Pacman:
    id = 2
    nuggets_collected = 0

    def __init__(self, game, spawnLocation):
        self._game = game
        self._location = spawnLocation

    def handle_move(self, move):
        if move == 'U':
            self._location[1] = self._location[1] - 1
            return self._location

        if move == 'D':
            self._location[1] = self._location[1] + 1
            return self._location

        if move == 'L':
            self._location[0] = self._location[0] - 1
            return self._location

        if move == 'R':
            self._location[0] = self._location[0] + 1
            return self._location

        if move == '':
            return self._location

        raise Exception('Invalid Move Identifier')

    def is_valid_move(self):
        return False
