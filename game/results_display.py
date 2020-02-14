from PIL import Image, ImageDraw
from rgb_mapper import board_to_rgb
import numpy as np


def generate_board_with_stats(board, _version_type):
    board_m = board.calculate_board()
    board_rgb = np.array(board_to_rgb(board_m))
    stats_rgb = np.array(generate_stats(board, _version_type)) / 5

    return np.vstack((board_rgb, stats_rgb)).astype(int)


def generate_stats(board, _version_type):
    img = Image.new('RGB', (60, 9), color=(0, 0, 0))
    heart = Image.open('./resources/heart.png')
    heart.thumbnail((60, 7), Image.ANTIALIAS)

    d = ImageDraw.Draw(img)

    d.text((30 - d.textsize(str(_version_type))[0], -1), str(_version_type), fill=(255, 255, 255))

    for h in range(0, board.pacman_lives):
        img.paste(heart, (h * 8, 1))

    d.text((60 - d.textsize(str(board.calc_score()))[0], -1), str(board.calc_score()), fill=(100, 100, 0))

    return img
