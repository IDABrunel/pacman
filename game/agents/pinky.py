class Pinky:
    id = 3

    def __init__(self, game, spawnLocation):
        self._game = game

    def is_valid_move(self):
        return False