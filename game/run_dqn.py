from sys import argv
from baselines import deepq
import numpy as np
from results_display import generate_board_with_stats
from matplotlib import pyplot as plt
from rlenv import PacmanEnv


plt.ion()

env = PacmanEnv()
model = deepq.learn(
    env,
    "conv_only",
    convs=[(32, 8, 4), (64, 4, 2), (64, 3, 1)],
    hiddens=[256],
    dueling=True,
    total_timesteps=0,
    exploration_final_eps=0.01,
    load_path=argv[1]
)

obs, done = env.reset(), False
obs = np.array(obs)
episode_rew = 0

while not done:
    plt.clf()
    plt.imshow(generate_board_with_stats(env.board))
    plt.show()
    plt.pause(0.05)
    obs, rew, done, _ = env.step(model(obs)[0])
    episode_rew += rew
print("Episode reward", episode_rew)
