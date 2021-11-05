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
        self.RUNNING = True 
        self.WINNER = None    # 1 stands for player1 win, 2 stands for player2 win
        # title of the game 
        self.TITLE_IMG = pygame.image.load('./resources/gobang_title.png')
        # chess pieces 
        self.WHITE_PIECES_IMG = pygame.transform.scale(pygame.image.load('./resources/white.png'), (35, 35))  # size of chess pieces 
        self.BLACK_PIECES_IMG = pygame.transform.scale(pygame.image.load('./resources/black.png'), (35, 35))
        self.BOARD_IMG = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT)) # create a surface for chess board
        self.BOARD_IMG.fill((240, 200, 0))                           # fill the surface with RGB (240,200,0)
                                            # view the RGB color in https://en.m.fontke.com/tool/rgbschemes/
        # draw the line on the board 
        for n in range(MARGIN_X, CELL_SIZE * (BOARD_ORDER + 1), CELL_SIZE):  # +1 is because n can reach CELL_SIZE * BOARD_ORDER. Otherwise it cannot
            print(n)
            width = 1
            if n == MARGIN_X or n == MARGIN_X + CELL_SIZE * BOARD_ORDER:
                width = 2 
            pygame.draw.line(self.BOARD_IMG, (0, 0, 0), (MARGIN_X, n), (BOARD_WIDTH - MARGIN_X, n), width) # screen, color_rgb, start_point, end_point, width
            pygame.draw.line(self.BOARD_IMG, (0, 0, 0), (n, MARGIN_Y), (n, BOARD_HEIGHT - MARGIN_Y), width)
    
    def refresh(self, surface):
        """refresh [refresh the screen]

        :param surface: [the surface that is going to be refreshed]
        :type surface: [pygame.surface]
        """
        surface.fill((180, 140, 0))             # fill the background color 
        surface.blit(self.TITLE_IMG, (MARGIN_X + 90, MARGIN_Y))    # put the title 
        surface.blit(self.BOARD_IMG, (30, 80))
    
    def run(self):
        while self.RUNNING:
            self.refresh(self.DISPLAY)
            pygame.display.update()

            for event in pygame.event.get():
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     if event.button == 1 and gobang.status == STATUS_RUNNING:
                #         gobang.mouse_down(event.pos[0], event.pos[1])
                if event.type == pygame.QUIT:
                    self.RUNNING = False
                    pygame.quit()  # exit the game
        
        
if __name__ == '__main__':
    main = GoBang_GUI()
    main.run()