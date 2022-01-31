import copy
import pygame

import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from Game_Interface.board import Board
from Game_Interface.piece import Piece
from Game_Interface.interface import Interface

class Game_vs_IA :
    
    def __init__(self,IA_player,starter="human") :
        self.last_boards=[]
        self.last_boards.append(Board())
        self.IA_player=IA_player
        
        if starter=="human" :
            self.human_turn=True
            print("Vous avez les rouges ! lorsque vous executerez .end_game(), ce sera à vous de commencer")
        else :
            self.human_turn=False
            print("Vous avez les blancs ! lorsque vous executerez .end_game(), ce sera à l'IA de commencer")
        print("")
        self.interface=Interface()
        
    def same_numbers(self) :
        if len(self.last_boards)>=2 :
            for i in range(len(self.last_boards)-1) :
                if self.last_boards[i].numbers()!=self.last_boards[i+1].numbers() :
                    return False
        return True
        
    def is_game_over(self) :
        board=self.last_boards[len(self.last_boards)-1]
        if board.is_game_over() :
            print("Fin du jeu par manque de coups")
            return board.winner()
        if (len(self.last_boards)>=17 and self.last_boards[len(self.last_boards)-17].spots==self.last_boards[len(self.last_boards)-9].spots==board.spots) or (len(self.last_boards)==25 and self.same_numbers()) :
            if (len(self.last_boards)>=17 and self.last_boards[len(self.last_boards)-17].spots==self.last_boards[len(self.last_boards)-9].spots==board.spots) :
                print("Fin du jeu par posiitons repetees")
            else :
                print("Fin du jeu par chiffres répétés")
            if board.evaluate(True)==100 :
                return 1
            if board.evaluate(True)==-100 :
                return 2
            return 3
        return False
    
    def one_move(self,ignore_history=True) :
        board=copy.deepcopy(self.last_boards[len(self.last_boards)-1])
        turn = board.player_turn
        
        if ignore_history!=True :
            ignore_history=copy.deepcopy(self.last_boards)

        if turn==self.human_turn :
            run = True
            clock = pygame.time.Clock()
            while run:
                clock.tick(self.interface.fps)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = None
                        break

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        row, col = self.interface.get_row_col_from_mouse(pos)
                        newrow,newcol = board.realtospots(row,col)
                        result=self.interface.select(newrow, newcol)
                        if result :
                            run = False
                            break
                            
                self.interface.update()
            
            if run==None :
                return ("end")
            
            board=copy.deepcopy(self.interface.board)
            
        else :
            p=self.IA_player.get_name() + "2"
            
            move=self.IA_player.move(board,ignore_history)
            pygame.time.delay(200)
            board.make_move(move)
            
            piece=self.interface.board.get_piece(move[0][0], move[0][1])
            self.interface.board.make_move_from_piece(piece,move)
            self.interface.set_turn(self.human_turn)
        
        if len(self.last_boards)==25 :
            self.last_boards.pop(0)
        
        self.last_boards.append(board)
        
    def end_game(self,ignore_history=True) :
        
        result=self.is_game_over()
        
        if not result :
            step=self.one_move(ignore_history)
            if step == "end" :
                print("Vous avez arrêté le jeu !")
                pygame.quit()
                return
            return self.end_game(ignore_history)
            
        self.IA_player.number_games+=1
        pygame.quit()
        
        if result==1 :
            if self.human_turn :
                print("Victoire !")
            else :
                print("Défaite...")
        elif result==2 :
            if not self.human_turn :
                print("Victoire !")
            else :
                print("Défaite...")
        else :
            print("Egalité")
        return result