import json
import time
from pathlib import Path


class Logger:
    def __init__(
        self,
        game,
        output_dir=Path('./logs'),
        file_name=Path(str(round(time.time())) + '.log')
    ):
        self._game = game
        Path(output_dir).mkdir(exist_ok=True, parents=True)
        self.log_path = output_dir / file_name
        self.log_initial_state()

    def write(self, log_type, log):
        json.dump([log_type, log], open(self.log_path, 'a'))
        with open(self.log_path, 'a') as f:
            f.write('\n')

    def log_initial_state(self):
        self.write('initial', {
            "state": self._game.state,
            "blinky_location": self._game.blinky._current_location,
            "pinky_location": self._game.pinky._current_location,
            "inky_location": self._game.inky._current_location,
            "clyde_location": self._game.clyde._current_location,
            "pacman_location": self._game.pacman._current_location,
            "pacman_lives": self._game.pacman_lives
        })

    def log_move(self, pacman_move, blinky_move, pinky_move, inky_move, clyde_move):
        self.write('tick', {
            "state": self._game.state,
            "blinky_move": blinky_move,
            "blinky_location": self._game.blinky._current_location,
            "pinky_move": pinky_move,
            "pinky_location": self._game.pinky._current_location,
            "inky_move": inky_move,
            "inky_location": self._game.inky._current_location,
            "clyde_move": clyde_move,
            "clyde_location": self._game.clyde._current_location,
            "pacman_move": pacman_move,
            "pacman_location": self._game.pacman._current_location,
            "pacman_lives": self._game.pacman_lives
        })
