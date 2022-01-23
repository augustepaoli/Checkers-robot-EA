from player import Player

import sys
sys.path.insert(1, '/Users/auguste/Desktop/EA/code /Game')
from board import Board



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
            return board.evaluate(True)
        
        if ignore_history!=True and len(ignore_history)>=25 :
            same = True
            for i in range(24) :
                if ignore_history[len(ignore_history)-i-1].numbers() != ignore_history[len(ignore_history)-i-2].numbers() :
                    same=False
            if same :
                return board.evaluate(True)
            
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
                score = max(score, evaluation)
                if score == evaluation:
                    best_move = moves[i]
                    
                if ignore_history!=True :
                    ignore_history.pop()
                    
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
                score = min(score, evaluation)
                if score == evaluation:
                    best_move = moves[i]
                    
                if ignore_history!=True :
                    ignore_history.pop()
                
            return score,best_move