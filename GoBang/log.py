# a simple logging system 
# Author: Jingkai Zhang 
# Date: 2021.12.10 

import datetime 
import os 
import inspect

class Log(object):
    def __init__(self):
        super()
        time_stamp_for_file = datetime.datetime.now().strftime('%Y-%m-%d')
        self.file_name = time_stamp_for_file + '_system.log'
        self.log_file_path = os.path.join('/home/pi/Desktop/ECE5725_project/ECE5725-Final-Project','logging/')
        if not os.path.exists(self.log_file_path + self.file_name):
            if not os.path.exists(self.log_file_path):
                os.makedirs(self.log_file_path)
            f = open(self.log_file_path + self.file_name,'w+')
            f.close()
            
        self.info('logging saved in ' + self.log_file_path + self.file_name)
    
    def get_time_stamp(self):
        # [0:23] means 3 digit in mili seconds, if it is removed, the total digit would be 6.
        # return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[0:23]
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    def get_func_name(self):
        return inspect.stack()[1][3]
    
    def write_log(self,str):
        with open(self.log_file_path + self.file_name,'a') as file:
            file.write(str)
            file.close()
    def info(self,content):
        logging_str = self.get_time_stamp()+' [INFO] ' + content + '\n'
        print(logging_str)
        self.write_log(logging_str)
        
    def debug(self,content):
        logging_str = self.get_time_stamp()+ ' [DEBUG] ' + content + '\n'
        print(logging_str)
        self.write_log(logging_str)
        
    def critical(self,content):
        logging_str = self.get_time_stamp()+' [CRITICAL] ' + content + '\n'
        print(logging_str)
        self.write_log(logging_str)
        
    def error(self,content):
        logging_str = self.get_time_stamp()+' [ERROR] ' + content + '\n'
        print(logging_str)
        self.write_log(logging_str)
    
    def warning(self,content):
        logging_str = self.get_time_stamp()+' [WARNING] ' + content + '\n'
        print(logging_str)
        self.write_log(logging_str)
        
# test part

if __name__ == '__main__':
    log = Log()
    log.info('Works fine')
    log.warning('Something might be a problem')
    log.debug('test something')