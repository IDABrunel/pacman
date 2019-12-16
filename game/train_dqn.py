from baselines import deepq, logger
from rlenv import PacmanEnv

env = PacmanEnv()

logger.configure()

model = deepq.learn(
    env,
    "conv_only",
    convs=[(32, 8, 4), (64, 4, 2), (64, 3, 1)],
    hiddens=[256],
    dueling=True,
    lr=1e-4,
    total_timesteps=int(1e8),
    buffer_size=10000,
    exploration_fraction=0.1,
    exploration_final_eps=0.01,
    train_freq=4,
    learning_starts=10000,
    target_network_update_freq=1000,
    gamma=0.99
)

model.save('1e8.0.1.pkl')
