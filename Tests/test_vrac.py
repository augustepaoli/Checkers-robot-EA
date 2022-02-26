import pickle



import os

PROJECT_ROOT2 = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir,"Game"))

print(PROJECT_ROOT2)

import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

print(PROJECT_ROOT)

from Game.game import Game
from IA.random_player import random_player
from IA.minimax_player import minimax_player


mini = minimax_player(2)
file=open("minimax_2.obj","wb")
pickle.dump(mini,file)
file.close()


file2=open('minimax_2.obj','rb')
mini=pickle.load(file2)
game=Game(mini,random_player())
print(game.end_game())