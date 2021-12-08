# Pi Camera Driver
# Author: Lanyue Fang:(Soft: design the red_dot_track algorithm, image preprocess algorithm)
#         Jingkai Zhang:(Soft: design the framework of class, view correction. Hard: fixed it on frame, installation) 
# Date: 2021.11

import cv2  
import math
import numpy as np
import sys
from init import read_calibration_data

class Camera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture(0)                                       # get the video steam 
        self.is_cap_open = self.cap.isOpened()                               # check if the camera is open 
        self.whole_box, self.chess_box, self.cali_point = \
                                                    read_calibration_data()  # read the calibration data
    
    def __del__(self):
        self.cap.release()                                                   # release the camera 
    
    def camera_update(self):
        ret, self.frame = self.cap.read()
    
    def get_camera_view(self):
        # ret, self.frame = self.cap.read()
        # if ret is False:
        #     print('camera seems not open, check the pi camera first!')
        #     sys.exit(0)
        return self.frame

    def get_camera_open_flag(self):
        return self.is_cap_open                                              # return True if camera is opened
        
    def get_box(self,box_name='whole'):
        if box_name is 'whole': 
            return self.whole_box
        elif box_name is 'chess':
            return self.chess_box
        else:
            print('Please assign a valid name for box')                      # could be 'whole' or 'chess'
            return 
  
    def get_calibration_point(self):
        return self.cali_point
    
    def get_whole_area(self):
        return self.whole_img
    
    def get_chessboard_area(self):
        return self.chess_img
    
    def show(self,name,figure):
        cv2.imshow(name,figure)
  
    def img_preprocess(self):
        self.frame = cv2.resize(self.frame)
        self.whole_img = np.rot90(self.perspective_transform(self.whole_box,self.frame))
        self.chess_img = np.rot90(self.perspective_transform(self.chess_box,self.frame))
        self.grayImg = cv2.cvtColor(self.whole_img, cv2.COLOR_BGR2GRAY)
        self.hsvImg = cv2.cvtColor(self.whole_img, cv2.COLOR_BGR2HSV)
        red_lo = np.array([170, 125, 125])                                  # lower limit for red color
        red_hi = np.array([179, 255, 255])                                  # higher limit for red color
        self.red_region = cv2.inRange(self.hsvImg, red_lo, red_hi)          # filter the red area 
        kernel_1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
        kernel_2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        self.red_region_1 = cv2.erode(self.red_region_1, kernel_1)
        self.red_region_1 = cv2.dilate(self.red_region_1, kernel_1)
        self.red_region_2 = cv2.dilate(self.red_region_1, kernel_2)
        self.red_region_2 = cv2.erode(self.red_region_2, kernel_2)
        self.red_circles = []
        
    def perspective_transform(self,box,origin_img):
        # get the original width and height
        orignal_W = math.ceil(np.sqrt((box[3][1] - box[2][1]) ** 2 + (box[3][0] - box[2][0]) ** 2))
        orignal_H = math.ceil(np.sqrt((box[3][1] - box[0][1]) ** 2 + (box[3][0] - box[0][0]) ** 2))

        # using the 4 points from box to construct transform matrix 
        pts1 = np.float32([box[0], box[1], box[2], box[3]])
        pts2 = np.float32(
            [[int(orignal_W + 1), int(orignal_H + 1)], [0, int(orignal_H + 1)], [0, 0], [int(orignal_W + 1), 0]])

        # transform by using built-in function from opencv
        M = cv2.getPerspectiveTransform(pts1, pts2)
        result_img = cv2.warpPerspective(origin_img, M, (int(orignal_W + 3), int(orignal_H + 1)))

        return result_img
    
    def detect_red_dot(self):
        pass  
    