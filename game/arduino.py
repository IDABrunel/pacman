import serial
import time
from random import shuffle


def generate_empty_rgb_matrix(width, height):
    matrix = []
    for _ in range(0, height):
        row = []
        for _ in range(0, width):
            row.append([0, 0, 0])
        matrix.append(row)
    return matrix


class ArduinoRGBMatrix:

    def __init__(self):
        self.width = 60
        self.height = 21
        self.current_state = generate_empty_rgb_matrix(self.width, self.height)
        self.serial = serial.Serial('/dev/ttyACM0', 9600)
        time.sleep(1)

    ###
    # Low-level ops.
    ###

    def send_batch_ops(self, op_arrs):
        ops_str = ''

        for op_arr in op_arrs:
            op_str = ''

            for i in op_arr:
                op_str = op_str + str(i) + ','

            ops_str = ops_str + op_str + '\n'

        self.serial.write(bytes(ops_str, 'ascii'))

        for _ in op_arrs:
            self.serial.read_until(b'E')

    def send_op(self, op_arr):
        self.send_batch_ops([op_arr])

    def op_clear(self):
        return [0]

    def op_set(self, iloc, r, g, b):
        return [1, iloc, r, g, b]

    def op_show(self):
        return [2]

    def location_to_iloc(self, location):
        [x, y] = location

        if (y % 2) == 1:
            return (y * (self.width)) + self.width - x - 1
        else:
            return (y * self.width) + x

    ###
    # High Level Ops
    ###

    def clear(self):
        self.send_batch_ops([
            self.op_clear(),
            self.op_show()
        ])

    def set_pixel(self, location, rgb):
        r, g, b = rgb
        [x, y] = location

        self.send_batch_ops([
            self.op_set(self.location_to_iloc(location), r, g, b),
            self.op_show()
        ])

        self.current_state[y][x] = rgb

    def update_by_pixel(self, rgb_matrix):
        changes_from_current_state = self.calculate_diff(rgb_matrix)

        for [location, rgb] in changes_from_current_state:
            self.set_pixel(location, rgb)

    def update_by_n_random_pixels(self, rgb_matrix, n=1):
        changes_from_current_state = self.calculate_diff(rgb_matrix)
        shuffle(changes_from_current_state)

        while(len(changes_from_current_state) > 0):
            x = n if n < len(changes_from_current_state) else len(
                changes_from_current_state)
            ops = []

            for _ in range(0, x):
                [location, rgb] = changes_from_current_state.pop()
                x, y = location
                r, g, b = rgb
                self.current_state[y][x] = rgb
                ops.append(self.op_set(
                    self.location_to_iloc(location), r, g, b))

            ops.append(self.op_show())

            self.send_batch_ops(ops)

    def update(self, rgb_matrix):
        """
        Update the whole board in one batch.
        """
        changes_from_current_state = self.calculate_diff(rgb_matrix)

        ops = []

        for [location, rgb] in changes_from_current_state:
            [r, g, b] = rgb
            [x, y] = location

            self.current_state[y][x] = rgb
            ops.append(self.op_set(self.location_to_iloc(location), r, g, b))

        ops.append(self.op_show())

        self.send_batch_ops(ops)

    def calculate_diff(self, new_state):
        """
        Compared the current state with a proposed / new state and returns all
        the pixels that differ.

        Returns in the form of [ [[x, y], [r, g, b]], ... ]
        """
        pixel_changes = []

        for y, row in enumerate(new_state):
            for x, pixel in enumerate(row):
                if (
                    pixel[0] != self.current_state[y][x][0]
                    or pixel[1] != self.current_state[y][x][1]
                    or pixel[2] != self.current_state[y][x][2]
                ):
                    pixel_changes.append([[x, y], pixel])

        return pixel_changes
