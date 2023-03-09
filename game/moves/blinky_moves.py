import math
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.dijkstra import AStarFinder
from .rand import ValidRandom, ValidRandomWithMomentem


def bool_to_int(val):
    return 1 if val else 0


def map_list_bool_to_int(ls):
    return list(map(bool_to_int, ls))


class BlinkyMoves:
    last_move = ''
    def generate_move(self, agent):
        agent_location = agent._current_location
        pacman_location = agent._game.pacman._current_location
        dist = math.sqrt(pow(agent_location[0] - pacman_location[0], 2) + pow(agent_location[1] - pacman_location[1], 2))
        
        if not agent._game._is_ghost_mode:
            if agent._game._cooldown_tick < 100:
                if (
                    (self.last_move != '') and agent.is_valid_location(
                        agent.calculate_move_location(self.last_move)
                    )
                ):
                    return self.last_move
    
                self.last_move = ValidRandom().generate_move(agent)

                return self.last_move
            elif agent._game._is_scatter_mode:
                if (
                    (self.last_move != '') and agent.is_valid_location(
                        agent.calculate_move_location(self.last_move)
                    )
                ):
                    return self.last_move
        
                self.last_move = ValidRandom().generate_move(agent)

                return self.last_move
            else:
                matrix = list(map(map_list_bool_to_int, np.array(agent._game.state) != 1))

                grid = Grid(matrix=matrix)

                start = grid.node(agent_location[0], agent_location[1])
                end = grid.node(pacman_location[0], pacman_location[1])
                
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
                path, runs = finder.find_path(start, end, grid)

                target_next = path[1]

                if agent_location[0] < target_next[0]:
                    move = 'R'
                elif agent_location[0] > target_next[0]:
                    move = 'L'
                if agent_location[1] < target_next[1]:
                    move = 'D'
                elif agent_location[1] > target_next[1]:
                    move = 'U'

                if agent.is_valid_location(agent.calculate_move_location(move)):
                    return move
                elif ((self.last_move != '') and agent.is_valid_location(
                    agent.calculate_move_location(self.last_move))
                ): 
                    return self.last_move
                self.last_move = ValidRandom().generate_move(agent)
                return self.last_move
        else:
            matrix = list(map(map_list_bool_to_int, np.array(agent._game.state) != 1))

            grid = Grid(matrix=matrix)
            start = grid.node(agent_location[0], agent_location[1])
            end = grid.node(58, 1)
            
            finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
            path, runs = finder.find_path(start, end, grid)
            
            if len(path) > 6:
                target_next = path[1]

                if agent_location[0] < target_next[0]:
                    move = 'R'
                elif agent_location[0] > target_next[0]:
                    move = 'L'
                if agent_location[1] < target_next[1]:
                    move = 'D'
                elif agent_location[1] > target_next[1]:
                    move = 'U'

                if agent.is_valid_location(agent.calculate_move_location(move)):
                    return move
                elif ((self.last_move != '') and agent.is_valid_location(
                    agent.calculate_move_location(self.last_move))
                ): 
                    return self.last_move
                self.last_move = ValidRandom().generate_move(agent)
                return self.last_move

            if (
                (self.last_move != '') and agent.is_valid_location(
                    agent.calculate_move_location(self.last_move)
                )
            ):
                return self.last_move
            self.last_move = ValidRandom().generate_move(agent)
            return self.last_move