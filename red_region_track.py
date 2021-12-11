
from typing_extensions import Final
import cv2 as cv
import numpy as np
# from img_calibration import Perspective_transform
from init import read_calibration_data
import math

def Perspective_transform(box,original_img):
    # 获取画框宽高(x=orignal_W,y=orignal_H)
    orignal_W = math.ceil(np.sqrt((box[3][1] - box[2][1])**2 + (box[3][0] - box[2][0])**2))
    orignal_H= math.ceil(np.sqrt((box[3][1] - box[0][1])**2 + (box[3][0] - box[0][0])**2))

    # 原图中的四个顶点,与变换矩阵
    pts1 = np.float32([box[0], box[1], box[2], box[3]])
    pts2 = np.float32([[int(orignal_W+1),int(orignal_H+1)], [0, int(orignal_H+1)], [0, 0], [int(orignal_W+1), 0]])

    # 生成透视变换矩阵；进行透视变换
    M = cv.getPerspectiveTransform(pts1, pts2)
    result_img = cv.warpPerspective(original_img, M, (int(orignal_W+3),int(orignal_H+1)))

    return result_img

if __name__ == '__main__':
    #box=[(465,447),(211,425),(233,100),(488,105)]
    # box=[(465,447),(488,105),(233,390),(211,425)]
    #cap = cv.VideoCapture(0)
    #print(box)
    box, _,_ = read_calibration_data()
    print('box=',box)
    circles_sequence = []
    circles_xc = []
    circles_yc = []
    circles_r = []
    cap = cv.VideoCapture(0)
    
    n = 0
    m = 0
    median = []
    while (cap.isOpened()):
        ret, frame = cap.read()
        # cv.imshow("origin",frame)
        frame = cv.resize(frame,(960,720))
        frame = Perspective_transform(box,frame)
        frame = np.rot90(frame)
        cv.imshow("transform",frame)
        hsvImg = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        red_lo = np.array([170, 100, 100])
        red_hi = np.array([179, 255, 255])
        red_region = cv.inRange(hsvImg, red_lo, red_hi)
        # cv.imshow("red_region", red_region)

        kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
        red_region = cv.erode(red_region, kernel)
        red_region = cv.dilate(red_region, kernel)
        cv.imshow("ed", red_region)

        circles = cv.HoughCircles(red_region, cv.HOUGH_GRADIENT, 1, 20 \
                                  , param1=30, param2=10, minRadius=0, maxRadius=100)
        # circles = np.uint16(np.around(circles))
        # if circles is None:
        #     continue
        coordinate = circles[0][0]
        # print(circles)
        print('x = ',coordinate[0],' y = ',coordinate[1])
        # cv.circle(frame, (int(average_xc), int(average_yc)), int(average_r), (0, 255, 0), 2)
        # # draw the center of the circle
        # cv.circle(frame, (int(average_xc), int(average_yc)), 2, (0, 0, 255), 3)
        # cv.imshow('detected circles', frame)
        # if circles is not None:
        #     c = circles[0]
        #     # print("xc,yc,r", c[0][0],c[0][1],c[0][2])
            
            
        #     if n<5:
        #         circles_sequence.append((c[0][0],c[0][1],c[0][2]))
        #         circles_xc.append(c[0][0])
        #         circles_yc.append(c[0][1])
        #         circles_r.append(c[0][2])
        #         n=n+1
        #     else:
        #         n=0
        #         circles_xc.sort()
        #         circles_yc.sort()
        #         circles_r.sort()
        #         xc=circles_xc[2]
        #         yc=circles_yc[2]
        #         r=circles_r[2]

        #         # print("median",xc,' ',yc,' ',r)            
        #         circles_sequence = []
        #         circles_xc = []
        #         circles_yc = []
        #         circles_r = []
                
        #         if m<3:
        #             median.append((xc,yc,r))
        #             m=m+1
        #         else:
        #             m=0
        #             average_xc=(median[0][0]+median[1][0]+median[2][0])/3
        #             average_yc=(median[0][1]+median[1][1]+median[2][1])/3
        #             average_r=(median[0][2]+median[1][2]+median[2][2])/3
        #             median = []
        #             print("average median",average_xc,average_yc,average_r)
                
                
        #             #draw the outer circle
        #             cv.circle(frame, (int(average_xc), int(average_yc)), int(average_r), (0, 255, 0), 2)
        #             # draw the center of the circle
        #             cv.circle(frame, (int(average_xc), int(average_yc)), 2, (0, 0, 255), 3)
        #             cv.imshow('detected circles', frame)
        
        
        if cv.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()
