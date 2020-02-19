import sys
import argparse
from matplotlib import pyplot as plt
from game import Game
from arduino import ArduinoRGBMatrix
from results_display import generate_board_with_stats
from moves.rand import FullRandom, ValidRandom, ValidRandomWithMomentem
from moves.console import ConsoleInput
from moves.controller import Controler

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

_version_type = 0

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

blinky_move_factory = ValidRandomWithMomentem()
pinky_move_factory = ValidRandomWithMomentem()
inky_move_factory = ValidRandomWithMomentem()
clyde_move_factory = ValidRandomWithMomentem()

if args.strategy == 'full_random':
    _version_type = 1
    pacman_move_factory = FullRandom()
elif args.strategy == 'valid_random':
    _version_type = 2
    pacman_move_factory = ValidRandom()
elif args.strategy == 'valid_random_momentem':
    _version_type = 3
    pacman_move_factory = ValidRandomWithMomentem()
elif args.strategy == 'user_input':
    _version_type = 4
    pacman_move_factory = ConsoleInput()
elif args.strategy == 'controller':
    _version_type = 5
    pacman_move_factory = Controler()
else:
    raise 'Unknown movmement strategy.'


if args.arduino:
    arduino_matrix = ArduinoRGBMatrix(args.arduino_path)
    arduino_matrix.clear()
    arduino_matrix.update_by_n_random_pixels(
        generate_board_with_stats(board, _version_type, args.style),
        50
    )

if args.matplotlib:
    plt.ion()
    plt.clf()
    plt.imshow(generate_board_with_stats(board, _version_type, args.style))
    plt.axis('off')
    plt.show()
    plt.pause(0.05)

if args.images:
    plt.clf()
    plt.imshow(generate_board_with_stats(board, _version_type, args.style))
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
        arduino_matrix.update(generate_board_with_stats(board, _version_type, args.style))

    if args.matplotlib:
        plt.clf()
        plt.imshow(generate_board_with_stats(board, _version_type, args.style))
        plt.axis('off')
        plt.show()
        plt.pause(0.05)

    if args.images:
        plt.clf()
        plt.imshow(generate_board_with_stats(board, _version_type, args.style))
        plt.axis('off')
        plt.savefig('images/{:04d}.png'.format(board._current_tick), bbox_inches='tight')
