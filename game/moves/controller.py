import struct
import array
from fcntl import ioctl
from threading import Thread

axis_names = {
    0x00: 'x',
    0x01: 'y'
}

button_names = {
    0x120: 'blue',
    0x121: 'red',
    0x122: 'yellow',
    0x123: 'green',

    0x124: 'left trigger',
    0x125: 'right trigger',

    0x128: 'select',
    0x129: 'start',
}


class Controler:

    def __init__(self):
        self.input_listener_thread = Thread(target=self.input_listener)
        self.input_listener_thread.start()

        self.direction = ''
        self.last_direction = ''

    def device_setup(self):
        self.axis_states = {}
        self.button_states = {}

        self.axis_map = []
        self.button_map = []

        # Open the joystick device.
        self.jsdev = open('/dev/input/js0', 'rb')

        # Get number of axes and buttons.
        buf = array.array('B', [0])
        ioctl(self.jsdev, 0x80016a11, buf)  # JSIOCGAXES
        num_axes = buf[0]

        buf = array.array('B', [0])
        ioctl(self.jsdev, 0x80016a12, buf)  # JSIOCGBUTTONS
        num_buttons = buf[0]

        # Get the axis map.
        buf = array.array('B', [0] * 0x40)
        ioctl(self.jsdev, 0x80406a32, buf)  # JSIOCGAXMAP

        for axis in buf[:num_axes]:
            axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
            self.axis_map.append(axis_name)
            self.axis_states[axis_name] = 0.0

        # Get the button map.
        buf = array.array('H', [0] * 200)
        ioctl(self.jsdev, 0x80406a34, buf)  # JSIOCGBTNMAP

        for btn in buf[:num_buttons]:
            btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
            self.button_map.append(btn_name)
            self.button_states[btn_name] = 0

        print('%d axes found: %s' % (num_axes, ', '.join(self.axis_map)))
        print('%d buttons found: %s' % (num_buttons, ', '.join(self.button_map)))

    def buf_to_direction(self, evbuf):
        _, value, type, number = struct.unpack('IhBB', evbuf)

        if type & 0x01:
            button = self.button_map[number]
            if button:
                self.button_states[button] = value

        if type & 0x02:
            axis = self.axis_map[number]
            if axis:
                fvalue = value / 32767.0
                self.axis_states[axis] = fvalue

                if (axis == 'y' and fvalue > 0):
                    self.direction = 'D'
                elif (axis == 'y' and fvalue < 0):
                    self.direction = 'U'
                elif axis == 'x' and fvalue < 0:
                    self.direction = 'L'
                elif axis == 'x' and fvalue > 0:
                    self.direction = 'R'

    def input_listener(self):
        self.device_setup()

        while True:
            evbuf = self.jsdev.read(8)
            if evbuf:
                self.buf_to_direction(evbuf)

    def generate_move(self, agent):

        if agent.is_valid_location(
            agent.calculate_move_location(self.direction)
        ):
            self.last_direction = self.direction
            return self.direction

        else:
            return self.last_direction
