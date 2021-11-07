'''
    Description:
        Implementation of GoBang GUI via pygame
    Author: 
        Jingkai Zhang (jz544@cornell.edu)
    Version:
        1.0
    Update history:
        1.0 -Add basic 
    Last modified:
        2021.11.4 -add basic content 
'''
import pygame               # the whole GUI is implemented by pygame
from Config import *        # import all constants

class GoBang_GUI():
    def __init__(self):
        """__init__ [Load the necessary resources]
        """
        # init the pygame 
        pygame.init()
        self.DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # define the status of game 
        self.running = True 
        self.winner = None    #  It could be PLAYER1_PIECES or PLAYER2_PIECES
        self.order = 0        # the number to record the order of each piece sequentially(e.g. 0,1,2,3,4,5,6,...)
        self.is_balck_turn = True 
        self.is_white_turn = False
        # title of the game 
        self.TITLE_IMG = pygame.image.load('./resources/gobang_title.png')
        # chess pieces 
        # Note: pygame.transform.scale() is faster, but smoothscale() gives better image 
        self.WHITE_PIECES_IMG = pygame.transform.smoothscale(pygame.image.load('./resources/white.png'), (30, 30))  # size of chess pieces 
        self.BLACK_PIECES_IMG = pygame.transform.smoothscale(pygame.image.load('./resources/black.png'), (30, 30))
        self.PIECES_ON_BOARD = list()   # list to store all the position of pieces
        # self.WHITE_PIECES_ON_BOARD = list()   # list to store all the position of white pieces
        self.BOARD_IMG = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT)) # create a surface for chess board
        self.BOARD_IMG.fill((240, 200, 0))                           # fill the surface with RGB (240,200,0)
                                            # view the RGB color in https://en.m.fontke.com/tool/rgbschemes/
        # draw the line on the board 
        for n in range(MARGIN_X, CELL_SIZE * (BOARD_ORDER + 1), CELL_SIZE):  # +1 is because n can reach CELL_SIZE * BOARD_ORDER. Otherwise it cannot
            width = 1
            if n == MARGIN_X or n == MARGIN_X + CELL_SIZE * BOARD_ORDER:
                width = 2 
            pygame.draw.line(self.BOARD_IMG, (0, 0, 0), (MARGIN_X, n), (BOARD_WIDTH - MARGIN_X, n), width) # screen, color_rgb, start_point, end_point, width
            pygame.draw.line(self.BOARD_IMG, (0, 0, 0), (n, MARGIN_Y), (n, BOARD_HEIGHT - MARGIN_Y), width)
            
    def draw_pieces(self):
        if self.order < 1:  # skip if no piece 
            return 
        for i in range(self.order):  #  drawing the BLACK pieces on the chessboard 
            piece_x, piece_y = self.PIECES_ON_BOARD[i - 1]
            #x_, y_ = self.PIECES_ON_BOARD[i]         # get the position of the current piece on board 
            # judge black or white piece
            piece_img = self.BLACK_PIECES_IMG if CHESS_BOARD[piece_x][piece_y] == BLACK_PIECE else self.WHITE_PIECES_IMG
            self.DISPLAY.blit(piece_img,(MARGIN_X + MARGIN_X_BOARD + (piece_x -1) * CELL_SIZE,\
                                                    MARGIN_Y + MARGIN_Y_BOARD + (piece_y - 1) * CELL_SIZE))
        # for i in range(len(self.ORDER)):
        #     coor = self.ORDER[i]
           # self.DISPLAY.blit(self.playerImg, (self.start_x+coor[0]*CELL_SIZE, self.start_y+coor[1]*CELL_SIZE))
            # draw_text(surface, SCORE_FONT, (255, 0, 0), str(i),\
            # self.start_x+coor[0]*CELL_SIZE+int(CELL_SIZE/2), self.start_y+coor[1]*CELL_SIZE+int(CELL_SIZE/2))
    
    def refresh(self, surface):
        """refresh [refresh the screen]

        :param surface: [the surface that is going to be refreshed]
        :type surface: [pygame.surface]
        """
        surface.fill((180, 140, 0))                                # fill the background color 
        surface.blit(self.TITLE_IMG, (MARGIN_X + 90, MARGIN_Y))    # put the title 
        surface.blit(self.BOARD_IMG, (MARGIN_X_BOARD, MARGIN_Y_BOARD))
        self.draw_pieces()
        
    def mouse_click(self, mouse_x, mouse_y):
        # print('mouse_x = ', mouse_x,' mouse_y = ',mouse_y)
        # this means the click happens in the chessboard
        x, y = 0, 0 # initialize the variables 
        if MARGIN_X + MARGIN_X_BOARD < mouse_x < MARGIN_X + BOARD_ORDER * CELL_SIZE + MARGIN_X_BOARD and \
           MARGIN_Y + MARGIN_Y_BOARD < mouse_y < MARGIN_Y_BOARD + MARGIN_Y + BOARD_ORDER * CELL_SIZE: 
            # print('pressed in chessboard')
            '''
                range of board (0,0) to (18*30, 18*30)
            '''
            x = int((mouse_x - MARGIN_X_BOARD - MARGIN_X) / CELL_SIZE) + 1    # 30 is the horizontal position of chessboard
            y = int((mouse_y - MARGIN_Y_BOARD - MARGIN_Y) / CELL_SIZE) + 1    # 80 is the vertical position of chessboard
            # print('x = ', x, ' y = ', y ) # for debug
            if self.is_balck_turn and CHESS_BOARD[x][y] is EMPTY_PIECE:       # chess piece can be added only when the cell 
                                                                              # is not occupied
                self.PIECES_ON_BOARD.append((x,y))                            # Add the coordinates of new balck pieces 
                CHESS_BOARD[x][y] = BLACK_PIECE                               # Record the type of pieces
                self.is_balck_turn = False                                    # change the turn for white 
                self.is_white_turn = True 
                self.order = self.order + 1                                   # sequence number + 1
            elif self.is_white_turn and CHESS_BOARD[x][y] is EMPTY_PIECE:     # chess piece can be added only when the cell 
                                                                              # is not occupied
                self.PIECES_ON_BOARD.append((x,y))                            # Add the new white pieces 
                CHESS_BOARD[x][y] = WHITE_PIECE                               # Record the type of pieces
                self.is_balck_turn = True                                     # change the turn for black 
                self.is_white_turn = False
                self.order = self.order + 1                                   # sequence number + 1
        
        # elif mouse_x and mouse_y: # this means the click happens in the control panel 
        #pass 
    
    def run(self):
        while self.running:
            self.refresh(self.DISPLAY)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_click(event.pos[0], event.pos[1])
                if event.type == pygame.QUIT:
                    self.RUNNING = False
                    pygame.quit()  # exit the game
        
# for demo test, this part will be moved to the interface in the feature       
if __name__ == '__main__':
    main = GoBang_GUI()
    main.run()