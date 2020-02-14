import importlib


def id_to_rgb(id, style='default'):
    return importlib.import_module('styles.' + style).STYLE[id]


def id_array_to_rgb_array(arr, style='default'):

    def id_to_rgb_with_style(arr):
        return id_to_rgb(arr, style)

    return list(map(id_to_rgb_with_style, arr))


def board_to_rgb(calculated_board, style='default'):

    def id_array_to_rgb_array_with_style(arr):
        return id_array_to_rgb_array(arr, style)

    return list(map(id_array_to_rgb_array_with_style, calculated_board))
