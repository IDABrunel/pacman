RGB_MAPPINGS = {
    0: [0, 0, 0],  # space
    1: [0, 0, 100],  # wall
    2: [255, 193, 7],  # pacman
    3: [244, 67, 54],  # blinky
    4: [233, 30, 99],  # pinky
    5: [0, 188, 212],  # inky
    6: [255, 87, 34],  # clyde
    7: [250, 250, 250],  # title
    8: [150, 150, 0],  # nuggets
    9: [255, 255, 255],
    10: [255, 193, 7],
    11: [0, 188, 212]
}


def id_to_rgb(id):
    return RGB_MAPPINGS[id]


def id_array_to_rgb_array(arr):
    return list(map(id_to_rgb, arr))


def board_to_rgb(calculated_board):
    return list(map(id_array_to_rgb_array, calculated_board))
