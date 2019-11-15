import serial
import time

class ArduinoRGBMatrix:

    def __init__(self, init_state, width, height, row_reverse):
        self.width = width
        self.current_state = init_state
        # self.send_full()
        self.serial = serial.Serial('/dev/ttyACM0', 9600)
        time.sleep(3)


    def send_pixel(self, location, rgb):
        r, g, b = rgb
        print("{},{},{},{}".format(location, r, g, b))
        print(self.serial.write(bytes('{},{},{},{}\n'.format(location, r, g, b), 'ascii')))
        time.sleep(.05)

    def send_full(self, rgb_matrix):
        for (y, row) in enumerate(rgb_matrix):
            for (x, rgb) in enumerate(row):
                if (y % 2) == 1:
                    self.send_pixel((y * (self.width)) + self.width - x - 1, [rgb[0], rgb[1], rgb[2]])
                    # print('{},{},{},{}'.format((y * self.width) + self.width - x, rgb[0], rgb[1], rgb[2]))
                else:
                    self.send_pixel((y * self.width) + x, [rgb[0], rgb[1], rgb[2]])
                    # print('{},{},{},{}'.format((y * self.width) + x, rgb[0], rgb[1], rgb[2]))

    def send_update(self, rgb_matrix):
        updates = self.calculate_diff(rgb_matrix)
        print('UPDATES')
        for x in updates:
            print(x)

    def calculate_diff(self, new_state):
        pixel_changes = []

        for y, row in enumerate(new_state):
            for x, pixel in enumerate(row):
                if pixel != self.current_state[y][x]:
                    pixel_changes.append([[x, y], pixel])

        return pixel_changes


# a = ArduinoRGBMatrix([], 60, 20, False)
# import random
# for x in range(0, 60 * 6):
#     a.send_pixel(x, random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))

# a.send_pixel(0, 0,0,0)



# s = serial.Serial('/dev/ttyACM0', 9600, timeout=5)


# s.write(bytes("{},{},{},{}\n\n".format(location, r, g, b).encode('ascii')))
# # s.flush()
# # time.sleep(6) 