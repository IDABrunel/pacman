import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def bool_to_int(val):
    return 1 if val == True else 0

def map_list_bool_to_int(ls):
    return list(map(bool_to_int, ls))

class SmartGhost:
    def generate_move(self, agent):
        matrix = list(map(map_list_bool_to_int, np.array(agent._game.state) != 1))

        grid = Grid(matrix=matrix)

        agent_location = agent._current_location
        pacman_location = agent._game.pacman._current_location

        start = grid.node(agent_location[0], agent_location[1])
        end = grid.node(pacman_location[0],pacman_location[1])

        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        
        target_next = path[1]

        if agent_location[0] < target_next[0]:
            return 'R'
        elif agent_location[0] > target_next[0]:
            return 'L'
        if agent_location[1] < target_next[1]:
            return 'D'
        elif agent_location[1] > target_next[1]:
            return 'U'