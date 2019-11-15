class ArduinoRGBMatrix:

    def __init__(self, init_state, width, height, row_reverse):
        self.current_state = init_state
        self.send_full()

    def send_pixel(self, location, pixel):
        pass

    def send_full(self):
        pass

    def calculate_diff(self, new_state):
        pixel_changes = []

        for y, row in enumerate(new_state):
            for x, pixel in enumerate(row):
                if pixel != self.current_state[y][x]:
                    pixel_changes.append([[x, y], pixel])
