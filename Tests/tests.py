import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from Game.game import Game
from IA.random_player import random_player
from IA.minimax_player import minimax_player

print("Pre test : ")
p1=random_player()
p2=random_player()
game=Game(p1,p2)
print(game.end_game(verbose=False))
print("")

print("test : number of wins of a minimax player with depth 2 against random player, out of 100 games :")
p1=random_player()
p2=minimax_player(2)
count=0
for i in range(100) :
    game=Game(p1,p2)
    if game.end_game()==2 :
        count+=1
print(count)