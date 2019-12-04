#!/usr/bin/env python3

from PIL import Image
import numpy as np
import sys
from arduino import ArduinoRGBMatrix


board = ArduinoRGBMatrix()
board.clear()


def remove_transparency(im, bg_colour=(0, 0, 0)):
    alpha = im.convert('RGBA').split()[-1]
    bg = Image.new("RGB", im.size, bg_colour + (255,))
    bg.paste(im, mask=alpha)
    return bg


im = Image.open(sys.argv[1])

im = remove_transparency(im)

# Scale to max height / width
im.thumbnail((60, 21), Image.ANTIALIAS)


# Center in board

new_width = 60
new_height = 21

width, height = im.size

left = (width - new_width) / 2
top = (height - new_height) / 2
right = (width + new_width) / 2
bottom = (height + new_height) / 2

im = im.crop((left, top, right, bottom))

ar = np.array(im) / 10

board.update_by_n_random_pixels(ar, 50)
