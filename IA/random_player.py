import random as rd

import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from IA.player import Player

class random_player(Player) :
    
    def __init__(self) :
        self.name="Random player"
        self.number_games=0
    
    def get_name(self) :
        return self.name
    
    def move(self,board,ignore_history=True) :
        moves = board.get_possible_next_moves()
        move = moves[rd.randint(0,len(moves)-1)]
        return move
    
    def get_numbergames(self) :
        return self.number_games
