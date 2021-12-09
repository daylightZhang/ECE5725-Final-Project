# calibration for picker 
# Author: Jingkai Zhang & Lanyue Fang
# Date: 2021.11.29
import cv2 
import json 
import numpy as np
import math

def save_calibration_data(data,file_name='calibration.json'):
    json_str = json.dumps(data)
    with open(file_name, 'w+') as json_file_handle:
        json_file_handle.write(json_str)
    print('file has been saved.')

def read_calibration_data(file_name='calibration.json'):
    with open(file_name,'r') as json_file_handle:
        json_obj = json.load(json_file_handle)
        return json_obj['box'],json_obj['calibration_point'],json_obj['chessboard_point']

def Perspective_transform(box, original_img):
    # 获取画框宽高(x=orignal_W,y=orignal_H)
    orignal_W = math.ceil(np.sqrt((box[3][1] - box[2][1]) ** 2 + (box[3][0] - box[2][0]) ** 2))
    orignal_H = math.ceil(np.sqrt((box[3][1] - box[0][1]) ** 2 + (box[3][0] - box[0][0]) ** 2))

    # 原图中的四个顶点,与变换矩阵
    pts1 = np.float32([box[0], box[1], box[2], box[3]])
    pts2 = np.float32(
        [[int(orignal_W + 1), int(orignal_H + 1)], [0, int(orignal_H + 1)], [0, 0], [int(orignal_W + 1), 0]])

    # 生成透视变换矩阵；进行透视变换
    M = cv2.getPerspectiveTransform(pts1, pts2)
    result_img = cv2.warpPerspective(original_img, M, (int(orignal_W + 3), int(orignal_H + 1)))

    return result_img
    
def main():
    global box
    global box1 
    global calibration_point 
    box = []  # the box that stores the coordinates of region
    box1 = [] # the box that stores the coordinates of chessboard 
    calibration_point = (0,0)  # x,y 
    def mouse(event, x, y, flags, param):
        global box
        if event == cv2.EVENT_LBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            cv2.circle(test_img, (x, y), 1, (0, 0, 255), thickness = -1)
            cv2.putText(test_img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (0, 0, 255), thickness = 1)
            cv2.imshow("set point", test_img)
            if len(box) < 4:
                box.append((x,y))
    def mouse1(event, x, y, flags, param):
        global box1
        if event == cv2.EVENT_LBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            cv2.circle(test_img, (x, y), 1, (0, 0, 255), thickness = -1)
            cv2.putText(test_img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (0, 0, 255), thickness = 1)
            cv2.imshow("set point", test_img)
            if len(box1) < 4:
                box1.append((x,y))
    def mouse3(event, x, y, flags, param):
        global calibration_point
        if event == cv2.EVENT_LBUTTONDOWN:
            xy = "%d,%d" % (x, y)
            cv2.circle(test_img, (x, y), 1, (0, 0, 255), thickness = -1)
            cv2.putText(test_img, xy, (x, y), cv2.FONT_HERSHEY_PLAIN,
                        1.0, (0, 0, 255), thickness = 1)
            cv2.imshow("set point", test_img)
            calibration_point = (x,y)
    def mouse2(a,b,c,d,e):
        pass
    option = input('Enter your choice: (1 for creating new point, 2 for checking current point)')
    if option == '1': 
        cap = cv2.VideoCapture(0)
    #    cap.set(3,720)
    #    cap.set(4,540)
        cap.set(5,30)
        ret, frame = cap.read()
        test_img = frame 
        test_img = cv2.resize(test_img,(960,720)) # reduce the size of image
        cv2.imshow('set point',test_img)
        cv2.namedWindow("set point")
        cv2.imshow("set point", test_img)
        cv2.setMouseCallback("set point", mouse)  # click should be clockwise, from buttom right
        cv2.waitKey(0)  # wait for choosing the point 
        cv2.setMouseCallback("set point", mouse2)   # disenable mouse click
        cv2.destroyAllWindows()
        ret, frame = cap.read()
        test_img = frame 
        test_img = cv2.resize(test_img,(960,720)) # reduce the size of image
        test_img = Perspective_transform(box,test_img)
        test_img = np.rot90(test_img)
        cv2.imshow('set point',test_img)
        cv2.namedWindow("set point")
        cv2.imshow("set point", test_img)
        cv2.setMouseCallback("set point", mouse3)  # click should be clockwise, from buttom right
        cv2.waitKey(0)  # wait for choosing the point 
        cv2.setMouseCallback("set point", mouse2)   # disenable mouse click
        cv2.destroyAllWindows()
        
        
        ret, frame = cap.read()
        test_img = frame 
        test_img = cv2.resize(test_img,(960,720)) # reduce the size of image        
        cv2.imshow('set point',test_img)
        cv2.namedWindow("set point")
        cv2.imshow("set point", test_img)
        cv2.setMouseCallback("set point", mouse1)  # click should be clockwise, from buttom right
        cv2.waitKey(0)  # wait for choosing the point 
        cv2.setMouseCallback("set point", mouse2)   # disenable mouse click
        cv2.destroyAllWindows()
        
        
        calibration = {'box':box,'calibration_point':calibration_point,'chessboard_point':box1}
        save_calibration_data(calibration)
    else:
        a,b,c = read_calibration_data()
        print(a)
        print(b)
        print(c)
    
if __name__ == '__main__':
    main()

