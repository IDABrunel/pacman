import math
import random
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.breadth_first import BreadthFirstFinder
from .rand import ValidRandom, ValidRandomWithMomentem


def bool_to_int(val):
    return 1 if val else 0


def map_list_bool_to_int(ls):
    return list(map(bool_to_int, ls))


class InkyMoves:
    last_move = ''
    def generate_move(self, agent):

        if not agent._game._is_ghost_mode:
            if agent._game._is_scatter_mode:
                # Scatter Mode
                if (
                    (self.last_move != '') and agent.is_valid_location(
                        agent.calculate_move_location(self.last_move)
                    )
                ):
                    return self.last_move
                else:
                    self.last_move = ValidRandom().generate_move(agent)
                    return self.last_move
            else:
                if agent._game._cooldown_tick > 100:
                    # Chase Mode
                    agent_location = agent._current_location
                    pacman_location = agent._game.pacman._current_location
                    blinky_location = agent._game.blinky._current_location

                    dist = math.sqrt(pow(blinky_location[0] - pacman_location[0], 2) + pow(blinky_location[1] - pacman_location[1], 2))

                    matrix = list(map(map_list_bool_to_int, np.array(agent._game.state) != 1))

                    grid = Grid(matrix=matrix)
        
                    start = grid.node(agent_location[0], agent_location[1])
                    
                    if agent._game.pacman._move_direction == 'U':
                        if grid.walkable(pacman_location[0], pacman_location[1]+round(2+dist)):
                            end = grid.node(pacman_location[0], pacman_location[1]+round(2+dist))
                        else:
                            end = random.choice(grid.neighbors(grid.node(pacman_location[0], pacman_location[1])))
                    elif agent._game.pacman._move_direction == 'D':
                        if grid.walkable(pacman_location[0], pacman_location[1]-round(2+dist)):
                            end = grid.node(pacman_location[0], pacman_location[1]-round(2+dist))
                        else:
                            end = random.choice(grid.neighbors(grid.node(pacman_location[0], pacman_location[1])))
                    elif agent._game.pacman._move_direction == 'L':
                        if grid.walkable(pacman_location[0]-round(2+dist), pacman_location[1]):
                            end = grid.node(pacman_location[0]-round(2+dist), pacman_location[1])
                        else:
                            end = random.choice(grid.neighbors(grid.node(pacman_location[0], pacman_location[1])))
                    elif agent._game.pacman._move_direction == 'R':
                        if grid.walkable(pacman_location[0]+round(2+dist), pacman_location[1]):
                            end = grid.node(pacman_location[0]+round(2+dist), pacman_location[1])
                        else:
                            end = random.choice(grid.neighbors(grid.node(pacman_location[0], pacman_location[1])))
                    else:
                        end = grid.node(pacman_location[0], pacman_location[1])

                    finder = BreadthFirstFinder(diagonal_movement=DiagonalMovement.never)
                    path, runs = finder.find_path(start, end, grid)

                    # print(len(path))
                    if (len(path) > 1):
                        target_next = path[1]

                        if agent_location[0] < target_next[0]:
                            move = 'R'
                        elif agent_location[0] > target_next[0]:
                            move = 'L'
                        if agent_location[1] < target_next[1]:
                            move = 'D'
                        elif agent_location[1] > target_next[1]:
                            move = 'U'

                        if not self.is_backtracking(agent, move) and agent.is_valid_location(agent.calculate_move_location(move)):
                            self.last_move = move
                            return self.last_move
                        elif (
                            (self.last_move != '') and agent.is_valid_location(
                                agent.calculate_move_location(self.last_move)
                            )
                        ):
                            return self.last_move
                        else:
                            self.last_move = ValidRandom().generate_move(agent)
                            return self.last_move
                    elif (
                        (self.last_move != '') and agent.is_valid_location(
                            agent.calculate_move_location(self.last_move)
                        )
                    ):
                        return self.last_move
                    else:
                        self.last_move = ValidRandom().generate_move(agent)
                        return self.last_move
                elif (
                    (self.last_move != '') and agent.is_valid_location(
                        agent.calculate_move_location(self.last_move)
                    )
                ):
                    return self.last_move
                else:
                    self.last_move = ValidRandom().generate_move(agent)
                    return self.last_move
        else:
            # Terrified Ghost Mode
            agent_location = agent._current_location    

            matrix = list(map(map_list_bool_to_int, np.array(agent._game.state) != 1))

            grid = Grid(matrix=matrix)

            start = grid.node(agent_location[0], agent_location[1])
            end = grid.node(58, 10)
            
            finder = BreadthFirstFinder(diagonal_movement=DiagonalMovement.never)
            path, runs = finder.find_path(start, end, grid)
            # print(len(path))
            if (len(path) > 1):
                target_next = path[1]

                if agent_location[0] < target_next[0]:
                    move = 'R'
                elif agent_location[0] > target_next[0]:
                    move = 'L'
                if agent_location[1] < target_next[1]:
                    move = 'D'
                elif agent_location[1] > target_next[1]:
                    move = 'U'

                if not self.is_backtracking(agent, move) and agent.is_valid_location(agent.calculate_move_location(move)):
                    self.last_move = move
                    return self.last_move
                elif (
                    (self.last_move != '') and agent.is_valid_location(
                        agent.calculate_move_location(self.last_move)
                    )
                ):
                    return self.last_move
                else:
                    self.last_move = ValidRandom().generate_move(agent)
                    return self.last_move
            elif (
                (self.last_move != '') and agent.is_valid_location(
                    agent.calculate_move_location(self.last_move)
                )
            ):
                return self.last_move
            else:
                self.last_move = ValidRandom().generate_move(agent)
                return self.last_move

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
