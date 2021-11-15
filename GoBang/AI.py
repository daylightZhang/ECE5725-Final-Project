# AI algorithm for GoBang game 
# Author: Jingkai Zhang
# Date: 2021.11.13


from Config import * 

# attack_coefficient = 1                
# difficulty = 1                        # it is actually the search depth of tree
# depth_of_search = difficulty * 2 + 1  # search depth of tree


# class Stupid_AI(object):
#     def __init__(self, difficulty=1):
#         self.attack_coefficient = 1     # when this coefficient > 1, means attack, if it is < 1, means defend
#         self.depth_of_search = difficulty * 2 + 1  # search depth of tree
#         self.chessboard = CHESS_BOARD
        
#     def update_chessboard(self,chessboard):
#         self.chessboard = chessboard
    
#     def evaluate(self):
#         '''
#             Rules: 
#               situation                     score
#             Five in a row                   999999 win
#             Four in a row                   100
#             three (two side/one side)       60/30
#             two                             20/15
#             one                             5/0
#         '''
        


#class Smart_AI(Object):