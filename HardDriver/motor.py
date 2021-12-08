# Step Motor driver
# We reference code from "2D plotter"
# Author: Lanyue Fang:(Soft: initialization, axis selection. Hard: physical connection)
#         Jingkai Zhang:(Soft: multiprocess. Hard: Cut wires and choose GPIO pins) 
# Date: 2021.11

import RPi.GPIO as GPIO
import time
import threading

class Motor(object):
    def __init__(self):
        # initialize the GPIOs for step motor
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.y_axis_pins = [4, 5, 6, 17]
        self.x_axis_pins = [23, 24, 25, 18]
        self.z_axis_pins = [12, 16, 20, 21]
        self.unit_step= 193 # 186 
        self.unit_step_z= 34

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

        self.cur_coordinate = [0,0,0]     # current coordinate [x,y,z]
        self.origin_coordinate = [0,0,0]  # used for calibration

    def __del__(self):
        GPIO.cleanup()

    def move(self, axis, blocks):
        if axis == 'x':
            pins = self.x_axis_pins
            step = round(abs(blocks) * self.unit_step_x)
            self.cur_coordinate[0] = self.cur_coordinate[0] + blocks
        elif axis == 'y':
            pins = self.y_axis_pins
            step = round(abs(blocks) * self.unit_step_y)
            self.cur_coordinate[1] = self.cur_coordinate[1] + blocks
        else:
            pins = self.z_axis_pins
            step = round(abs(blocks) * self.unit_step_z)
            self.cur_coordinate[2] = self.cur_coordinate[2] + blocks

        step = int(step)
        for i in range(step):
            for halfstep in range(8):
                for pin in range(4):
                    if (blocks > 0):
                        GPIO.output(pins[pin], self.seq[halfstep][pin])
                    else:
                        GPIO.output(pins[pin], self.seq[7 - halfstep][pin])
                time.sleep(0.0008)
    
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
    

