from random import randint


class FullRandom:
    def generate_move(self, _):
        return ['U', 'D', 'L', 'R', ''][randint(0, 4)]

class NoMovement:
    def generate_move(self, _):return ''

class ValidRandom:
    def generate_move(self, agent):
        possi_moves = ['U', 'D', 'L', 'R', '']
        valid_moves = []

        for move in possi_moves:
            if agent.is_valid_location(agent.calculate_move_location(move)):
                valid_moves.append(move)

        return valid_moves[randint(0, len(valid_moves) - 1)]


class ValidRandomWithMomentem:
    last_move = ''

    def generate_move(self, agent):
        if (
            (self.last_move != '') and agent.is_valid_location(
                agent.calculate_move_location(self.last_move)
            )
        ):
            return self.last_move
        else:
            self.last_move = ValidRandom().generate_move(agent)
            return self.last_move