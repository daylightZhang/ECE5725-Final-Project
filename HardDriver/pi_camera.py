# Pi Camera Driver
# Author: Lanyue Fang:(Soft: design the red_dot_track algorithm, image preprocess algorithm)
#         Jingkai Zhang:(Soft: design the framework of class, view correction. Hard: fixed it on frame, installation) 
# Date: 2021.11

import cv2  
from init import read_calibration_data

class Camera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)                                       # get the video steam 
        self.is_cap_open = self.cap.isOpened()                               # check if the camera is open 
        self.box, self.chess_box, self.cali_point = read_calibration_data()  # read the calibration data
    
    def __del__(self):
        self.cap.release()                                                   # release the camera 
    
    def detect_red_dot(self):
        pass  
    
    def get_chessboard_area(self):
        pass 
    
    def get_whole_area(self):
        pass 
     