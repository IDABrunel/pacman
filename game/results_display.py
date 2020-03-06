from PIL import Image, ImageDraw
from rgb_mapper import board_to_rgb
import numpy as np
import importlib


def generate_board_with_stats(board, _version_type, style='default'):
    STYLE = importlib.import_module('styles.' + style).STYLE

    if STYLE['STATS_ENABLED']:
        board_m = board.calculate_board()
        board_rgb = np.array(board_to_rgb(board_m, style))
        stats_rgb = np.array(generate_stats(board, _version_type, style)) / STYLE['STATS_REDUCER']

        return np.vstack((board_rgb, stats_rgb)).astype(int)
    else:
        board_m = board.calculate_board()
        board_rgb = np.array(board_to_rgb(board_m, style))
        return board_rgb


def generate_stats(board, _version_type, style='default'):
    STYLE = importlib.import_module('styles.' + style).STYLE

    img = Image.new('RGBA', (60, 9), color=STYLE['STATS_BG'])
    heart = Image.open('./resources/heart.png')
    heart.thumbnail((60, 7))

    d = ImageDraw.Draw(img)

    d.text((30 - d.textsize(str(_version_type))[0], -1), str(_version_type), fill=STYLE['STATS_TEXT'])

    for h in range(0, board.pacman_lives):
        img.paste(heart, (h * 8, 1), mask=heart)

    d = ImageDraw.Draw(img)

    d.text((60 - d.textsize(str(board.calc_score()))[0], -1), str(board.calc_score()), fill=STYLE['STATS_TEXT'])

    return img.convert('RGB')
