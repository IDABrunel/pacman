import sys
import argparse
from matplotlib import pyplot as plt
from game import Game
from rgb_mapper import board_to_rgb
from arduino import ArduinoRGBMatrix
from moves import UserInput, ValidRandomWithMomentem

INIT_BOARD_STATE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1],
    [1, 8, 0, 8, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 8, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1],
    [1, 8, 0, 8, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 8, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 8, 1],
    [1, 8, 1, 8, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 0, 8, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

INIT_BLINKY_LOCATION = [26, 4]
INIT_PINKY_LOCATION = [26, 5]
INIT_INKY_LOCATION = [26, 6]
INIT_CLYDE_LOCATION = [26, 7]

INIT_PACMAN_LOCATION = [26, 10]


# print('Length of board', getNumCol())
# print('Width of board', getNumRow())
# print('Length of board', boardLength)
# print('Width of board', boardWidth)

board = Game(
    INIT_BOARD_STATE,
    INIT_PACMAN_LOCATION,
    INIT_BLINKY_LOCATION,
    INIT_PINKY_LOCATION,
    INIT_INKY_LOCATION,
    INIT_CLYDE_LOCATION
)


parser = argparse.ArgumentParser()
parser.add_argument('--matplotlib', action='store_true',
                    help='Enables matplotlib output')
parser.add_argument('--arduino', action='store_true',
                    help='Enables Arduino output')
parser.add_argument('--nooutput', action='store_true',
                    help='Enables nooutput')
parser.add_argument('--images', action='store_true',
                    help='Saves each figure to ./images/xxxx.png')

if len(sys.argv[1:]) == 0:
    parser.print_help()
    parser.exit()

args = parser.parse_args()

blinky_move_factory = ValidRandomWithMomentem()
pinky_move_factory = ValidRandomWithMomentem()
inky_move_factory = ValidRandomWithMomentem()
clyde_move_factory = ValidRandomWithMomentem()
pacman_move_factory = UserInput()

if args.arduino:
    arduino_matrix = ArduinoRGBMatrix()
    arduino_matrix.clear()
    arduino_matrix.update_by_n_random_pixels(board_to_rgb(board.calculate_board()), 50)

if args.matplotlib:
    plt.ion()
    plt.clf()
    plt.imshow(board_to_rgb(board.calculate_board()))
    plt.show()
    plt.pause(0.05)

if args.images:
    plt.clf()
    plt.imshow(board_to_rgb(board.calculate_board()))
    plt.savefig('images/0000.png')

i = 1
while board.complete is False:
    print('Tick...' + str(i))

    board.handle_moves(
        pacman_move_factory.generate_move(),
        blinky_move_factory.generate_move(board.blinky),
        pinky_move_factory.generate_move(board.pinky),
        inky_move_factory.generate_move(board.inky),
        clyde_move_factory.generate_move(board.clyde)
    )

    if args.arduino:
        arduino_matrix.update(board_to_rgb(board.calculate_board()))

    if args.matplotlib:
        plt.clf()
        plt.imshow(board_to_rgb(board.calculate_board()))
        plt.show()
        plt.pause(0.05)

    if args.images:
        plt.clf()
        plt.imshow(board_to_rgb(board.calculate_board()))
        plt.savefig('images/{:04d}.png'.format(i))

    i = i + 1
