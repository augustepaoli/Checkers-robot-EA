from player import Player

import random as rd

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
