import pygame

import pygame

import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

class Piece:

    PADDING = 15
    OUTLINE = 2
    
    WIDTH, HEIGHT = 800, 800
    ROWS, COLS = 8, 8
    SQUARE_SIZE = WIDTH//COLS

    # rgb
    RED = (236, 112, 99)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GREY = (128,128,128)

    CROWN = pygame.transform.scale(pygame.image.load('Game_Interface/crown.png'), (44, 25))


    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def __init__(self, row, col, nb):
        self.row = row
        self.col = col
        if nb == 1 or nb == 3:
            self.color = self.RED
        if nb == 2 or nb == 4:
            self.color = self.WHITE
        if nb == 1 or nb == 2:
            self.king = False
        if nb == 3 or nb == 4:
            self.king = True
        self.x = 0
        self.y = 0
        self.calc_pos()
        
    def realtospots(self,row,col):
        if row%2 == 0:
            if col%2==0:
                return(row,int(col/2))
            else:
                return(-1,-1)
        else:
            if col%2==0:
                return(-1,-1)
            else:
                return(row,int((col-1)/2))

    def spotstoreal(self,row,col):
        if row%2 == 0:
            if col%2==0:
                return(row,int(2*col))
            else:
                if col==1:
                    return(row,2)
                else:
                    return(row,6)
        else:
            return(row,int(2*col+1))
        
    def calc_pos(self):
        newrow,newcol = self.spotstoreal(self.row,self.col)
        self.x = self.SQUARE_SIZE * newcol + self.SQUARE_SIZE // 2
        self.y = self.SQUARE_SIZE * newrow + self.SQUARE_SIZE // 2

    def make_king(self):
        self.king = True
    
    def draw(self, win):
        radius = self.SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, self.GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(self.CROWN, (self.x - self.CROWN.get_width()//2, self.y - self.CROWN.get_height()//2))

    def move(self, row,col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)