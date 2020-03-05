#!/usr/bin/env python3
import sys
from PIL import Image, ImageDraw
from arduino import ArduinoRGBMatrix
import numpy as np


class ScrollingText:
    def __init__(self, text, width, height):
        self.image_width = width
        self.image_height = height

        self.text = text

        self.text_width, self.text_height = self.calculate_text_dimentions()
        self.text_x = self.image_width

    def calculate_text_dimentions(self):
        img = Image.new('RGB', (self.image_width, self.image_height), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        return d.textsize(self.text)

    def generate(self):
        img = Image.new('RGB', (self.image_width, self.image_height), color=(0, 0, 0))
        d = ImageDraw.Draw(img)

        d.text((self.text_x, 0), self.text, fill=(100, 100, 0))

        self.text_x = self.text_x - 1

        if self.text_x <= - self.text_width:
            self.text_x = self.image_width

        return img


#st = ScrollingText(sys.argv[1], 60, 21)

#board = ArduinoRGBMatrix(serial_path='/dev/ttyACM0')

#while True:
#    board.update(np.array(st.generate()))
