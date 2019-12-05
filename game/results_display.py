from PIL import Image, ImageDraw
from rgb_mapper import board_to_rgb
import numpy as np


def generate_board_with_stats(board):
    board_m = board.calculate_board()
    board_rgb = np.array(board_to_rgb(board_m))
    stats_rgb = np.array(generate_stats(board)) / 5

    return np.vstack((board_rgb, stats_rgb)).astype(int)


def generate_stats(board):
    img = Image.new('RGB', (60, 9), color=(0, 0, 0))
    heart = Image.open('./resources/heart.png')
    heart.thumbnail((60, 7), Image.ANTIALIAS)

    for h in range(0, board.pacman_lives):
        img.paste(heart, (h * 8, 1))

    d = ImageDraw.Draw(img)

    score = (176 - board.count_nuggets_left())

    d.text((60 - d.textsize(str(score))[0], -1), str(score), fill=(100, 100, 0))

    return img
