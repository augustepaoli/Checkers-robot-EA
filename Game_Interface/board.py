import math
import copy
from functools import reduce
import pygame

import os
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(
                  os.path.dirname(__file__), 
                  os.pardir)
)
sys.path.append(PROJECT_ROOT)

from Game_Interface.piece import Piece

class Board:
    """
    A class to represent and play an 8x8 game of checkers.
    """
    EMPTY_SPOT = 0
    P1 = 1
    P2 = 2
    P1_K = 3
    P2_K = 4
    BACKWARDS_PLAYER = P2
    HEIGHT = 8
    WIDTH = 4
    
    WIDTH_DRAW, HEIGHT_DRAW = 800, 800
    ROWS, COLS = 8, 8
    SQUARE_SIZE = WIDTH_DRAW//COLS

    # rgb
    RED = (236, 112, 99)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)
    GREY = (128,128,128)
    
    def __init__(self, old_spots=None, the_player_turn=True):
        """
        Initializes a new instance of the Board class.  Unless specified otherwise, 
        the board will be created with a start board configuration.
        
        NOTE:
        Maybe have default parameter so board is 8x8 by default but nxn if wanted.
        """
        self.player_turn = the_player_turn 
        if old_spots is None:   
            self.spots = [[j, j, j, j] for j in [self.P1, self.P1, self.P1, self.EMPTY_SPOT, self.EMPTY_SPOT, self.P2, self.P2, self.P2]]
        else:
            self.spots = old_spots


    def reset_board(self):
        """
        Resets the current configuration of the game board to the original 
        starting position.
        """
        self.spots = Board().spots
        
    
    def empty_board(self):
        """
        Removes any pieces currently on the board and leaves the board with nothing but empty spots.
        """
        self.spots = [[j, j, j, j] for j in [self.EMPTY_SPOT] * self.HEIGHT]  # Make sure [self.EMPTY_SPOT]*self.HEIGHT] has no issues
    
    
    def is_game_over(self):
        """
        Finds out and returns weather the game currently being played is over or
        not.
        """
        if not self.get_possible_next_moves():
            return True
        return False


    def not_spot(self, loc):
        """
        Finds out of the spot at the given location is an actual spot on the game board.
        """
        if len(loc) == 0 or loc[0] < 0 or loc[0] > self.HEIGHT - 1 or loc[1] < 0 or loc[1] > self.WIDTH - 1:
            return True
        return False
    
    
    def get_spot_info(self, loc):
        """
        Gets the information about the spot at the given location.
        
        NOTE:
        Might want to not use this for the sake of computational time.
        """
        return self.spots[loc[0]][loc[1]]
    
    
    def forward_n_locations(self, start_loc, n, backwards=False):
        """
        Gets the locations possible for moving a piece from a given location diagonally
        forward (or backwards if wanted) a given number of times(without directional change midway).  
        """
        if n % 2 == 0:
            temp1 = 0
            temp2 = 0
        elif start_loc[0] % 2 == 0:
            temp1 = 0
            temp2 = 1 
        else:
            temp1 = 1
            temp2 = 0

        answer = [[start_loc[0], start_loc[1] + math.floor(n / 2) + temp1], [start_loc[0], start_loc[1] - math.floor(n / 2) - temp2]]

        if backwards: 
            answer[0][0] = answer[0][0] - n
            answer[1][0] = answer[1][0] - n
        else:
            answer[0][0] = answer[0][0] + n
            answer[1][0] = answer[1][0] + n

        if self.not_spot(answer[0]):
            answer[0] = []
        if self.not_spot(answer[1]):
            answer[1] = []
            
        return answer
    

    def get_simple_moves(self, start_loc):
        """    
        Gets the possible moves a piece can make given that it does not capture any opponents pieces.
        
        PRE-CONDITION:
        -start_loc is a location with a players piece
        """
        if self.spots[start_loc[0]][start_loc[1]] > 2:
            next_locations = self.forward_n_locations(start_loc, 1)
            next_locations.extend(self.forward_n_locations(start_loc, 1, True))
        elif self.spots[start_loc[0]][start_loc[1]] == self.BACKWARDS_PLAYER:
            next_locations = self.forward_n_locations(start_loc, 1, True)  # Switched the true from the statement below
        else:
            next_locations = self.forward_n_locations(start_loc, 1)
        

        possible_next_locations = []

        for location in next_locations:
            if len(location) != 0:
                if self.spots[location[0]][location[1]] == self.EMPTY_SPOT:
                    possible_next_locations.append(location)
            
        return [[start_loc, end_spot] for end_spot in possible_next_locations]      
           
     
    def get_capture_moves(self, start_loc, move_beginnings=None):
        """
        Recursively get all of the possible moves for a piece which involve capturing an opponent's piece.
        """
        if move_beginnings is None:
            move_beginnings = [start_loc]
            
        answer = []
        if self.spots[start_loc[0]][start_loc[1]] > 2:  
            next1 = self.forward_n_locations(start_loc, 1)
            next2 = self.forward_n_locations(start_loc, 2)
            next1.extend(self.forward_n_locations(start_loc, 1, True))
            next2.extend(self.forward_n_locations(start_loc, 2, True))
        elif self.spots[start_loc[0]][start_loc[1]] == self.BACKWARDS_PLAYER:
            next1 = self.forward_n_locations(start_loc, 1, True)
            next2 = self.forward_n_locations(start_loc, 2, True)
        else:
            next1 = self.forward_n_locations(start_loc, 1)
            next2 = self.forward_n_locations(start_loc, 2)
        
        
        for j in range(len(next1)):
            if (not self.not_spot(next2[j])) and (not self.not_spot(next1[j])) :  # if both spots exist
                if self.get_spot_info(next1[j]) != self.EMPTY_SPOT and self.get_spot_info(next1[j]) % 2 != self.get_spot_info(start_loc) % 2:  # if next spot is opponent
                    if self.get_spot_info(next2[j]) == self.EMPTY_SPOT:  # if next next spot is empty
                        temp_move1 = copy.deepcopy(move_beginnings)
                        temp_move1.append(next2[j])
                        
                        answer_length = len(answer)
                        
                        if self.get_spot_info(start_loc) != self.P1 or next2[j][0] != self.HEIGHT - 1: 
                            if self.get_spot_info(start_loc) != self.P2 or next2[j][0] != 0: 

                                temp_move2 = [start_loc, next2[j]]
                                
                                temp_board = Board(copy.deepcopy(self.spots), self.player_turn)
                                temp_board.make_move(temp_move2, False)

                                answer.extend(temp_board.get_capture_moves(temp_move2[1], temp_move1))
                                
                        if len(answer) == answer_length:
                            answer.append(temp_move1)
                            
        return answer
    
        
    def get_possible_next_moves(self):
        """
        Gets the possible moves that can be made from the current board configuration.
        """
        piece_locations = []
        for j in range(self.HEIGHT):
            for i in range(self.WIDTH):
                if (self.player_turn == True and (self.spots[j][i] == self.P1 or self.spots[j][i] == self.P1_K)) or (self.player_turn == False and (self.spots[j][i] == self.P2 or self.spots[j][i] == self.P2_K)):
                    piece_locations.append([j, i])
                    
        try:  #Should check to make sure if this try statement is still necessary 
            capture_moves = list(reduce(lambda a, b: a + b, list(map(self.get_capture_moves, piece_locations))))  # CHECK IF OUTER LIST IS NECESSARY

            if len(capture_moves) != 0:
                return capture_moves

            return list(reduce(lambda a, b: a + b, list(map(self.get_simple_moves, piece_locations))))  # CHECK IF OUTER LIST IS NECESSARY
        except TypeError:
            return []
    
    
    def make_move(self, move, switch_player_turn=True):
        """
        Makes a given move on the board, and (as long as is wanted) switches the indicator for
        which players turn it is.
        """
        if abs(move[0][0] - move[1][0]) == 2:
            for j in range(len(move) - 1):
                if move[j][0] % 2 == 1:
                    if move[j + 1][1] < move[j][1]:
                        middle_y = move[j][1]
                    else:
                        middle_y = move[j + 1][1]
                else:
                    if move[j + 1][1] < move[j][1]:
                        middle_y = move[j + 1][1]
                    else:
                        middle_y = move[j][1]
                        
                self.spots[int((move[j][0] + move[j + 1][0]) / 2)][middle_y] = self.EMPTY_SPOT
                
                
        self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.spots[move[0][0]][move[0][1]]
        if move[len(move) - 1][0] == self.HEIGHT - 1 and self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] == self.P1:
            self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.P1_K
        elif move[len(move) - 1][0] == 0 and self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] == self.P2:
            self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.P2_K
        else:
            self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.spots[move[0][0]][move[0][1]]
        self.spots[move[0][0]][move[0][1]] = self.EMPTY_SPOT
                
        if switch_player_turn:
            self.player_turn = not self.player_turn
       

    def get_potential_spots_from_moves(self, moves):
        """
        Get's the potential spots for the board if it makes any of the given moves.
        If moves is None then returns it's own current spots.
        """
        if moves is None:
            return self.spots
        answer = []
        for move in moves:
            original_spots = copy.deepcopy(self.spots)
            self.make_move(move, switch_player_turn=False)
            answer.append(self.spots) 
            self.spots = original_spots 
        return answer
        
        
    def insert_pieces(self, pieces_info):
        """
        Inserts a set of pieces onto a board.
        pieces_info is in the form: [[vert1, horz1, piece1], [vert2, horz2, piece2], ..., [vertn, horzn, piecen]]
        """
        for piece_info in pieces_info:
            self.spots[piece_info[0]][piece_info[1]] = piece_info[2]
        
    
    def get_symbol(self, location):
        """
        Gets the symbol for what should be at a board location.
        """
        if self.spots[location[0]][location[1]] == self.EMPTY_SPOT:
            return " "
        elif self.spots[location[0]][location[1]] == self.P1:
            return "o"
        elif self.spots[location[0]][location[1]] == self.P2:
            return "x"
        elif self.spots[location[0]][location[1]] == self.P1_K:
            return "O"
        else:
            return "X"
    
    
    def print_board(self):
        """
        Prints a string representation of the current game board.
        """
        norm_line = "|---|---|---|---|---|---|---|---|"
        print(norm_line)
        for j in range(self.HEIGHT):
            if j % 2 == 1:
                temp_line = "|///|"
            else:
                temp_line = "|"
            for i in range(self.WIDTH):
                temp_line = temp_line + " " + self.get_symbol([j, i]) + " |"
                if i != 3 or j % 2 != 1:  # should figure out if this 3 should be changed to self.WIDTH-1
                    temp_line = temp_line + "///|"
            print(temp_line)
            print(norm_line)
            
    ##########
    #Pour impl??menter l'interface
    ##########
    
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
        
    def draw_squares(self, win):
        win.fill(self.BLACK)
        for row in range(self.ROWS):
            for col in range(row % 2, self.COLS, 2):
                pygame.draw.rect(win, self.RED, (row*self.SQUARE_SIZE, col *self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw(self, win):
        self.draw_squares(win)
        for row in range(self.ROWS):
            for col in range(self.COLS):
                spotsrow,spotscol = self.realtospots(row,col)
                if spotsrow==-1:
                    piece=0
                else:
                    piece = self.get_piece(spotsrow,spotscol)
                if piece != 0:
                    piece.draw(win)
                    
    def get_symbol(self, location):
        """
        Gets the symbol for what should be at a board location.
        """
        if self.spots[location[0]][location[1]] == self.EMPTY_SPOT:
            return " "
        elif self.spots[location[0]][location[1]] == self.P1:
            return "o"
        elif self.spots[location[0]][location[1]] == self.P2:
            return "x"
        elif self.spots[location[0]][location[1]] == self.P1_K:
            return "O"
        else:
            return "X"
        
    def get_piece(self, row, col):
        nb = self.spots[row][col]
        if nb != 0:
            return(Piece(row,col,nb))
        else:
            return(0)
                    
    def get_possible_next_moves_from_piece(self,piece):
        row,col = piece.row,piece.col
        l=[]
        liste = self.get_possible_next_moves()
        for i in range(len(liste)):
            if liste[i][0] == [row,col]:
                l.append(liste[i])
        return(l)
    
    def make_move_from_piece(self, piece, move, switch_player_turn=True):
        """
        Makes a given move on the board, and (as long as is wanted) switches the indicator for
        which players turn it is.
        """
        print(move)
        piece.move(move[-1][0],move[-1][1])
        if abs(move[0][0] - move[1][0]) == 2:
            for j in range(len(move) - 1):
                if move[j][0] % 2 == 1:
                    if move[j + 1][1] < move[j][1]:
                        middle_y = move[j][1]
                    else:
                        middle_y = move[j + 1][1]
                else:
                    if move[j + 1][1] < move[j][1]:
                        middle_y = move[j + 1][1]
                    else:
                        middle_y = move[j][1]
                        
                self.spots[int((move[j][0] + move[j + 1][0]) / 2)][middle_y] = self.EMPTY_SPOT
                
                
        self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.spots[move[0][0]][move[0][1]]
        if move[len(move) - 1][0] == self.HEIGHT - 1 and self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] == self.P1:
            self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.P1_K
            piece.make_king()
        elif move[len(move) - 1][0] == 0 and self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] == self.P2:
            self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.P2_K
            piece.make_king()
        else:
            self.spots[move[len(move) - 1][0]][move[len(move) - 1][1]] = self.spots[move[0][0]][move[0][1]]
        self.spots[move[0][0]][move[0][1]] = self.EMPTY_SPOT
                
        if switch_player_turn:
            self.player_turn = not self.player_turn
            
    #########
    #Pour les IAs
    #########  
            
    def numbers(self):
        
        p1c,p1k,p2c,p2k,p134,p234,p156,p256,p1center,p2center,p1bridge,p2bridge=0,0,0,0,0,0,0,0,0,0,0,0

        for i in range(8):
            for j in range(4):
                location = i,j
                if self.spots[location[0]][location[1]] == self.EMPTY_SPOT:
                    pass
                elif self.spots[location[0]][location[1]] == self.P1:
                    p1c+=1
                    if i==2 or i==3 :
                        p134+=1
                    if i==4 or i==5 : 
                        p156+=1
                    if (i==3 and (j==1 or j==2)) or (i==4 and (j==1 or j==2)) :
                        p1center+=1
                elif self.spots[location[0]][location[1]] == self.P2:
                    p2c+=1
                    if i==2 or i==3 :
                        p256+=1
                    if i==4 or i==5 : 
                        p234+=1
                    if (i==3 and (j==1 or j==2)) or (i==4 and (j==1 or j==2)) :
                        p2center+=1
                elif self.spots[location[0]][location[1]] == self.P1_K:
                    p1k+=1
                    if (i==3 and (j==1 or j==2)) or (i==4 and (j==1 or j==2)) :
                        p1center+=1
                else:
                    p2k+=1
                    if (i==3 and (j==1 or j==2)) or (i==4 and (j==1 or j==2)) :
                        p2center+=1
        
        p1bridge = 1
        p2bridge = 1
        
        if p2k>0 :
            p1bridge=0
        else :
            if self.spots[0][1] != self.P1 or self.spots[0][3] != self.P1 :
                p1bridge = 0

        if p1k>0 :
            p2bridge=0
        else :
            if self.spots[7][0] != self.P2 or self.spots[7][2] != self.P2 :
                p2bridge = 0

        return p1c,p2c,p1k,p2k,p134,p234,p156,p256,p1center,p2center,p1bridge,p2bridge
    
    def get_features_values(self,features) :
        numbers=self.numbers()
        answer=[]

        for name_feature in features :
            if name_feature=="number_pawns_p1" :
                answer.append(numbers[0])
            if name_feature=="number_pawns_p2" :
                answer.append(numbers[1])
            if name_feature=="number_kings_p1" :
                answer.append(numbers[2])
            if name_feature=="number_kings_p2" :
                answer.append(numbers[3])
            if name_feature=="number_pieces_3or4_p1" :
                answer.append(numbers[4])
            if name_feature=="number_pieces_3or4_p2" :
                answer.append(numbers[5])
            if name_feature=="number_pieces_5or6_p1" :
                answer.append(numbers[6])
            if name_feature=="number_pieces_5or6_p2" :
                answer.append(numbers[7])
            if name_feature=="center_control_p1" :
                answer.append(numbers[8])
            if name_feature=="center_control_p2" :
                answer.append(numbers[9])
            if name_feature=="bridge_p1" :
                answer.append(numbers[10])
            if name_feature=="bridge_p2" :
                answer.append(numbers[11])

        return answer
    
    def evaluate(self,repetition=False):
        if repetition :
            if self.evaluate() > 0 :
                return 100
            if self.evaluate() < 0 :
                return -100
            return 0
        
        if self.is_game_over() :
            if self.player_turn :
                return(-100)
            return(100)
        
        p1c,p2c,p1k,p2k=self.numbers()[:4]
        return(p1c - p2c + 2*(p1k - p2k))
    
    def winner(self):
        if self.is_game_over() :
            if self.player_turn :
                return(2)
            return(1)
        return None