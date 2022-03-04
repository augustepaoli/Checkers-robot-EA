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

boot = bootstrap_player(1,features=["number_pawns_p1","number_pawns_p2","number_kings_p1","number_kings_p2"])
boot.step=1
boot.name="trained_few_features"
boot.counting_error=True

errors = []

p2=random_player()

for i in range(200) :
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
boot.default_depth=2

p2=minimax_player(1)

for i in range(200) :
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
boot.default_depth=3

p2=minimax_player(2)

for i in range(200) :
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

boot.save()
boot.total_square_error=0
boot.number_scores_counted=0
p2=minimax_player(4)

for i in range(100) :
    boot.number_scores_counted=0
    boot.total_square_error=0
    print(i)
    game=Game(boot,p2)
    game.end_game()
    print(boot.theta)
    print(boot.total_square_error)
    errors.append(boot.total_square_error)

plt.plot(np.arange(len(errors)),errors)
plt.xlabel("Number of games played")
plt.ylabel("mean squared error")
plt.title("Evolution of the error while learning")
plt.legend()
plt.show()


