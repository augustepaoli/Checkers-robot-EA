import copy

import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from Game.board import Board


class Game :
    
    def __init__(self,p1,p2) :
        self.last_boards=[]
        self.p1=p1
        self.p2=p2
        self.last_boards.append(Board())
    
    def same_numbers(self) :
        if len(self.last_boards)>=2 :
            for i in range(len(self.last_boards)-1) :
                if self.last_boards[i].numbers()!=self.last_boards[i+1].numbers() :
                    return False
        return True
        
    def is_game_over(self) :
        board=self.last_boards[len(self.last_boards)-1]
        if board.is_game_over() :
            return board.winner()
        if (len(self.last_boards)>=17 and self.last_boards[len(self.last_boards)-17].spots==self.last_boards[len(self.last_boards)-9].spots==board.spots) or (len(self.last_boards)==25 and self.same_numbers()) :
            if board.evaluate(True)==100 :
                return 1
            if board.evaluate(True)==-100 :
                return 2
            return 3
        return False
    
    def one_move(self,verbose=False,ignore_history=True) :
        board=copy.deepcopy(self.last_boards[len(self.last_boards)-1])
        turn = board.player_turn
        
        if ignore_history!=True :
            ignore_history=copy.deepcopy(self.last_boards)

        if turn :
            p=self.p1.get_name() + "1"
            board.make_move(self.p1.move(board,ignore_history))
        else :
            p=self.p2.get_name() + "2"
            board.make_move(self.p2.move(board,ignore_history))
        
        if len(self.last_boards)==25 :
            self.last_boards.pop(0)
        
        self.last_boards.append(board)
        
        if verbose :
            print(p + " a joué")
            board.print_board()
        
    def end_game(self,verbose=False,ignore_history=True) :
        result=self.is_game_over()
        if not result :
            self.one_move(verbose,ignore_history)
            return self.end_game(verbose,ignore_history)
        
        board=self.last_boards[len(self.last_boards)-1]
        
        if verbose :
            if result == 1 :
                print(self.p1.get_name() + "1" + " a gagné :")
            if result == 2 :
                print(self.p2.get_name() + "2" + " a gagné :")
            if result == 3:
                print("Il y a égalité")
            print(result)
            board.print_board()
            
        self.p1.number_games+=1
        self.p2.number_games+=1
        
        return result