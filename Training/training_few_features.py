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

boot = bootstrap_player(4)
boot.step=1.0
boot.name="trained"
boot.counting_error=True

p2=minimax_player(2)

for i in range(100) :
    game=Game(boot,p2)
    game.end_game(ignore_history=False)
    print(boot.theta)
    print(boot.total_square_error)

boot.save()
boot.total_square_error=0

p2=minimax_player(3)

for i in range(100) :
    game=Game(boot,p2)
    game.end_game(ignore_history=False)
    print(boot.theta)
    print(boot.total_square_error)

boot.save()
boot.total_square_error=0

p2=minimax_player(4)

for i in range(100) :
    game=Game(boot,p2)
    game.end_game(ignore_history=False)
    print(boot.theta)
    print(boot.total_square_error)

boot.save()
boot.total_square_error=0

p2=minimax_player(5)

for i in range(100) :
    game=Game(boot,p2)
    game.end_game(ignore_history=False)
    print(boot.theta)
    print(boot.total_square_error)




