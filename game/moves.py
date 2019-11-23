from random import randint, random


def calculate_valid_moves(agent):
    possi_moves = ['U', 'D', 'L', 'R', '']
    valid_moves = []

    for move in possi_moves:
        if agent.is_valid_location(agent.calculate_move_location(move)):
            valid_moves.append(move)

    return valid_moves

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


class QLearning:
    def __init__(self, game, learning_rate=.2, exploration_rate=.4, discount_factor=.8, num_training=10):
        self.game = game
        self.lr = learning_rate
        self.er = exploration_rate
        self.df = discount_factor
        self.num_training = num_training

        self.q_table = {}

        self.last_states = []
        self.last_actions = []

        self.primative = ValidRandomWithMomentem()

        self.score = 0

    def get_q_value(self, state, action):
        if tuple((str(state), action)) in self.q_table:
            return self.q_table[tuple((str(state), action))]
        else:
            return 0

    def set_q_value(self, state, action, value):
        self.q_table[(str(state), action)] = value

    def max_q(self, state, valid_actions):
        q_list = []
        for action in valid_actions:
            q = self.get_q_value(state, action)
            q_list.append(q)
        if len(q_list) ==0:
            return 0
        return max(q_list)

    def update_q(self, state, action, reward, max_q):
        q = self.get_q_value(state,action)
        self.set_q_value(state, action, q + self.lr * (reward + self.df * max_q - q))


    def generate_move(self, agent):
        valid_moves = calculate_valid_moves(agent)

        if len(self.last_states) > 0:
            last_state = self.last_states[-1]
            last_action = self.last_actions[-1]
            reward = agent._nuggets_collected - self.score

            self.q_table[(str(last_state), last_action)] = reward


        if random() < self.er:
            valid_move = Moves.valid_random(agent)
        else:
            valid_move_q_values = []

            for valid_move in valid_moves:
                valid_move_q_values.append(self.get_q_value(self.game.calculate_board(), valid_move))

            if max(valid_move_q_values) == 0:
                valid_move = self.primative.generate_move(agent)
            else:
                valid_move = valid_moves[valid_move_q_values.index(max(valid_move_q_values))]


            
        print(valid_move)
        self.last_states.append(self.game.calculate_board())
        self.last_actions.append(valid_move)

        return valid_move
        
        # self.score = self.nuggets_collected