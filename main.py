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
import time, sys 
import json
import log

log = log.Log()                                               # create a logging to record the information of system 
log.info('GoBang starts now')
motor = Motor()                                               # initialize the step motor 
camera = Camera()                                             # initialize the pi camera 
if camera.is_cap_open == False:
    log.critical('Failed to load Pi Camera, program terminated')
    sys.exit(0)
pump = Pump()                                                 # initialize the pump 
log.info('Hardware has been initialized successfully.')

K_p = 2                                                       # set the pid control parameter
calibrate_threshold = 1.5                                     # threadhold value for calibration, small than this will not calibrate 
                                                              # this value is count as pixel, e.g. Now it is 1.5 pixels 

with open('cali_points.json','r') as json_file_handle:
    cali_points = json.load(json_file_handle)
log.info('calibration points have been loaded')
cur_black_pos = []
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
            in order to place the chess more accurately, motor position will be calibrated with the target position
            put the chess piece and go back to the origin point
        
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
    def place(self):
        target_coordinate = motor.target_coordinate.copy()
        if target_coordinate != motor.transition_coordinate:        # stil need to be moved 1-2 blocks 
            motor.move_by_coordinate(target_coordinate[0],target_coordinate[1])        
        log.debug('white(AI) stone has arrived at x-'+str(target_coordinate[0])+' y-'+str(target_coordinate[1]))   
        pump.release(motor)
        log.info('white(AI) has released the stone')
        log.debug('origin coordinate:'+str(motor.origin_coordinate[0])+' '+str(motor.origin_coordinate[1]))
        motor.move_by_coordinate(motor.origin_coordinate[0], motor.origin_coordinate[1])
        # calibrate
        motor.target_coordinate = [motor.origin_coordinate[0], motor.origin_coordinate[1]]
        motor.target_position_pixel = motor.origin_position_pixel.copy()
        log.debug('target coordinate:'+str(motor.target_position_pixel[0])+' '+str(motor.target_position_pixel[1]))
        flag_controller['calibrate_flag'] = True
        
    def locate(self):
        # AI calculate where the white chess should be placed, should know black.pieces
        # place the white chess and then go back to the calibration point (motor.origin_coordinate)
        cur_info = read('info.json')
        ai_new_step = cur_info['ai_new_step']                   # (x,y) starts from (1,1)
        motor.target_coordinate = ai_new_step
        target_coordinate_str = '('+ str(ai_new_step[0]) + ',' + str(ai_new_step[1])+')'
        log.debug('tar_coor_str = '+target_coordinate_str)
        motor.target_position_pixel = cali_points[target_coordinate_str]
        pump.pick(motor)
        log.info('white(AI) picked up a piece')
        [x,y] = motor.get_transition_coordinate()
        motor.move_by_coordinate(x, y)
        # calibrate
        flag_controller['calibrate_flag'] = True

white = White()

def calibrate(red_circle):
    if red_circle is None:
        # If no red_circle detected, return  
        log.error('Did not detect red circle, calibration failed.')
        # flag_controller['calibrate_flag'] = True              # Keep detecting red circles 
        return 
    else:
        flag_controller['calibrate_flag'] = False             # disenable this flag in order not to open 2 same thread
        log.info('Coordinate of red circle: x-'+str(red_circle[0])+' y-'+str(red_circle[1]))
        move_step = [0,0]                                     # list to store the move steps 
        target_position = motor.target_position_pixel.copy()
        cur_position = [red_circle[0],red_circle[1]]          # get the center coordinates of red circle  
        dx = target_position[0] - cur_position[0]             # compute the distance difference in x-axis 
        dy = target_position[1] - cur_position[1]             # compute the distance difference in y-axis 
        output_step_x = K_p * dx                              # PID control, calculate the output step for control step motor 
        output_step_y = K_p * dy                              # output control for y axis 

        log.info('cur_pos: x-'+str(cur_position[0])+' y-'+str(cur_position[1]) + \
                 ' target_pos: x-'+str(target_position[0])+' y-'+str(target_position[1]))
        dx_direction = -1 if dx > 0 else 1                    # set the rorating direction for x-axis 
        dy_direction = 1 if dy > 0 else -1                    # set the rorating direction for y-axis 
        move_step[0] = dx_direction * abs(output_step_x)      # x-axis 
        move_step[1] = dy_direction * abs(output_step_y)      # y-axis 
        motor.move_xy_by_step(move_step,False)                # multipleprocess = False, which could be set as true 

        flag_controller['calibrate_check_flag'] = True        # enable calibration check 
        
