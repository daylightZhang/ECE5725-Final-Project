# Step Motor driver
# We reference code from "2D plotter"
# Author: Lanyue Fang:(Soft: initialization, axis selection. Hard: physical connection)
#         Jingkai Zhang:(Soft: multiprocess. Hard: Cut wires and choose GPIO pins) 
# Date: 2021.11

import RPi.GPIO as GPIO
import time
import threading
from init import read_calibration_data
import numpy as np
import math

class Motor(object):
    def __init__(self):
        # initialize the GPIOs for step motor
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.y_axis_pins = [4, 5, 6, 17]
        self.x_axis_pins = [23, 24, 25, 18]
        self.z_axis_pins = [12, 16, 20, 21]
        self.unit_step_x = 193
        self.unit_step_y = 186
        self.unit_step_z= 62
        self.unit_pixel = 25
        self.cur_coordinate = [5,-1,1]     # current coordinate [x,y,z]
        self.origin_coordinate = [5,-1,1]   
        _,self.origin_position_pixel,_ = read_calibration_data() # get the calibration point

        # set as output GPIOs
        for pin in self.y_axis_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
        for pin in self.x_axis_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)
        for pin in self.z_axis_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, 0)

        self.seq = [[1, 0, 0, 0],
                   [1, 1, 0, 0],
                   [0, 1, 0, 0],
                   [0, 1, 1, 0],
                   [0, 0, 1, 0],
                   [0, 0, 1, 1],
                   [0, 0, 0, 1],
                   [1, 0, 0, 1], ]

        
    def __del__(self):
        GPIO.cleanup()

    def get_origin_coordinate(self):
        return self.origin_coordinate
    
    def set_cur_coordinate(self, value):
        self.cur_coordinate = value 
    
    def move(self, axis, blocks):
        print("ori pos",self.origin_coordinate)
        print("cur pos",self.cur_coordinate)
        if axis == 'x':
            pins = self.x_axis_pins
            step = round(abs(blocks) * self.unit_step_x)
            self.cur_coordinate[0] = self.cur_coordinate[0] + blocks * -1
        elif axis == 'y':
            pins = self.y_axis_pins
            step = round(abs(blocks) * self.unit_step_y)
            self.cur_coordinate[1] = self.cur_coordinate[1] + blocks
        else:
            pins = self.z_axis_pins
            step = round(abs(blocks) * self.unit_step_z)
            self.cur_coordinate[2] = self.cur_coordinate[2] + blocks

        for i in range(step):
            for halfstep in range(8):
                for pin in range(4):
                    if (blocks > 0):
                        GPIO.output(pins[pin], self.seq[halfstep][pin])
                    else:
                        GPIO.output(pins[pin], self.seq[7 - halfstep][pin])
                time.sleep(0.0008)
        print("ori pos",self.origin_coordinate)
        print("cur pos",self.cur_coordinate)
    
    def move_xy(self,move_distance,is_multiThread=False): # move_distance = [5,7] 5 is for x axis, 7 is for y axis
        if is_multiThread is True:
            thread_y = threading.Thread(target=self.move,args=('y',move_distance[1]))
            thread_x = threading.Thread(target=self.move,args=('x',move_distance[0]))
            thread_x.start()
            thread_y.start()
            
            thread_x.join()
            thread_y.join()
        else:
            self.move('x',move_distance[0])
            # time.sleep(1)
            self.move('y',move_distance[1])
            # time.sleep(1)
    
    def move_by_step(self,axis,step):
        step_value = int(abs(step))
        if axis == 'x':
            pins = self.x_axis_pins

        elif axis == 'y':
            pins = self.y_axis_pins

        for i in range(step_value):
            for halfstep in range(8):
                for pin in range(4):
                    if (step > 0):
                        GPIO.output(pins[pin], self.seq[halfstep][pin])
                    else:
                        GPIO.output(pins[pin], self.seq[7 - halfstep][pin])
                time.sleep(0.0008)
                
    def move_xy_by_step(self,move_step,is_multiThread=False):
        if is_multiThread is True:
            thread_y = threading.Thread(target=self.move_by_step,args=('y',move_step[1]))
            thread_x = threading.Thread(target=self.move_by_step,args=('x',move_step[0]))
            thread_x.start()
            thread_y.start()
            
            thread_x.join()
            thread_y.join()
        else:
            self.move_by_step('x',move_step[0])
            # time.sleep(1)
            self.move_by_step('y',move_step[1])
            # time.sleep(1)
    
    def move_by_coordinate(self, x_position, y_position):
        print('move_by_coordinate is executing!')
        dx_block = x_position - self.cur_coordinate[0]
        dy_block = y_position - self.cur_coordinate[1]
        dx_direction = -1 if dx_block > 0 else 1
        dy_direction = 1 if dy_block > 0 else -1
        print('x_pos:',x_position,' y_pos:',y_position)
        print('cur_pos:',self.cur_coordinate)
        print('dx_block:',dx_block,' dy_block:',dy_block)
        self.move('x', dx_direction * abs(dx_block))
        time.sleep(0.5)
        self.move('y', dy_direction * abs(dy_block))
        time.sleep(0.5)

