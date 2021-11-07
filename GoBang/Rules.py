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


# For each cell on the board, the status can be defined
# the chess pieces round the cell 

'''
class Cell():
    def __init__(self):
        self.x = None      # the horizontal position on the board 
        self.y = None      # the vertical position on the board
        self.type = None   # empty, player1 or player2 
    
    def set_pos(self,pos): 
        """set_pos [set chess pieces position on chessboard]

        :param pos: [it is a position on chessboard (x,y)]
        :type pos: [turple]
        """
        self.x = pos[0] 
        self.y = pos[1]
        
    def get_pos(self):
        return (self.x,self.y)    
    
    def set_type(self,type):
        self.type = type 
    
    def get_type(self):
        return self.type
        
'''




