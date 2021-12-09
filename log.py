# a simple logging system 
# Date: 2021.12.10 
import json
import datetime 
class Log(object):
    def __init__(self):
        super()
        self.file_path = './system.log'
        self.logging_str = []
    
    def get_time_stamp(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def write_log(self,str):
        with open(self.file_path,'a') as file:
            file.write(str)
    
    def info(self,content):
        logging_str = self.get_time_stamp()+' [INFO] ' + content
        print(logging_str)
        self.write_log(logging_str)
        
    def debug(self,content):
        logging_str = self.get_time_stamp()+ '[DEBUG] ' + content
        print(logging_str)
        self.write_log(logging_str)
        
    def fetal(self,content):
        logging_str = self.get_time_stamp()+'[FETAL] ' + content
        print(logging_str)
        self.write_log(logging_str)
    
    def warning(self,content):
        logging_str = self.get_time_stamp()+'[WARNING] ' + content
        print(logging_str)
        self.write_log(logging_str)