'''
    Description:
        Implementation of GoBang rules (e.g. win rules)
    Author: 
        Jingkai Zhang (jz544@cornell.edu)
    Version:
        1.0
    Update history:
        1.0 -Add basic judging rules 
    Last modified:
        2021.11.4 -add basic content 
'''
from Config import *   # get all the constant

# Eight direction for a single cell. Why only 4 here?
# Because we are going to use -1 to extend it to eight
# More details can be seen in function 'win_judgment'
DIRECTIONS = ((1, 0), (0, 1), (1, 1), (-1, 1)) 
X = 0
Y = 1

def win_judgment(board, new_piece_pos, piece_type):
    """win_judgment [judge whether the new_piece will win or not]

    :param board: [the 2-D array that indicate the status of chessboard]
    :type board: [list]
    :param new_piece_pos: [the posisiton of new piece]
    :type new_piece_pos: [turple]
    :param piece_type: [black/white/empty]
    :type piece_type: [int]
    :return: [True if piece_type win]
    :rtype: [bool]
    """
    x, y = new_piece_pos[0], new_piece_pos[1]
    
    for direction in DIRECTIONS: # choose one of the direction 
        piece_in_a_line = 1      # count the number of pieces in a line for each direction
        for sub_direction in (1,-1):         # in this way, we can evaluate 8 directions 
            search_x = x + sub_direction * direction[X]
            search_y = y + sub_direction * direction[Y]
            for i in range(4):   # If five pieces in a row, win
                                 # Why range(4)? Because the new piece has been included
                                 # We only need to find other 4 in a line to judge
                '''              
                    Two basic criterion 
                    1. If the color is not same, pass 
                    2. exceed boundry, pass 
                '''
                # print('search_x,search_y=',search_x,' ',search_y)
                # print('board[search_x][search_y] = ',board[search_x][search_y])
                if search_x < 1 or search_x > BOARD_ORDER \
                    or search_y < 1 or search_y > BOARD_ORDER \
                        or piece_type is not board[search_x][search_y]:
                    # print('break')
                    break 
                elif piece_type == board[search_x][search_y]:
                    # print('piece in a line')
                    piece_in_a_line += 1 
                    search_x += sub_direction * direction[X]
                    search_y += sub_direction * direction[Y]
            if piece_in_a_line >= 5:
                return True
    return False



