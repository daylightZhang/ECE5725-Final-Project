'''
    Description:
        Implementation of GoBang GUI via pygame
    Author: 
        Jingkai Zhang (jz544@cornell.edu) & Lanyue Fang 
    Version:
        1.1
    Update history:
        1.0 -Add basic 
        1.1 -Add AI
        1.2 -Add interface with hardware 
    Last modified:
        2021.11.4 -add basic content 
        2021.11.14 -add AI, buttons
        2021.11.20 -fix bugs with regret button
        2021.12.8  -add interface 
'''
import pygame               # the whole GUI is implemented by pygame
import math
import threading 
# from GoBang.Config import *        # import all constants
# from GoBang.Rules import *         # import all GoBang Rules
# from GoBang.gobang_AI import ai
from Config import *        # import all constants
from Rules import *         # import all GoBang Rules
from gobang_AI import ai
import os
import json

def default_font(font_size=15):
    """
        @brief define the default font
        @para font_size: the size of font default is 20 
        Example:
            font = default_font(20)
        # get default font format, font_size = 20. 
    """
    pygame.init()
    font_size = font_size
    font_addr = pygame.font.get_default_font()
    font = pygame.font.Font(font_addr,font_size)
    return font

##
# @brief get the default color library 
#
# @return color library
def default_color_lib():
    """
        @brief return the default color library 
        Example:
            default_lib = default_color_lib()
    """
    return {'WHITE':(255,255,255),'RED':(255,0,0),'GREEN':(0,255,0),'BLACK':(0,0,0)}
