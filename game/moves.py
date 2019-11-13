from random import randint


class Moves:
    @classmethod
    def fully_random(self):
        return ['U', 'D', 'L', 'R'][randint(0, 3)]
