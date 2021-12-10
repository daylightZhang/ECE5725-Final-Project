# # main program for the project 
# # Author: Jingkai Zhang (jz544@cornell.edu) and Lanyue Fang (lf355@cornell.edu)
# # Date: 2021.12.8
# import threading
# import RPi.GPIO as GPIO
# import cv2
# import numpy as np
# # from GoBang.GUI import GoBang_GUI # display should be written in another file 
# from HardDriver.motor import Motor
# from HardDriver.pi_camera import Camera
# from HardDriver.pump import Pump
# import time

# motor = Motor()                                               # initialize the step motor 
# camera = Camera()                                             # initialize the pi camera 
# pump = Pump()                                                 # initialize the pump 
# K_p = 2                                                       # set the pid control parameter
# calibrate_threshold = 1.5                                     # threadhold value for calibration, small than this will not calibrate 
#                                                               # this value is count as pixel, e.g. Now it is 1.5 pixels 
# # create a dictionary for flag control
# flag_controller = {'calibrate_flag':False,'calibrate_check_flag':False,\
#                    'identify_flag':False,'turn_to_AI':False,\
#                    'move_piece_flag':False,'human_finish_step':False}

# def calibrate(red_circle):
#     if red_circle is None:                                    # If no red_circle detected, return  
#         print('No red circle detected! Try red_region_track.py')
#         return 
#     else: 
#         flag_controller['calibrate_flag'] = False             # disenable this flag in order not to open 2 same thread
#         move_step = []                                        # list to store the move steps 
#         target_position = motor.origin_coordinate
#         cur_position = [red_circle[0],red_circle[1]]          # get the center coordinates of red circle  
#         dx = target_position[0] - cur_position[0]             # compute the distance difference in x-axis 
#         dy = target_position[1] - cur_position[1]             # compute the distance difference in y-axis 
#         output_step_x = K_p * dx                              # PID control, calculate the output step for control step motor 
#         output_step_y = K_p * dy                              # output control for y axis 
#         dx_direction = -1 if dx > 0 else 1                    # set the rorating direction for x-axis 
#         dy_direction = 1 if dy > 0 else -1                    # set the rorating direction for y-axis 
#         print('target_position = ',target_position,' cur_position = ', cur_position,\
#               ' error_x = ', dx, ' error_y = ', dy, ' step_x = ', output_step_x,\
#               ' step_y = ', output_step_y)
#         move_step[0] = dx_direction * abs(output_step_x)      # x-axis 
#         move_step[1] = dy_direction * abs(output_step_y)      # y-axis 
#         motor.move_xy_by_step(move_step,False)                # multipleprocess = False, which could be set as true 
#         flag_controller['calibrate_check_flag'] = True        # enable calibration check 
        
# def calibrate_check():
#     red_circle = camera.detect_red_circle()
#     check_dx = abs(motor.origin_position_pixel[0] - red_circle[0])
#     check_dy = abs(motor.origin_position_pixel[1] - red_circle[1])
#     if check_dx > calibrate_threshold or check_dy > calibrate_threshold:
#         red_circle_flag = 1                                   # ???? What is this flag used for  
#         flag_controller['calibrate_flag'] = True 
#         print("still need calibrate")
#         print('check_dx = ',check_dx,' check_dy = ',check_dy)
#     else:
#         print("calibrate succeeded")
#         print('check_dx = ',check_dx,' check_dy = ',check_dy)
#     flag_controller['calibrate_check_flag'] = False           # after check, disenable
    
# def btn27_call_back(btn):
#     print('button ',btn,' is pressed!')
#     flag_controller['human_finish_step'] = True               # use a physical button to indicate human has finished   

# def identify_black_step():
#     resize_img = cv2.resize(camera.chess_img, (270,270))      # adjust the size of chessboard image 
#     gray_img = cv2.cvtColor(resize_img, cv2.COLOR_BGR2GRAY)
#     # blurred = cv2.GaussianBlur(gray_img, (9, 9), 0)
#     _, black_stones = cv2.threshold(gray_img, 60, 255, cv2.THRESH_BINARY)
#     # hls_img = cv2.cvtColor(resize_img, cv2.COLOR_BGR2HSV)
#     # mask = cv2.inRange(resize_img, np.array([160,170,190]), np.array([255,255,255]))
#     kernel = np.ones((30,30))                                 # a 30x30 all one matrix
#     position = np.zeros((9,9))                                # a 9x9 all zero matirix to indicate the position of black pieces
#     num_black_stone = 0
#     for i in range(9):                                        # 9 rows 
#         for j in range(9):                                    # 9 colomns
#             block = black_stones[i*30:(i+1)*30,j*30:(j+1)*30] # in opencv, we express in this way (y,x)
#             check_matrix = block * kernel
#             # print('row:',i,' col:',j,' sum=',check_matrix.sum())
#             if check_matrix.sum() <= 180000:
#                 num_black_stone += 1
#                 position[i][j] = 1                            # 1 indicate black stone 
#                 print('black stone ','row:',i+1,' col:',j+1,' sum=',check_matrix.sum())
#     print('number of black stone is ',num_black_stone)
#     return black_stones 

