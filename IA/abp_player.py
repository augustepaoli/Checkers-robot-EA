import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from IA.player import Player
from Game_Interface.board import Board


class abp_player(Player) :
    
    def __init__(self,depth) :
        self.name= "ABP player, depth" + str(depth)
        self.depth=depth
        self.number_games=0
    
    def get_name(self) :
        return self.name
    
    def move(self,board,ignore_history=True) :
        alpha = float('-inf')
        beta = float('inf')
        algo = self.abp_search(board,self.depth,alpha,beta,board.player_turn,ignore_history)
        return algo[1]
    
    def get_numbergames(self) :
        return self.number_games
        
    def abp_search(self,board,depth,alpha,beta,player,ignore_history=True) :
        
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
                child = Board(boards[i])
                
                if ignore_history!=True :
                    ignore_history.append(child)
                
                evaluation = self.abp_search(child, depth-1, alpha,beta, False,ignore_history)[0]
                score = max(score, evaluation)
                alpha = max(alpha, evaluation)
                if(best_move == None or evaluation>=score):
                    best_move = moves[i]
                    
                if ignore_history!=True :
                    ignore_history.pop()

                if beta <= alpha:
                    break
                    
            return score,best_move

        else:
            score = float('inf')
            best_move = None
            moves = board.get_possible_next_moves()
            boards = board.get_potential_spots_from_moves(moves)
            for i in range(len(moves)):
                child = Board(boards[i])
                
                if ignore_history!=True :
                    ignore_history.append(child)
                
                evaluation = self.abp_search(child, depth-1, alpha, beta, True, ignore_history)[0]
                score = min(score, evaluation)
                beta = min(beta,evaluation)
                if (best_move == None or evaluation<=score):
                    best_move = moves[i]
                    
                if ignore_history!=True :
                    ignore_history.pop()

                if beta <= alpha:
                    break
                
            return score,best_move