def calibrate_check():
    red_circle = camera.detect_red_circle()
    if red_circle is None:
        log.error('Did not detect red circle, calibration check failed.')
        return 
    flag_controller['calibrate_check_flag'] = False           # after check, disenable
    check_dx = abs(motor.target_position_pixel[0] - red_circle[0])
    check_dy = abs(motor.target_position_pixel[1] - red_circle[1])
    if check_dx > calibrate_threshold or check_dy > calibrate_threshold:
        flag_controller['calibrate_flag'] = True 
        log.info('calibration error is still big, continue calibrating')
        log.info('error_x:'+str(check_dx)+' error_y:'+str(check_dy))
    else:
        # motor.cur_coordinate = motor.origin_coordinate.copy()
        '''
            [Solved] Bug description
            list cannot be assigned by '=', it will result in the same address 
        '''
        log.info('calibration succeed')
        
        if motor.target_coordinate == [5,-1]:
            log.info('waiting for human to place chess stone')
            # print('check_dx = ',check_dx,' check_dy = ',check_dy)
            # flag_controller['calibration_finished_flag'] = True   # means picker has been in calibration point 
            #                                                       # Now should wait for human 
        else:
            thread_white_place = threading.Thread(target=white.place)  
            thread_white_place.start()
        
    
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
        # print('write successed')   
        
def btn27_call_back(btn):
    # print('button ',btn,' is pressed!')
    log.info('Human\'s turn has finished, now turn to AI')
    flag_controller['identify_flag'] = True # use a physical button to indicate human has finished   

def identify_black_step():
    flag_controller['identify_flag'] = False
    resize_img = cv2.resize(camera.chess_img, (270,270))            # adjust the size of chessboard image 
    gray_img = cv2.cvtColor(resize_img, cv2.COLOR_BGR2GRAY)
    _, black_stones = cv2.threshold(gray_img, 60, 255, cv2.THRESH_BINARY)
    kernel = np.ones((30,30))                                       # a 30x30 all one matrix
    
    for i in range(9):                                              # 9 rows 
        for j in range(9):                                          # 9 colomns
            block = black_stones[i*30:(i+1)*30,j*30:(j+1)*30]       # in opencv, we express in this way (y,x)
            check_matrix = block * kernel
            # print('row:',i,' col:',j,' sum=',check_matrix.sum())
            if check_matrix.sum() <= 150000:
                if (j+1,i+1) not in cur_black_pos:
                    new_black_step = (j + 1, i + 1)                 # detect new added black pieces 
                    cur_black_pos.append(new_black_step)
                    log.info('Identified new black stone position on board: x-'+str(j+1)+' y-'+str(i+1))
                    # record the new human(black) step in the info.json
                    write('info.json','human_new_step',new_black_step)
                    break
                                         
                # log.debug('black stone pos: x-'+str(j+1)+' y-'+str(i+1)+'check_sum: '+str(check_matrix.sum()))

    write('info.json','identify_finished_flag',True)
    # global read_flag_timer
    # read_flag_timer.start()  # start the timer 
    # return num_black_stone 

def read_ai_finished_flag():
    global read_flag_timer
    cur_info = read('info.json')
    ai_think_finished_flag = cur_info['ai_think_finished_flag']
    if ai_think_finished_flag:
        write('info.json','ai_think_finished_flag',False)
        log.info('white(AI) has finished thinking')
        thread_white_locate = threading.Thread(target=white.locate)
        thread_white_locate.start()
    
    read_flag_timer = threading.Timer(1,read_ai_finished_flag)
    read_flag_timer.start()

def init_flags():
    write('info.json','identify_finished_flag',False)
    write('info.json','ai_think_finished_flag',False)
    log.info('Control flags has been initialized')

def main():
    init_flags()
    RUNNING = True 
    button = 27                                               # set the GPIO for button
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)     # configure the GPIO
    GPIO.add_event_detect(button, GPIO.RISING, \
                          callback=btn27_call_back,\
                            bouncetime=200)                   # dectecting the botton using interrupt
    global read_flag_timer
    read_flag_timer = threading.Timer(1,read_ai_finished_flag)
    read_flag_timer.start()
    log.info('Start the flag reading timer')
    log.info('Waiting for human to place chess stone')
    
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
            '''
                detect_red_circle() returns the current red circle center position (x,y), regarded as actual_pos
                target_pos is stored in the motor class
                for going back, target_pos should be the origin point 
                for puting white stone, target_pos should be selected from a list 
            '''
            thread_calibrate = threading.Thread(target=calibrate, args=(camera.detect_red_circle(),))  
            thread_calibrate.start()
          
        if flag_controller['calibrate_check_flag']:           # if calibrate_check_flag is True 
            calibrate_check()
        # wait for human's next step 
        # identify human's next step with camera 
        
        if flag_controller['identify_flag']:              # if human_finish_step is True
            '''
                Note: The 'identify_flag' is triggered by a physical button 
                After human finish, the new step should be detected and recorded 
            '''
            thread_black_stone = threading.Thread(target=identify_black_step)  
            thread_black_stone.start()
        
        # go back to calibration point 
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    
    read_flag_timer.cancel()
    log.info('Main program ended')

if __name__ == '__main__':
    main()
