# Step Motor driver
# Author: Lanyue Fang:(Soft: initialization, axis selection. Hard: physical connection)
#         Jingkai Zhang:(Soft: multiprocess Hard: Cut wires and choose GPIO pins) 
# Date: 2021.11

import RPi.GPIO as GPIO
import time

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


    def move(self, axis, blocks,step=None):

        if step is not None:
            print('use mannul step value')
            step = step 
                
            pins = self.y_axis_pins
            # step = round(abs(blocks) * self.unit_step)
            self.cur_coordinate[0] = self.origin_coordinate[1] + blocks
        else:
            if axis == 'x':
                pins = self.x_axis_pins
                step = round(abs(blocks) * self.unit_step)
                self.cur_coordinate[0] = self.origin_coordinate[0] + blocks
                # print('x moving')
            elif axis == 'y':
                pins = self.y_axis_pins
                step = round(abs(blocks) * self.unit_step)
                self.cur_coordinate[1] = self.origin_coordinate[1] + blocks
            else:
                print('z is movinng')
                pins = self.z_axis_pins
                step = round(abs(blocks) * self.unit_step_z)
                self.cur_coordinate[2] = self.origin_coordinate[2] + blocks
        # print('step=',step)
        # print('type=',type(step))

            
        print(step)
        for i in range(step):
            for halfstep in range(8):
                for pin in range(4):
                    if (blocks > 0):
                        
                        GPIO.output(pins[pin], self.seq[halfstep][pin])
                    else:
                        
                        GPIO.output(pins[pin], self.seq[7 - halfstep][pin])
                time.sleep(0.0008)
    def move_xy(self,move_distance): # move_distance = [5,7] 5 is for x axis, 7 is for y axis
        # thread_y = threading.Thread(target=self.move,args=('y',move_distance[1]))
        # thread_x = threading.Thread(target=self.move,args=('x',move_distance[0]))
        # thread_x.start()
        # thread_y.start()
        
        # thread_x.join()
        # thread_y.join()
        
        self.move('x',move_distance[0])
        time.sleep(1)
        self.move('y',move_distance[1])
        time.sleep(1)

