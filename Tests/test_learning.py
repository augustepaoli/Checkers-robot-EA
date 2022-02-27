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

boot=bootstrap_player(2)

#print(boot.theta)

#board=Board()
#print(boot.evaluate(board))
#boot.learning=True
#move=boot.minimax_search(board,3,True,3)
#print(boot.theta)
#for i in range(10) :
#    board.make_move(move[1])
#    board.print_board()
#    board.make_move(random_player().move(board))
#    board.print_board()
#    print(boot.evaluate(board))
#    print(boot.theta)
#    move=boot.minimax_search(board,3,True,3)
#    print(boot.theta)
#
#print(boot.theta)

#boot.save()
##boot.delete()
#print(boot.get_name())
#boot.save()
boot2 = bootstrap_player.load("bootstrap_player1645979635757")
print(boot2.theta)
print(Game(boot2,minimax_player(1)).end_game(ignore_history=False))