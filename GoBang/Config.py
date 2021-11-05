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
        2021.11.4 -add basic content 
'''

# define the constant here
# Warning: it is convenient to directly list all constants here, but it 
#   is dangerous, since they are easy to change.
#   The proper way is to use enum (from enum import Enum) 
#   If time is available, this should be done. 

# define the size of the screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 680

# define the parameter for chessboard
BOARD_ORDER =  19   # The order of board, if it is 19, this means 
                    # the board contains 19 x 19 cells 
CELL_SIZE = 30      # default 30, the size of one cell, it would 30p x 30p
                    # p stands for pixel
MARGIN_X = 15   # the horizontal margin
MARGIN_Y = 15   # the vertical margin

# define the status of the each cell on board
EMPTY_PIECE = 0     # no one has put a piece right here 
PLAYER1_PIECE = 1   # a label for Player_1 
PLAYER2_PIECE = 2   # a label for Player_2 

# define the size of chessboard 
BOARD_WIDTH = 2 * MARGIN_X + BOARD_ORDER * CELL_SIZE 
BOARD_HEIGHT = 2 * MARGIN_Y + BOARD_ORDER * CELL_SIZE


