# main program for the project 
# Author: Jingkai Zhang (jz544@cornell.edu) and Lanyue Fang (lf355@cornell.edu)
# Date: 2021.12.8
import threading
import RPi.GPIO as GPIO  
# from GoBang.GUI import GoBang_GUI # display should be written in another file 
from HardDriver.motor import Motor
from HardDriver.pi_camera import Camera
from HardDriver.pump import Pump
import time, datetime
import logging
import matplotlib.pyplot as plt

motor = Motor()      # initialize the step motor 
camera = Camera()    # initialize the pi camera 
pump = Pump()        # initialize the pump 

def PID_calibration():
    RUNNING = True   
    # start_time = time.time()
    '''
        Note:
            In our real application, 190 steps corresponds to 25 unit distance 
    '''
    init_position = 200
    cur_position, _ = camera.get_red_dot()        # get x-axis coordinate
    target_position = 100                         # set target position for x-axis 
    cur_pos = []                                  # used for plot figure
    cur_pos.append(cur_position)
    K_p = 2                                    # set the proportion control parameter

    error = 0

    while RUNNING:
        output_step = K_p * error
        # update the current position
        # cur_position = 25 * output_step / 190.0 + cur_position # ideal  
        # cur_position = 25 * output_step / 190.0 + cur_position + random.random()
        # print('output_step = ',output_step)
        # cur_position = input('enter cur_position:')
        # cur_position = float(cur_position)
        photo = camera.get_current()
        cur_position, _ = camera.get_red_dot()
        cur_pos.append(cur_position)
        # print(random.random())
        error = target_position - cur_position    # compute error
                                                  
        if -2 <= error <= 2 or cur_position >= 1500:
            break

        print('cur_position = ',cur_position,' error = ',error,' step = ',output_step)
        # time.sleep(1)

    print('stable position = ',cur_position,' stable error = ',error)

    y = cur_pos
    x = range(len(y))
    plt.plot(x,y)
    plt.show()

def main():
    RUNNING = True 
    
    PID_calibration()
    
    # while RUNNING:
        
    #     pass 

if __name__ == '__main__':
    main()