##
# @brief class for Caption 
class Caption(pygame.sprite.Sprite): # inherit from
    """
       @brief create a caption 
       @para screen: the screen that is going to display 
             font: font format
             text: the content of the caption 
             color: color of font, it can be anything in the color library 
             x: the horizontal position of the caption on the screen 
             y: the vertical position of the caption on the screnn 
       Example:
           s1 = screen 
           font = default_font()
           c1 = Caption(s1,font,'test1','BLUE',100,100)
           #means the caption will be displayed on s1, with default font format,
           #the content is 'test1', and the color is blue, it will be put on (100,100).
    """
    def __init__(self,screen,font,text, color, x=None, y=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.font = font
        self.text = text
        self.color = color
        self.color_lib = default_color_lib()
        self.surface = font.render(text, True, self.color_lib[color])
    
    ##
    # @brief display the caption on the screen 
    #
    # @return None 
    def display(self):
        """
            Example:
                c1 = Caption(s1,font,'test1','BLUE',100,100) # build a caption 
                c1.display() # display on the screen 
        """
        self.screen.blit(self.surface, (self.x, self.y))
    
    ##
    # @change the color of the caption
    #
    # @return None     
#    def change_color(self,COLOR):
#        """
#            Example:
#                c1.change_color('GREEN')
#        """  
#        self.surface= self.font.render(self.text, True,self.color_lib[COLOR])
#        self.color=COLOR        
    ##
    # @change the text of the caption
    #
    # @return None          
    def change_text(self,TEXT):
        """
            Example:
                c1.change_color('RESUME')
        """  
        self.surface= self.font.render(TEXT, True,self.color_lib[self.color])
        self.text=TEXT

##
# @brief pygame button 
class Button(Caption): # inherit from class Caption
    
    ##
    # @brief create a button 
    #
    # @param screen the screen that is going to display 
    # @param font the font format 
    # @param text the content of the button 
    # @param font_color the color of the font 
    # @param rect_color the color of the rect 
    # @param x horizontal position 
    # @param y vertical position 
    # @param is_circle boolean, if the button is a circle 
    #
    # @return None 
    def __init__(self,screen,font,text,font_color,rect_color=None,x=None,y=None,is_circle=False,call_func=None):
        """
            Example:
                def func():
                    print('hello')
                s1 = screen 
                font = default_font 
                b1 = Button(s1,font,'button1','RED','WHITE',150,100,True,func)
                # create a round button with white color, font's color is red. 
                # the button will be put in (150,100), on screen with default_font.
                # func() is used as the reaction for the button.
        """
        super(Button, self).__init__(screen,font,text,font_color,x,y)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.rect = self.surface.get_rect()
        self.rect_color = rect_color
        self.text = text
        self.is_circle = is_circle
        self.call_func = call_func  # call function for the button
        if self.is_circle:
            self.circle_center = self.x + self.width // 2, self.y + self.height // 2
            self.radius = 50

    def change_color(self,COLOR):
        """
            Example:
                c1.change_color('GREEN')
        """
        self.rect_color = COLOR
        #self.color=COLOR    
    ##
    # @brief add call_back function 
    #
    # @return None        
    def add_call_func(self,call_func):
        """
           Example:
               def func():
                   print('hello')
               
               s1 = Button()
               s1.add_call_func(func)
        """
        self.call_func = call_func
    ##
    # @brief reaction of the button
    #
    # @return None
    def reaction(self):
        """
            Example:
                b1 = Button()
                b1.reaction()
        """
        #self.call_func
        exec_func = self.call_func
        exec_func()
    ##
    # @brief display the button 
    #
    # @return None 
    def display(self):
        """
            Example:
                s = Button(xx)
                s.display() # show the button on the screen 
        """
        #print('button dispaly function')
        if self.is_circle:
            pygame.draw.circle(self.screen,self.color_lib[self.rect_color],self.circle_center,self.radius)
        else:
            pygame.draw.rect(self.screen,self.color_lib[self.rect_color],[self.x,self.y,self.width,self.height],0)
        #self.screen.blit(self.surface, (self.x, self.y))
        super(Button, self).display()

    ##
    # @brief check if the mouse if on the button 
    #
    # @param position the position of the mouse 
    #
    # @return True if mouse on the button, else False 
    def is_on_button(self, position):
        """
            Example: 
                position = pygame.event.get_mouse_pos()
                b = Button(xx)
                b.is_on_button(position) 
        """
        if not self.is_circle:
            x_match = self.x < position[0] < self.x + self.width
            y_match = self.y < position[1] < self.y + self.height
            if x_match and y_match:
                return True
            else:
                return False
        else:
            distance = math.pow(position[0] - self.circle_center[0],2) + math.pow(position[1] - self.circle_center[1],2)
            distance = math.sqrt(distance)
            return distance <= self.radius

class GoBang_GUI():
    def __init__(self):
        """__init__ [Load the necessary resources]
        """
        # init the pygame 
        pygame.init()
        self.DISPLAY = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # define the status of game 
        self.running = True 
        self.game_end = False
        self.winner = None    #  It could be PLAYER1_PIECES or PLAYER2_PIECES
        self.order = 0        # the number to record the order of each piece sequentially(e.g. 0,1,2,3,4,5,6,...)
        self.display_orders = []
        self.is_balck_turn = True 
        self.is_white_turn = False
        self.img_path = '/home/pi/Desktop/ECE5725_project/ECE5725-Final-Project/GoBang/resources/'
        # title of the game 
        self.TITLE_IMG = pygame.image.load(os.path.join(self.img_path, 'gobang_title.png'))
        # chess pieces 
        # Note: pygame.transform.scale() is faster, but smoothscale() gives better image 
        self.WHITE_PIECES_IMG = pygame.transform.smoothscale(pygame.image.load(os.path.join(self.img_path, 'white.png')), (50, 50))  
        self.BLACK_PIECES_IMG = pygame.transform.smoothscale(pygame.image.load(os.path.join(self.img_path, 'black.png')), (50, 50))
        self.PIECES_ON_BOARD = list()   # list to store all the position of pieces
        self.WHITE_PIECES_ON_BOARD = list()
        self.BLACK_PIECES_ON_BOARD = list() 
        self.list1 = list()
        self.list2 = list()
        self.list3 = list()
        # self.WHITE_PIECES_ON_BOARD = list()   # list to store all the position of white pieces
        self.BOARD_IMG = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT)) # create a surface for chess board
        self.BOARD_IMG.fill((240, 200, 0))                           # fill the surface with RGB (240,200,0)
                                            # view the RGB color in https://en.m.fontke.com/tool/rgbschemes/
        # define all the buttons here 
        self.button_font = default_font(28)                          # set the font size 
        self.piece_font = default_font(35)
        self.piece_font_2 = default_font(15)
        self.quit_button = Button(self.DISPLAY,self.button_font,'Quit','BLACK','WHITE',680,600,False,None)
        self.regret_button = Button(self.DISPLAY,self.button_font,'Wife Button','BLACK','WHITE',630,500,False,None)
        self.last_piece = 1
        self.file_name = '/home/pi/Desktop/ECE5725_project/ECE5725-Final-Project/info.json'
        self.identify_finished_flag = False                           # flag that is shared with main program
        self.ai_think_finished_flag = False                           # flag that is shared with main program 
        self.clock = pygame.time.Clock()
        self.timer = threading.Timer(1,self.read_chessboard)
        self.timer.start()
        
        # draw the line on the board 
        for n in range(MARGIN_X, CELL_SIZE * (BOARD_ORDER + 1), CELL_SIZE):  # +1 is because n can reach CELL_SIZE * BOARD_ORDER. Otherwise it cannot
            width = 1
            if n == MARGIN_X or n == MARGIN_X + CELL_SIZE * BOARD_ORDER:
                width = 2 
            pygame.draw.line(self.BOARD_IMG, (0, 0, 0), (MARGIN_X, n), (BOARD_WIDTH - MARGIN_X, n), width) # screen, color_rgb, start_point, end_point, width
            pygame.draw.line(self.BOARD_IMG, (0, 0, 0), (n, MARGIN_Y), (n, BOARD_HEIGHT - MARGIN_Y), width)
    
    def read_chessboard(self):
        cur_info = self.read(self.file_name)
        # self.ai_think_finshed_flag = cur_info['ai_think_finshed_flag']
        self.identify_finished_flag = cur_info['identify_finished_flag']
        self.timer = threading.Timer(1,self.read_chessboard)
        self.timer.start()
    
    def draw_pieces(self):
        if self.order < 1:  # skip if no piece 
            return 
        for i in range(1, self.order + 1):  #  drawing the BLACK pieces on the chessboard 
            piece_x, piece_y = self.PIECES_ON_BOARD[i -1]
            #x_, y_ = self.PIECES_ON_BOARD[i]         # get the position of the current piece on board 
            # judge black or white piece
            piece_img = self.BLACK_PIECES_IMG if CHESS_BOARD[piece_x][piece_y] == BLACK_PIECE else self.WHITE_PIECES_IMG
            color = COLOR1 if self.display_orders[i -1] is not self.last_piece else COLOR2
            self.DISPLAY.blit(piece_img,(MARGIN_X + MARGIN_X_BOARD + (piece_x -1) * CELL_SIZE,\
                                                    MARGIN_Y + MARGIN_Y_BOARD + (piece_y - 1) * CELL_SIZE))
            if self.display_orders[i - 1] < 10:    # one digit number 
                self.draw_text(color,str(self.display_orders[i -1]),\
                    piece_x * CELL_SIZE + MARGIN_X + 10 + 35, (piece_y - 1) * CELL_SIZE + MARGIN_Y + MARGIN_Y_BOARD + 5, self.display_orders[i - 1])
            elif 10 <= self.display_orders[i - 1] < 100: # two digit number 
                self.draw_text(color,str(self.display_orders[i -1]),\
                    piece_x * CELL_SIZE + MARGIN_X + 5 + 32, (piece_y - 1) * CELL_SIZE + MARGIN_Y + MARGIN_Y_BOARD + 6, self.display_orders[i - 1])
            elif self.display_orders[i - 1] >= 100: # three digit number 
                self.draw_text(color,str(self.display_orders[i -1]),\
                    piece_x * CELL_SIZE + MARGIN_X + 2, (piece_y - 1) * CELL_SIZE + MARGIN_Y + MARGIN_Y_BOARD + 6, self.display_orders[i - 1])                       
    
    def refresh(self, surface):
        """refresh [refresh the screen]

        :param surface: [the surface that is going to be refreshed]
        :type surface: [pygame.surface]
        """
        surface.fill((180, 140, 0))                                # fill the background color 
        surface.blit(self.TITLE_IMG, (MARGIN_X + 90, MARGIN_Y))    # put the title 
        surface.blit(self.BOARD_IMG, (MARGIN_X_BOARD, MARGIN_Y_BOARD))
        self.draw_pieces()
        self.quit_button.display()
        self.regret_button.display()
    
    def mouse_on_button(self, mouse_x, mouse_y):
        if self.quit_button.is_on_button([mouse_x,mouse_y]):       # if the mouse is on quit button 
           self.quit_button.change_color('GREEN')                  # green color is not suitable
        
        elif self.quit_button.is_on_button([mouse_x,mouse_y]) == False:
            self.quit_button.change_color('WHITE')
        
        if self.regret_button.is_on_button([mouse_x,mouse_y]):
            self.regret_button.change_color('GREEN') 
        elif self.regret_button.is_on_button([mouse_x,mouse_y]) == False:
            self.regret_button.change_color('WHITE')
            
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
            if self.is_balck_turn and CHESS_BOARD[x][y] is EMPTY_PIECE and self.game_end is False:    # chess piece can be added only when the cell 
                                                                              # is not occupied
                self.PIECES_ON_BOARD.append((x,y))                            # Add the coordinates of new balck pieces 
                self.BLACK_PIECES_ON_BOARD.append((x,y))
                print('Black pieces here:',x,' ',y)
                self.list3.append((x-1,y-1))
                self.list2.append((x-1,y-1))
                # print('BALCK',self.BLACK_PIECES_ON_BOARD)
                CHESS_BOARD[x][y] = BLACK_PIECE                               # Record the type of pieces
                self.is_balck_turn = False                                    # change the turn for white 
                self.is_white_turn = True 
                self.order = self.order + 1                                   # sequence number + 1
                self.display_orders.append(self.order)
                if win_judgment(CHESS_BOARD,(x,y),BLACK_PIECE):
                    self.game_end = True 
                    print('black win!')
 
        if self.quit_button.is_on_button([mouse_x,mouse_y]):   # if the quit button is pressed 
            self.running = False   # we must set self.running = False, otherwise error with pygame.fill can happen
            self.timer.cancel()    # release  the timer 
            pygame.quit()
        if self.regret_button.is_on_button([mouse_x,mouse_y]): # if the regret button is pressed
            black_piece = self.BLACK_PIECES_ON_BOARD.pop()
            white_piece = self.WHITE_PIECES_ON_BOARD.pop()
            CHESS_BOARD[black_piece[0]][black_piece[1]] = EMPTY_PIECE
            CHESS_BOARD[white_piece[0]][white_piece[1]] = EMPTY_PIECE
            self.PIECES_ON_BOARD.pop()
            self.PIECES_ON_BOARD.pop()
            self.list1.pop()
            self.list2.pop()
            self.list3.pop()
            self.list3.pop()
            if self.last_piece > 2:
                self.last_piece -= 2
            else:
                self.last_piece = 1
            if self.order > 2:
                self.order -= 2
            else:
                self.order = 0
            self.display_orders.pop()
            self.display_orders.pop()
            self.game_end = False
            self.is_balck_turn = True
            self.is_white_turn = False 
            print('successufully regret')
        # elif mouse_x and mouse_y: # this means the click happens in the control panel 
        #pass 
        
    def read(self,file_name):
        with open(file_name,'r') as json_file_handle:
            info = json.load(json_file_handle)
        return info
    
    def write(self,file_name,key,value):
        cur_info = self.read(file_name)
        cur_info[key] = value
        
        with open(file_name,'w') as json_file_handle:
            new_info = json.dumps(cur_info)
            json_file_handle.write(new_info)
            print('write successed')

    def Human(self):
        if self.identify_finished_flag:                            # means new pieces has been readed  
            cur_info = self.read(self.file_name) 
            human_new_step = cur_info['human_new_step']            # a turple contains new step (x,y)
            x,y = human_new_step[0], human_new_step[1]
            self.PIECES_ON_BOARD.append((x,y))
            self.BLACK_PIECES_ON_BOARD.append((x,y))
            self.list3.append((x-1,y-1))
            self.list2.append((x-1,y-1))
            CHESS_BOARD[x][y] = BLACK_PIECE
            self.order = self.order + 1 
            self.last_piece = self.order
            self.display_orders.append(self.order)
            if win_judgment(CHESS_BOARD,(x,y),WHITE_PIECE):
                self.game_end = True 
                print('You win!')
            self.is_white_turn = True 
            self.is_balck_turn = False
            self.identify_finished_flag = False
            # self.write(self.file_name,'cur_black_pos',self.BLACK_PIECES_ON_BOARD)
            self.write(self.file_name,'identify_finished_flag',False)

    def Robot(self):
        next_step = ai(self.list1,self.list2,self.list3,LIST_ALL)
        # print(next_step)
        x,y = next_step[0] + 1, next_step[1] + 1
        print('Robot set white pieces here:',x,' ',y)
        self.write(self.file_name,'ai_new_step',(x,y))             # record AI's new step in the info.json 
        self.write(self.file_name,'ai_think_finished_flag',True)    # AI has finished thinking
        self.PIECES_ON_BOARD.append((x,y))
        self.WHITE_PIECES_ON_BOARD.append((x,y))
        self.list3.append((x-1,y-1))
        self.list1.append((x-1,y-1))
        CHESS_BOARD[x][y] = WHITE_PIECE
        self.order = self.order + 1 
        self.last_piece = self.order
        self.display_orders.append(self.order)
        # self.draw_text(COLOR1,str(self.order),x,y)
        if win_judgment(CHESS_BOARD,(x,y),WHITE_PIECE):
            self.game_end = True 
            print('Sorry, robot win!')
        self.is_white_turn = False 
        self.is_balck_turn = True
        
    def draw_text(self, color, text, x, y, order):
        if order < 100:
            self.DISPLAY.blit(self.piece_font.render(text, True, color), (x, y))
        elif order >= 100:
            self.DISPLAY.blit(self.piece_font_2.render(text, True, color), (x, y))
            # print('yes')
        
    def run(self):
        while self.running:
            self.refresh(self.DISPLAY)
            pygame.display.update()

            if self.is_white_turn and self.game_end is False:
                self.Robot()
            
            if self.is_balck_turn and self.game_end is False:
                self.Human()
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_click(event.pos[0], event.pos[1])
                if event.type == pygame.MOUSEMOTION:
                    self.mouse_on_button(event.pos[0], event.pos[1])                    
                if event.type == pygame.QUIT:
                    self.RUNNING = False
                    pygame.quit()  # exit the game
            self.clock.tick(10)

        
# for demo test, this part will be moved to the interface in the feature       
if __name__ == '__main__':
    main = GoBang_GUI()
    main.run()
