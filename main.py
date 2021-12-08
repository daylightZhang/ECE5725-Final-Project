# main program for the project 
# Author: Jingkai Zhang (jz544@cornell.edu) and Lanyue Fang (lf355@cornell.edu)
# Date: 2021.11.29
import threading
import RPi.GPIO as GPIO  
from GoBang.GUI import GoBang_GUI
from HardDriver.motor import Motor
import time, datetime

def GUI_dispaly():
    GUI = GoBang_GUI()
    GUI.run()

def test(c,b):
    start_time = time.time()
    while time.time() - start_time < 20:
        print('c=',c,'d=',b)
        time.sleep(1)
        
def motor(num):
    start_time = time.time()
    while time.time() - start_time < 10:
        print(num,' is moving !')
        print(time.time())
        time.sleep(1)
def test_motor():
    m1 = threading.Thread(target=motor,args='1')
    m2 = threading.Thread(target=motor,args='2')
    m1.start()
    m2.start()
    m1.join()
    m2.join()

def main():
    '''
        1. calibration of motors 
        2. display the GUI 
        3. waiting human's step
        4. When human pressed buttom, take a picture and start to recognize human's step
        5. Update the chessboard and generate AI's next step 
        6. Pick up a chess and move it to the position
        7. After that, move it to the calibration position
        8. go the step 3 
    '''
    # thread1 = threading.Thread(target=GUI_dispaly)
    # thread1.setDaemon(True)  # if this is set to False, the Main thread will wait for the end of subthread
    #                           # Otherwise, when the main thread end, the subthread will end as well.
    # thread1.start()
    
    # thread2 = threading.Thread(target=test,args=(100,200))
    # thread2.start()
    '''
        csv read/write
    '''
    # import csv
    # chess = [[1,2,3,4,5,6],[2,2,3,4,5,6],[9,6,5,3,5,1]]
    # f = open('chess.csv','w')
    # write = csv.writer(f)
    # write.writerows(chess)
    # f.close()
    '''
        json read/write
    '''
    # import json
    # chess = [[1,2,3,4,5,6],[2,2,3,4,5,6],[9,6,5,3,5,1]]
    # json_str = json.dumps(chess)
    # file_name = 'chess.json'
    # with open(file_name, 'w+') as json_file_handle:
    #     json_file_handle.write(json_str)
    # import json
    # file_name = 'chess.json'
    # with open(file_name,'r') as json_file_handle:
    #     json_obj = json.load(json_file_handle)
    #     print(json_obj[0])
    #     print(json_obj[1])

if __name__ == '__main__':
    main()