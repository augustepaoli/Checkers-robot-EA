import pygame

import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from Game_Interface.piece import Piece
from Game_Interface.board import Board

class Interface :
    
    WIDTH, HEIGHT = 800, 800
    ROWS, COLS = 8, 8
    SQUARE_SIZE = WIDTH//COLS

    # rgb
    RED = (236, 112, 99)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GREY = (128,128,128)

    def __init__(self,FPS=60) :
        
        self.fps=60
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.selected = None
        self.board = Board()
        self.turn = self.RED
        self.valid_moves = []
        
        pygame.display.set_caption('Checkers')
        self.board.draw(self.win)
        pygame.display.update()
        
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
        
    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
            else :
                return result
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_possible_next_moves_from_piece(piece) 
        return False
    
    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        
        coord_val_moves = []
        for l in self.valid_moves:
            coord_val_moves.append(l[-1])
            
        if self.selected and piece == 0 and [row, col] in coord_val_moves:
            for j in range(len(coord_val_moves)):
                if coord_val_moves[j] == [row,col]:
                    finalj = j
            self.board.make_move_from_piece(self.selected, self.valid_moves[finalj])
            self.change_turn()
            return True
        return False
    
    def change_turn(self):
        self.valid_moves = []
        self.selected=None
        if self.turn == self.RED:
            self.turn = self.WHITE
        else:
            self.turn = self.RED
            
    def set_turn(self,turn) :
        if turn :
            self.turn=self.RED
        else :
            self.turn=self.WHITE
            
    def get_row_col_from_mouse(self,pos):
        x, y = pos
        row = y // self.SQUARE_SIZE
        col = x // self.SQUARE_SIZE
        return row, col
    
    def draw_valid_moves(self, moves):
        for move in moves:
            les_moves = move[1:]
            for j in range(len(les_moves)):
                row,col = les_moves[j]
                newrow,newcol = self.board.spotstoreal(row,col)
                pygame.draw.circle(self.win, self.BLUE, (newcol * self.SQUARE_SIZE + self.SQUARE_SIZE//2, newrow * self.SQUARE_SIZE + self.SQUARE_SIZE//2), 15)
        