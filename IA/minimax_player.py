import random as rd

import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from IA.player import Player
from Game_Interface.board import Board


class minimax_player(Player) :
    
    def __init__(self,depth) :
        self.name= "Minimax player, depth" + str(depth)
        self.depth=depth
        self.number_games=0
    
    def get_name(self) :
        return self.name
    
    def move(self,board,ignore_history=True) :
        algo = self.minimax_search(board,self.depth,board.player_turn,ignore_history)
        return algo[1]
    
    def get_numbergames(self) :
        return self.number_games
        
    def minimax_search(self,board,depth,player,ignore_history=True) :
        
        board.player_turn = player
        
        if ignore_history!=True and len(ignore_history)>=17 and ignore_history[len(ignore_history)-17].spots==ignore_history[len(ignore_history)-9].spots==board.spots :
            return board.evaluate(True),board
        
        if ignore_history!=True and len(ignore_history)>=25 :
            same = True
            i=0
            while i<=23 and same == True :
                if ignore_history[len(ignore_history)-(25-i)].numbers() != ignore_history[len(ignore_history)-(25-i-1)].numbers() :
                    same=False
                i+=1
            if same :
                return board.evaluate(True),board
            
        if depth == 0 or board.is_game_over() :
            return board.evaluate(),board
    
        #Récursivité
        if player:
            score = float('-inf')
            best_move = None
            moves = board.get_possible_next_moves()
            boards = board.get_potential_spots_from_moves(moves)
            for i in range(len(moves)):
                new_board = Board(boards[i])
                
                if ignore_history!=True :
                    ignore_history.append(new_board)
                
                evaluation = self.minimax_search(new_board, depth-1, False,ignore_history)[0]

                egalite=(score==evaluation and i>=1)
                
                score = max(score, evaluation)
                if score == evaluation:
                    if egalite :
                        best_moves.append(moves[i])
                    else :
                        best_moves = [moves[i]]
                    
                if ignore_history!=True :
                    ignore_history.pop()
                    
            best_move = rd.choice(best_moves)

            return score,best_move

        else:
            score = float('inf')
            best_move = None
            moves = board.get_possible_next_moves()
            boards = board.get_potential_spots_from_moves(moves)
            for i in range(len(moves)):
                new_board = Board(boards[i])
                
                if ignore_history!=True :
                    ignore_history.append(new_board)
                
                evaluation = self.minimax_search(new_board, depth-1, True, ignore_history)[0]

                egalite=(score==evaluation and i>=1)
                
                score = min(score, evaluation)
                if score == evaluation:
                    if egalite :
                        best_moves.append(moves[i])
                    else :
                        best_moves = [moves[i]]
                    
                if ignore_history!=True :
                    ignore_history.pop()
                
            best_move = rd.choice(best_moves)
            
            return score,best_move