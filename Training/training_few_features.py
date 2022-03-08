import matplotlib.pyplot as plt
import numpy as np

import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from Game_Interface.board import Board
from Game.game import Game
from IA.random_player import random_player
from IA.minimax_player import minimax_player
from IA.bootstrap_player import bootstrap_player

boot=bootstrap_player.load("trained_full_features")
boot.counting_error=True
boot.default_depth=4
sys.setrecursionlimit(10000)
boot.name="trained_full_features_with_depth_4"

errors = []

p2=random_player()

for i in range(2000) :
    boot.number_scores_counted=0
    boot.total_square_error=0
    print(i)
    game=Game(boot,p2)
    game.end_game()
    print(boot.theta)
    print(boot.total_square_error)
    errors.append(boot.total_square_error)

boot.save()
boot.total_square_error=0
boot.number_scores_counted=0

p2=minimax_player(1)

for i in range(1000) :
    boot.number_scores_counted=0
    boot.total_square_error=0
    print(i)
    game=Game(boot,p2)
    game.end_game()
    print(boot.theta)
    print(boot.total_square_error)
    errors.append(boot.total_square_error)

boot.save()
boot.total_square_error=0
boot.number_scores_counted=0

p2=minimax_player(2)

for i in range(500) :
    boot.number_scores_counted=0
    boot.total_square_error=0
    print(i)
    game=Game(boot,p2)
    game.end_game()
    print(boot.theta)
    print(boot.total_square_error)
    errors.append(boot.total_square_error)

boot.save()
boot.total_square_error=0
boot.number_scores_counted=0
p2=minimax_player(3)

for i in range(100) :
    boot.number_scores_counted=0
    boot.total_square_error=0
    print(i)
    game=Game(boot,p2)
    game.end_game()
    print(boot.theta)
    print(boot.total_square_error)
    errors.append(boot.total_square_error)

boot.default_depth=3
boot.save()
boot.total_square_error=0
boot.number_scores_counted=0

plt.plot(np.arange(len(errors)),errors)
plt.xlabel("Number of games played")
plt.ylabel("mean squared error")
plt.title("Evolution of the error while learning")
plt.legend()
plt.show()

