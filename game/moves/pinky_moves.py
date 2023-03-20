import random
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.breadth_first import BreadthFirstFinder
from .rand import ValidRandom


def bool_to_int(val):
    return 1 if val else 0


def map_list_bool_to_int(ls):
    return list(map(bool_to_int, ls))


class PinkyMoves:
    last_move = ''

    def generate_move(self, agent):
        if agent._game._is_ghost_mode:
            # Terrified Ghost Mode
            target_location = (1, 1)
        else:
            # Scatter or Chase Mode
            if agent._game._is_scatter_mode:
                # Scatter Mode
                target_location = agent.calculate_move_location(self.last_move)
                if not agent.is_valid_location(target_location):
                    target_location = agent._current_location
            else:
                # Chase Mode
                if agent._game._cooldown_tick <= 100:
                    target_location = agent.calculate_move_location(self.last_move)
                    if not agent.is_valid_location(target_location):
                        target_location = agent._current_location
                else:
                    pacman_location = agent._game.pacman._current_location
                    target_location = (pacman_location[0], pacman_location[1])

        move = self.get_next_move(agent, target_location)
        if move:
            self.last_move = move
        else:
            self.last_move = self.generate_random_move(agent)

        return self.last_move

    def get_target_location(self, agent, grid, pacman_location):
        direction_to_move = {
            "": (0, 0),
            "U": (0, 4),
            "D": (0, -4),
            "L": (-4, 0),
            "R": (4, 0)
        }

        move_direction = agent._game.pacman._move_direction
        move_offset = direction_to_move[move_direction]
        new_location = (pacman_location[0] + move_offset[0], pacman_location[1] + move_offset[1])

        if grid.walkable(new_location[0], new_location[1]):
            end = grid.node(new_location[0], new_location[1])
        else:
            end = random.choice(grid.neighbors(grid.node(pacman_location[0], pacman_location[1])))

        return end

    def get_next_move(self, agent, target_location):
        agent_location = agent._current_location
        matrix = list(map(map_list_bool_to_int, np.array(agent._game.state) != 1))
        grid = Grid(matrix=matrix)
        start = grid.node(agent_location[0], agent_location[1])
        end = self.get_target_location(agent, grid, target_location)
        finder = BreadthFirstFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        if len(path) > 1:
            target_next = path[1]
            move = ""
            if agent_location[0] < target_next[0]:
                move = "R"
            elif agent_location[0] > target_next[0]:
                move = "L"
            elif agent_location[1] < target_next[1]:
                move = "D"
            elif agent_location[1] > target_next[1]:
                move = "U"
            if move and not self.is_backtracking(agent, move) and agent.is_valid_location(agent.calculate_move_location(move)):
                return move
        return None

    def generate_random_move(self, agent):
        return ValidRandom().generate_move(agent)

    def is_backtracking(self, agent, move):
        if agent._move_direction == 'U' and move == 'D':
            return True
        elif agent._move_direction == 'D' and move == 'U':
            return True
        elif agent._move_direction == 'R' and move == 'L':
            return True
        elif agent._move_direction == 'L' and move == 'R':
            return True
        else:
            return False
