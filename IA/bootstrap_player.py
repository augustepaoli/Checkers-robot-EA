import numpy as np
import time
import pickle
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

class bootstrap_player(Player) :

    ALL_FEATURES=["number_pawns_p1","number_pawns_p2","number_kings_p1","number_kings_p2","number_pieces_3or4_p1","number_pieces_3or4_p2","number_pieces_5or6_p1","number_pieces_5or6_p2"]
    VALABS_FEATURES_MAX=np.array([12,12,12,12,8,8,8,8])
    CST_VAR=1

    def __init__(self,default_depth,learning=True,step=5e-2,theta_init="rd",features="all") :
        self.learning=learning
        self.name = "bootstrap_player"+str(int(time.time()*1000))
        self.default_depth = default_depth
        self.step=step
        
        if features=="all" :
            self.features=self.ALL_FEATURES
        else :
            self.features=features
        
        if theta_init=="rd" :
            self.theta=np.random.randn(len(self.features))
        else :
            self.theta=theta_init

        new_mean=np.mean(self.theta)    
        new_var=np.var(self.theta)
        self.theta=(self.CST_VAR/new_var)*(self.theta-new_mean)

        self.number_games=0
        self.counting_error=False
        self.total_square_error=0.0
        self.number_scores_counted=0

        return   
    
    def get_name(self) :
        return self.name

    def save(self) :
        target_path = os.path.abspath(os.path.join(
                        os.path.dirname(__file__), 
                        os.pardir,
                        "saved_IAs")
        )
        filename = self.name + '.obj'
        completeName = os.path.join(target_path, filename)

        file = open(completeName,'wb')
        pickle.dump(self,file)
        file.close()
        return

    def delete(self) :
        target_path = os.path.abspath(os.path.join(
                        os.path.dirname(__file__), 
                        os.pardir,
                        "saved_IAs")
        )
        filename = self.name + '.obj'
        completeName = os.path.join(target_path, filename)
        if os.path.exists(completeName) :
            os.remove(completeName)
        return

    @staticmethod
    def load(name) :

        target_path = os.path.abspath(os.path.join(
                        os.path.dirname(__file__), 
                        os.pardir,
                        "saved_IAs")
        )
        filename = name + '.obj'
        completeName = os.path.join(target_path, filename)

        file=open(completeName,'rb')
        player=pickle.load(file)
        return player

    def set_learning(self,learning) :
        self.learning=learning
    
    def move(self,board,ignore_history=True,depth="default") :
        
        if depth=="default" :
            depth=self.default_depth
        
        return self.minimax_search(board,depth,board.player_turn,depth,ignore_history)[1]
    
    def get_numbergames(self) :
        return self.number_games
    
    def get_features_values(self,board) :
        return np.array(board.get_features_values(self.features))
    
    def evaluate(self,board,repetition=False) :
        if repetition :
            print("il y a fin par repetition")
            val=self.evaluate(board)
            print(val)
            if val>0 :
                return np.inf
            if val<0 :
                return -np.inf
            return 0
        
        if board.is_game_over() :
            print("game over")
            if board.player_turn :
                return(-np.inf)
            return(np.inf)
        
        return np.dot(np.transpose(self.theta),self.get_features_values(board))
    
    def max_evaluate(self) :
        theta_abs=np.array(np.abs(self.theta))
        return np.dot(np.transpose(theta_abs),self.VALABS_FEATURES_MAX[:len(self.features)])

    def count_error(self,board,score) :

        if not np.isfinite(score) :
            if score>0 :
                score=self.max_evaluate()
            else :
                score=-self.max_evaluate()
                
        error=score-self.evaluate(board)

        self.total_square_error=(self.number_scores_counted*self.total_square_error+error**2)/(self.number_scores_counted+1)
        self.number_scores_counted+=1
    
    def update_theta(self,board,score) :
        end_game=False
        if not np.isfinite(score) :
            end_game=True
            if score>0 :
                score=self.max_evaluate()
            else :
                score=-self.max_evaluate()
        if end_game :
            board.print_board()
            print(score)
            print(self.evaluate(board))
        error=score-self.evaluate(board)
        step=self.step/((self.get_numbergames()+1)**(2/3))
        delta_theta=step*error*self.get_features_values(board)
        
        self.theta+=delta_theta
        
        ##On veut garder un ecart-type constant dans le vecteur theta, et une moyenne à 0
        new_mean=np.mean(self.theta)    
        new_var=np.var(self.theta)
        self.theta=(np.sqrt(self.CST_VAR/new_var))*(self.theta-new_mean)
        
        return
    
    def minimax_search(self,board,depth,player,depth_total,ignore_history=True) :
            
        board.player_turn = player
        
        if ignore_history!=True and len(ignore_history)>=17 and ignore_history[len(ignore_history)-17].spots==ignore_history[len(ignore_history)-9].spots==board.spots :
            return self.evaluate(board,True),board
        
        if ignore_history!=True and len(ignore_history)>=25 :
            same = True
            for i in range(24) :
                if ignore_history[len(ignore_history)-i-1].numbers() != ignore_history[len(ignore_history)-i-2].numbers() :
                    same=False
            if same :
                return self.evaluate(board,True),board
            
        if depth == 0 or board.is_game_over() :
            return self.evaluate(board),board
    
        #Récursivité
        if player:
            score = -np.inf
            best_move = None
            moves = board.get_possible_next_moves()
            boards = board.get_potential_spots_from_moves(moves)
            for i in range(len(moves)):
                new_board = Board(boards[i])
                
                if ignore_history!=True :
                    ignore_history.append(new_board)
                
                evaluation = self.minimax_search(new_board, depth-1,False,depth_total,ignore_history)[0]
                
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
            
            if self.learning and depth==depth_total : 
                self.update_theta(board,score)

            if self.counting_error and depth==depth_total :
                self.count_error(board,score)
                
            return score,best_move

        else:
            score = np.inf
            best_move = None
            moves = board.get_possible_next_moves()
            boards = board.get_potential_spots_from_moves(moves)
            for i in range(len(moves)):
                new_board = Board(boards[i])
                
                if ignore_history!=True :
                    ignore_history.append(new_board)
                
                evaluation = self.minimax_search(new_board, depth-1, True,depth_total,ignore_history)[0]
                
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
                    
            if self.learning and depth==depth_total : 
                self.update_theta(board,score)
                
            if self.counting_error and depth==depth_total :
                self.count_error(board,score)

            return score,best_move