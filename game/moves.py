from random import randint


class Moves:
    @classmethod
    def fully_random(self):
        return ['U', 'D', 'L', 'R', ''][randint(0, 4)]

    @classmethod
    def valid_random(self, agent):
        possi_moves = ['U', 'D', 'L', 'R', '']
        valid_moves = []

        for move in possi_moves:
            if agent.is_valid_location(agent.calculate_move_location(move)):
                valid_moves.append(move)

        return valid_moves[randint(0, len(valid_moves) - 1)]


class UserInput:
    def __init__(self):
        pass

    def generate_move(self):
        return input("Direction U/D/L/R: ")


class ValidRandomWithMomentem:
    last_move = ''

    def generate_move(self, agent):
        if (
            (self.last_move != '') and agent.is_valid_location(
                agent.calculate_move_location(self.last_move)
            )
        ):
            return self.last_move

        self.last_move = Moves.valid_random(agent)

        return self.last_move
