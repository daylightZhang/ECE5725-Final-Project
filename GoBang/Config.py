'''
    Description:
        Configuration for game, e.g. who play first, how big the board is 
    Author: 
        Jingkai Zhang (jz544@cornell.edu)
    Version:
        1.0
    Update history:
        1.0 -Add basic variables 
    Last modified:
        2021.11.4 -add basic parameters 
'''

# define the constant here
# Warning: it is convenient to directly list all constants here, but it 
#   is dangerous, since they are easy to change.
#   The proper way is to use enum (from enum import Enum) 
#   If time is available, this should be done. 

# define some color RGB  
COLOR1 = (255, 0, 0)  # red 
COLOR2 = (0, 255, 0)  # green
# define the size of the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 680

# define the status of the each cell on board
EMPTY_PIECE = 0     # no one has put a piece right here 
PLAYER1_PIECE = 1   # a label for Player_1 
PLAYER2_PIECE = 2   # a label for Player_2 

BLACK_PIECE = 4     # a label for black piece
WHITE_PIECE = 5     # a label for black piece
# define the parameter for chessboard
BOARD_ORDER =  9   # The order of board, if it is 19, this means 
                    # the board contains 19 x 19 cells 
CHESS_BOARD = []    # Two dimensional array used to store every chess piecess on the chessboard

for i in range(1, BOARD_ORDER + 2):                         # +2 is because we don't use (0,0), so we need one more
    row = [EMPTY_PIECE for j in range(1, BOARD_ORDER + 2) ] # +2 is because we don't use (0,0), so we need one more
    CHESS_BOARD.append(row)

LIST_ALL = []
for i in range(BOARD_ORDER):
    for j in range(BOARD_ORDER):
        LIST_ALL.append((i, j))
# print(LIST_ALL)
# print(len(CHESS_BOARD[0])) # output 18
# print(len(CHESS_BOARD[1]))
CELL_SIZE = 50      # default 30, the size of one cell, it would 30p x 30p
                    # p stands for pixel
MARGIN_X = 15   # the horizontal margin
MARGIN_Y = 15   # the vertical margin

MARGIN_X_BOARD = 30 + 50 # the horizontal margin for chessboard 
MARGIN_Y_BOARD = 80 + 50 # the vertical margin for chessboard

# define the size of chessboard 
BOARD_WIDTH = 2 * MARGIN_X + BOARD_ORDER * CELL_SIZE 
BOARD_HEIGHT = 2 * MARGIN_Y + BOARD_ORDER * CELL_SIZE

# define the direction, horizontal, vertical, 45 degree and 135 degree
DIRECTIONS = ((1, 0), (0, 1), (1, 1), (-1, 1))
X = 0    # horizontal indicator usgae: DIRECTION[X] where DIRECTION = (1,0)
Y = 1    # vertical indicator usage: DIRECTION[Y] where DIRECTION = (1,0)


# for i in range(1, BOARD_ORDER + 2):
#     for j in range(1, BOARD_ORDER + 2):
#         print('i=',i, 'j=',j)
#         print(CHESS_BOARD[i][j])
    
    # print(CHESS_BOARD[19][19])
# used for test