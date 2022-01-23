import sys
sys.path.insert(1, '/Users/auguste/Desktop/EA/code/Game')
from game import Game

sys.path.insert(1, '/Users/auguste/Desktop/EA/code/IA')
from random_player import random_player

p1=random_player()
p2=random_player()
game=Game(p1,p2)
print(game.end_game(verbose=False))