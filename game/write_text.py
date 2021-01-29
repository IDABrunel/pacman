#!/usr/bin/env python3
import sys
from PIL import Image, ImageDraw, ImageFont
from arduino import ArduinoRGBMatrix
import numpy as np

font = ImageFont.truetype('/usr/share/fonts/truetype/ttf-bitstream-vera/Vera.ttf', 9)


class TextWriter:
    def __init__(self, text, width, height):
        self.image_width = width
        self.image_height = height

        self.text = text

        self.text_width, self.text_height = self.calculate_text_dimentions()
        self.text_x = self.image_width

    def calculate_text_dimentions(self):
        img = Image.new('RGB', (self.image_width, self.image_height), color=(73, 109, 137))
        d = ImageDraw.Draw(img)
        return d.textsize(self.text, font)

    def generate(self):
        img = Image.new('RGB', (self.image_width, self.image_height), color=(0, 0, 0))
        d = ImageDraw.Draw(img)

        d.text(((self.image_width - self.text_width) / 2, 4), self.text, fill=(100, 100, 0), font=font)

        self.text_x = self.text_x - 1

        if self.text_x <= - self.text_width:
            self.text_x = self.image_width

        return img


if __name__ == '__main__':

    st = TextWriter(sys.argv[1], 60, 21)

    board = ArduinoRGBMatrix()

    board.update(np.array(st.generate()))