# def place_white_chess(x_position, y_position,multiprocess=False):
#     dx_block = x_position - motor.origin_coordinate[0]
#     dy_block = y_position - motor.origin_coordinate[1]
#     dx_direction = -1 if dx_block > 0 else 1
#     dy_direction = 1 if dy_block > 0 else -1
#     pump.pick(motor)
#     if multiprocess is False:
#         motor.move('x', dx_direction * abs(dx_block))
#         time.sleep(1)
#         motor.move('y', dy_direction * abs(dy_block))
#         time.sleep(1)
#     else: 
#         motor.move_xy([dx_direction * abs(dx_block),\
#                        dy_direction * abs(dy_block)],True)
        
#     pump.release(motor)
#     if multiprocess is False:
#         motor.move('x', -1 * dx_direction * abs(dx_block))
#         time.sleep(1)
#         motor.move('y', -1 * dy_direction * abs(dy_block))
#         time.sleep(1)
#     else:
#         motor.move_xy([-1 * dx_direction * abs(dx_block),\
#                        -1 * dy_direction * abs(dy_block)],True)
#     flag_controller['calibrate_flag'] = True                  # start the calibration

# def main():
#     RUNNING = True 
#     button = 27                                               # set the GPIO for button
#     GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)     # configure the GPIO
#     GPIO.add_event_detect(button, GPIO.RISING, \
#                           callback=btn27_call_back,\
#                             bouncetime=200)                   # dectecting the botton using interrupt
#     while RUNNING:
#         camera.camera_update()                                # update the camera
#         camera.img_preprocess()                               # preprocess the image
#         camera.show('Camera Preview',camera.frame)            # camera preview
#         # calibration 
#         if flag_controller['calibrate_flag']:                 # if calibrate_flag is True
#             # start a thread to calibrate 
#             thread_calibrate = threading.Thread(target=calibrate, args=(camera.red_circles,))  
#             thread_calibrate.start()
                                
#         if flag_controller['calibrate_check_flag']:           # if calibrate_check_flag is True 
#             calibrate_check()
#         # wait for human's next step 
#         # identify human's next step with camera 
#         if flag_controller['human_finish_step']:              # if human_finish_step is True
#             '''
#                 Note: The 'human_finish_step' is triggered by a physical button 
#                 After human finish, the new step should be detected and recorded 
#                 A function should be developed here 
#                 identify_new_step()
#             '''
#             black_stones = identify_black_step()
#             camera.show('Identified black stones',black_stones)
        
#         # generate AI's step 
#         if flag_controller['turn_to_AI']:                     # if turn_to_AI is True
#             '''
#                 Generate AI step, this part should be finished in gobang program
#             '''
#             pass
#         # move the piece to the designed position 
#         if flag_controller['move_piece_flag']:                # if move_piece_flag is True
#             # place_white_chess(1,2,True)                     # this function could be called 
#             pass 
#         # go back to calibration point 
        
#         if cv2.waitKey(25) & 0xFF == ord('q'):
#             break

# if __name__ == '__main__':
#     main()


# main program for the project 
# Author: Jingkai Zhang (jz544@cornell.edu) and Lanyue Fang (lf355@cornell.edu)
# Date: 2021.12.8
import threading
import RPi.GPIO as GPIO
import cv2
import numpy as np
# from GoBang.GUI import GoBang_GUI # display should be written in another file 
from HardDriver.motor import Motor
from HardDriver.pi_camera import Camera
from HardDriver.pump import Pump
import time
import json


motor = Motor()                                               # initialize the step motor 
camera = Camera()                                             # initialize the pi camera 
pump = Pump()                                                 # initialize the pump 
# goBangGUI = GoBang_GUI()
K_p = 2                                                       # set the pid control parameter
calibrate_threshold = 1.5                                     # threadhold value for calibration, small than this will not calibrate 
                                                              # this value is count as pixel, e.g. Now it is 1.5 pixels 
# create a dictionary for flag control
flag_controller = {'calibrate_flag':False,'calibrate_check_flag':False,\
                   'identify_flag':False,'turn_to_AI':False,\
                   'move_piece_flag':False,'human_finish_step':False}
