import time
import signal
import os
import sys
import argparse
from matplotlib import pyplot as plt
from game import Game
from arduino import ArduinoRGBMatrix
from results_display import generate_board_with_stats
from moves.blinky_moves import BlinkyMoves
from moves.pinky_moves import PinkyMoves
from moves.clyde_moves import ClydeMoves
from moves.inky_moves import InkyMoves

INIT_BOARD_STATE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 8, 1, 8, 1, 8, 1, 1, 1, 8, 1, 1, 1, 8, 1, 0, 1, 8, 1, 8, 0, 1, 0, 1, 1, 1, 0, 1, 0, 8, 0, 1, 1, 8, 1, 8, 1, 1, 0, 1, 1, 1, 0, 8, 1, 8, 1, 8, 1],
    [1, 8, 0, 9, 1, 8, 0, 8, 1, 8, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 7, 1, 0, 1, 1, 8, 1, 8, 1, 8, 0, 8, 1, 8, 0, 8, 1, 1, 0, 1, 0, 0, 0, 8, 0, 8, 1, 8, 0, 8, 0, 8, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 8, 0, 8, 1, 8, 1, 8, 1, 8, 1, 0, 1, 8, 1, 0, 1, 8, 1, 0, 1, 8, 1, 1, 0, 1, 0, 1, 0, 8, 0, 1, 0, 8, 0, 0, 0, 8, 1, 8, 1, 1, 0, 8, 0, 1, 0, 1, 0, 9, 1, 1, 1],
    [0, 8, 0, 8, 0, 8, 0, 8, 1, 1, 0, 8, 0, 8, 0, 8, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 8, 1, 8, 1, 1, 1, 8, 1, 8, 0, 8, 1, 1, 0, 8, 0, 8, 1, 8, 0, 8, 1, 8, 0, 8, 0, 8, 0, 8],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 8, 1, 1, 0, 1, 1, 8, 1, 1, 1, 8, 1, 1, 0, 8, 1, 0, 1, 8, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 8, 0, 1, 1, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 1, 8, 1, 1, 1],
    [1, 8, 0, 9, 1, 8, 0, 8, 0, 8, 0, 1, 1, 8, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 8, 1, 8, 0, 8, 1, 8, 0, 8, 0, 0, 0, 1, 0, 1, 1, 1, 1, 8, 1, 1, 0, 1, 0, 8, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 8, 0, 8, 0, 8, 0, 8, 1, 0, 1, 8, 1, 8, 1, 8, 1, 0, 1, 8, 1, 8, 1, 1, 0, 1, 0, 8, 0, 1, 0, 8, 0, 1, 1, 8, 1, 8, 0, 8, 0, 8, 0, 1, 0, 8, 0, 9, 0, 8, 1],
    [1, 8, 1, 8, 1, 8, 1, 8, 1, 8, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 8, 1, 8, 1, 1, 1, 8, 1, 1, 1, 8, 1, 1, 0, 1, 0, 1, 1, 1, 1, 8, 1, 8, 1, 1, 1, 1, 0, 1],
    [1, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 0, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

INIT_BLINKY_LOCATION = [26, 2]
INIT_PINKY_LOCATION = [26, 5]
INIT_INKY_LOCATION = [26, 6]
INIT_CLYDE_LOCATION = [26, 7]

INIT_PACMAN_LOCATION = [26, 10]

parser = argparse.ArgumentParser()
parser.add_argument('--style',
                    type=str,
                    default='default',
                    help='Style to use')
parser.add_argument('--matplotlib', action='store_true',
                    help='Enables matplotlib output')
parser.add_argument('--arduino', action='store_true',
                    help='Enables Arduino output')
parser.add_argument('--arduino_path',
                    type=str,
                    default='/dev/ttyACM0',
                    help='Arduino serial path')
parser.add_argument('--nooutput', action='store_true',
                    help='Enables nooutput')
parser.add_argument('--images', action='store_true',
                    help='Saves each figure to ./images/xxxx.png')
parser.add_argument('--logging', action='store_true',
                    help='Enables Logging')
parser.add_argument('--strategy',
                    type=str,
                    choices=['full_random', 'valid_random', 'valid_random_momentem', 'user_input', 'controller'],
                    default='valid_random_momentem',
                    help='Pacman move strategy')

if len(sys.argv[1:]) == 0:
    parser.print_help()
    parser.exit()

args = parser.parse_args()

board = Game(
    INIT_BOARD_STATE,
    INIT_PACMAN_LOCATION,
    INIT_BLINKY_LOCATION,
    INIT_PINKY_LOCATION,
    INIT_INKY_LOCATION,
    INIT_CLYDE_LOCATION,
    logging_enabled=args.logging
)

blinky_move_factory = BlinkyMoves()
pinky_move_factory = PinkyMoves()
inky_move_factory = InkyMoves()
clyde_move_factory = ClydeMoves()

if args.strategy == 'full_random':
    from moves.rand import FullRandom
    pacman_move_factory = FullRandom()
elif args.strategy == 'valid_random':
    from moves.rand import ValidRandom
    pacman_move_factory = ValidRandom()
elif args.strategy == 'valid_random_momentem':
    from moves.rand import ValidRandomWithMomentem
    pacman_move_factory = ValidRandomWithMomentem()
elif args.strategy == 'user_input':
    from moves.console import ConsoleInput
    pacman_move_factory = ConsoleInput()
elif args.strategy == 'controller':
    from moves.controller import Controler
    pacman_move_factory = Controler()
else:
    raise 'Unknown movmement strategy.'


if args.arduino:
    arduino_matrix = ArduinoRGBMatrix(args.arduino_path)
    arduino_matrix.clear()
    arduino_matrix.update_by_n_random_pixels(
        generate_board_with_stats(board, args.style),
        50
    )

if args.matplotlib:
    plt.ion()
    plt.clf()
    plt.imshow(generate_board_with_stats(board, args.style))
    plt.axis('off')
    plt.show()
    plt.pause(0.05)

if args.images:
    plt.clf()
    plt.imshow(generate_board_with_stats(board, args.style))
    plt.axis('off')
    plt.savefig('images/0000.png', bbox_inches='tight')

while board.complete is False:
    print('Tick...' + str(board._current_tick))
    board.handle_moves(
        pacman_move_factory.generate_move(board.pacman),
        blinky_move_factory.generate_move(board.blinky),
        pinky_move_factory.generate_move(board.pinky),
        inky_move_factory.generate_move(board.inky),
        clyde_move_factory.generate_move(board.clyde)
    )

    if args.arduino:
        arduino_matrix.update(generate_board_with_stats(board, args.style))

    if args.matplotlib:
        plt.clf()
        plt.imshow(generate_board_with_stats(board, args.style))
        plt.axis('off')
        plt.show()
        plt.pause(0.05)

    if args.images:
        plt.clf()
        plt.imshow(generate_board_with_stats(board, args.style))
        plt.axis('off')
        plt.savefig('images/{:04d}.png'.format(board._current_tick), bbox_inches='tight')

time.sleep(10)
os.kill(os.getpid(), signal.SIGKILL)