"""
    the logic of the main program is as follow:
    
    initialization:
        calibrate_flag = False
        calibrate_check_flag = False
        identify_flag = False           (not used) 
        human_finish_step = False 
        identify_finished_flag = False  (written in info.json)
        ai_think_finshed_flag = False  (written in info.json)
    
    begin: 
        wait human_finish_step to become True (triggered by physical button)
        
        if human_finish_step is True
            identify_black_chess()
            
        wait identify_finished_flag to become True (triggered by function identify_black_chess())
        
        if identify_finished_flag is True 
            display and generate AI step (Show in Pygame)
            
        wait ai_think_finshed_flag to become True (triggered by GUI.py)

        if ai_think_finshed_flag is True 
            read the new_position from info.json
            ai_think_finshed_flag = False 
            move chess piece to the target position  (start with a thread)
        
        wait calibrate_flag to become True 
        
        if calibrate_flag is True 
            calibrate()
            calibrate_check_flag = True 
        
        if calibrate_check_flag is True 
            calibrate_check() 
            calibrate_flag = True if the error is acceptable, otherwise False 
        
"""

class White(object):
    def __init__(self):
        self.pieces = []
    def __del__(self):
        pass
    def place(self,x_coordinate, y_coordinate):
        pump.pick(motor)
        motor.move_by_coordinate(x_coordinate, y_coordinate)
        pump.release(motor)
        motor.move_by_coordinate(motor.origin_coordinate[0], motor.origin_coordinate[1])
    def play(self):
        # AI calculate where the white chess should be placed, should know black.pieces
        # place the white chess and then go back to the calibration point (motor.origin_coordinate)
        self.place(0, 9)
        # calibrate
        flag_controller['calibrate_flag'] = True

white = White()

def calibrate(red_circle):
    flag_controller['calibrate_flag'] = False
    print('red_circle = ',red_circle)
    if red_circle is None:
        # If no red_circle detected, return  
        print('No red circle detected! Try red_region_track.py')
        return 
    else:
        flag_controller['calibrate_flag'] = False             # disenable this flag in order not to open 2 same thread
        move_step = [0,0]                                        # list to store the move steps 
        target_position = motor.origin_position_pixel
        cur_position = [red_circle[0],red_circle[1]]          # get the center coordinates of red circle  
        dx = target_position[0] - cur_position[0]             # compute the distance difference in x-axis 
        dy = target_position[1] - cur_position[1]             # compute the distance difference in y-axis 
        output_step_x = K_p * dx                              # PID control, calculate the output step for control step motor 
        output_step_y = K_p * dy                              # output control for y axis 

        print('target_position = ',target_position,' cur_position = ', cur_position,\
              ' error_x = ', dx, ' error_y = ', dy, ' step_x = ', output_step_x,\
              ' step_y = ', output_step_y)
        dx_direction = -1 if dx > 0 else 1                    # set the rorating direction for x-axis 
        dy_direction = 1 if dy > 0 else -1                    # set the rorating direction for y-axis 
        move_step[0] = dx_direction * abs(output_step_x)      # x-axis 
        move_step[1] = dy_direction * abs(output_step_y)      # y-axis 
        motor.move_xy_by_step(move_step,False)                # multipleprocess = False, which could be set as true 

        # motor.move_by_step('y', abs(output_step_y))
        # motor.move_by_step('x', abs(output_step_x))
        
        flag_controller['calibrate_check_flag'] = True        # enable calibration check 
        
def calibrate_check():
    red_circle = camera.detect_red_circle()
    check_dx = abs(motor.origin_position_pixel[0] - red_circle[0])
    check_dy = abs(motor.origin_position_pixel[1] - red_circle[1])
    if check_dx > calibrate_threshold or check_dy > calibrate_threshold:
        flag_controller['calibrate_flag'] = True 
        print("still need calibrate")
        print('check_dx = ',check_dx,' check_dy = ',check_dy)
    else:
        motor.cur_coordinate = motor.origin_coordinate
        print("calibrate succeeded")
        print('check_dx = ',check_dx,' check_dy = ',check_dy)
        flag_controller['calibration_finished_flag'] = True   # means picker has been in calibration point 
                                                              # Now should wait for human 
    flag_controller['calibrate_check_flag'] = False           # after check, disenable
    
def read(file_name):
    with open(file_name,'r') as json_file_handle:
        info = json.load(json_file_handle)
    return info

def write(file_name,key,value):
    cur_info = read(file_name)
    cur_info[key] = value
    
    with open(file_name,'w') as json_file_handle:
        new_info = json.dumps(cur_info)
        json_file_handle.write(new_info)
        print('write successed')   
        
def btn27_call_back(btn):
    print('button ',btn,' is pressed!')
    flag_controller['identify_flag'] = True # use a physical button to indicate human has finished   

def identify_black_step():
    flag_controller['identify_flag'] = False
    resize_img = cv2.resize(camera.chess_img, (270,270))      # adjust the size of chessboard image 
    gray_img = cv2.cvtColor(resize_img, cv2.COLOR_BGR2GRAY)
    _, black_stones = cv2.threshold(gray_img, 60, 255, cv2.THRESH_BINARY)
    kernel = np.ones((30,30))                                 # a 30x30 all one matrix
    cur_info = read('info.json')
    cur_black_pos = cur_info['cur_black_pos']                 # current black pieces on the board 

    for i in range(9):                                        # 9 rows 
        for j in range(9):                                    # 9 colomns
            block = black_stones[i*30:(i+1)*30,j*30:(j+1)*30] # in opencv, we express in this way (y,x)
            check_matrix = block * kernel
            # print('row:',i,' col:',j,' sum=',check_matrix.sum())
            if check_matrix.sum() <= 150000:
                if (i+1,j+1) not in cur_black_pos:
                    new_black_step = (i + 1, j + 1)           # detect new added black pieces 
                    print('new_black_step = ',new_black_step)
                    # record the new human(black) step in the info.json
                    write('info.json','human_new_step',new_black_step)
                    break
                                         
                print('black stone ','row:',i+1,' col:',j+1,' sum=',check_matrix.sum())
    
    thread_white = threading.Thread(target=white.play)
    thread_white.start()
    
    # return num_black_stone 

def place_white_chess(x_position, y_position,multiprocess=False):
    dx_block = x_position - motor.origin_coordinate[0]
    dy_block = y_position - motor.origin_coordinate[1]
    dx_direction = -1 if dx_block > 0 else 1
    dy_direction = 1 if dy_block > 0 else -1
    pump.pick(motor)
    if multiprocess is False:
        motor.move('x', dx_direction * abs(dx_block))
        time.sleep(1)
        motor.move('y', dy_direction * abs(dy_block))
        time.sleep(1)
    else: 
        motor.move_xy([dx_direction * abs(dx_block),\
                       dy_direction * abs(dy_block)],True)
        
    pump.release(motor)
    if multiprocess is False:
        motor.move('x', -1 * dx_direction * abs(dx_block))
        time.sleep(1)
        motor.move('y', -1 * dy_direction * abs(dy_block))
        time.sleep(1)
    else:
        motor.move_xy([-1 * dx_direction * abs(dx_block),\
                       -1 * dy_direction * abs(dy_block)],True)
    flag_controller['calibrate_flag'] = True                  # start the calibration

def main():
    RUNNING = True 
    button = 27                                               # set the GPIO for button
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)     # configure the GPIO
    GPIO.add_event_detect(button, GPIO.RISING, \
                          callback=btn27_call_back,\
                            bouncetime=200)                   # dectecting the botton using interrupt
    # Thread_GoBangGUI = threading.Thread(target=run_goBang)    # display the GUI of goBang
    # Thread_GoBangGUI.setDaemon(True)
    # Thread_GoBangGUI.start()                                  # start the GUI of goBang
    while RUNNING:
        camera.camera_update()                                # update the camera
        # camera preview
        camera.show('Camera Preview',camera.get_img())  
        # chessboard preview 
        camera.show('chessboard preview', camera.get_chessboard_area())          
        camera.show('red region',camera.red_region)
        # calibration 
        if flag_controller['calibrate_flag']:                 # if calibrate_flag is True
            # start a thread to calibrate 
            thread_calibrate = threading.Thread(target=calibrate, args=(camera.detect_red_circle(),))  
            thread_calibrate.start()
            pass                 
        if flag_controller['calibrate_check_flag']:           # if calibrate_check_flag is True 
            calibrate_check()
            pass 
        # wait for human's next step 
        # identify human's next step with camera 
        
        if flag_controller['identify_flag']:              # if human_finish_step is True
            '''
                Note: The 'identify_flag' is triggered by a physical button 
                After human finish, the new step should be detected and recorded 
            '''
            flag_controller['identify_flag'] = False 
            thread_black_stone = threading.Thread(target=identify_black_step)  
            thread_black_stone.start()
            identify_black_step()
            # camera.show('Identified black stones',black_stones)
        
        # generate AI's step 
        if flag_controller['turn_to_AI']:                     # if turn_to_AI is True
            '''
                Generate AI step, this part should be finished in gobang program
            '''
            pass
        # move the piece to the designed position 
        if flag_controller['move_piece_flag']:                # if move_piece_flag is True
            # place_white_chess(1,2,True)                     # this function could be called 
            pass 
        # go back to calibration point 
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    main()