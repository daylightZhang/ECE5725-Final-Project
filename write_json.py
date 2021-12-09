import json
import time 

file_name = 'info.json'

def read(file_name):
    with open(file_name,'r') as json_file_handle:
        info = json.load(json_file_handle)
    return info
def write(file_name,key,value):
    cur_info = read(file_name)
    cur_info[key] = value
    
    with open(file_name,'w') as json_file_handle:
        new_info = json.dumps(cur_info)
        json_file_handle.write(new_info)
        print('write successed')

# a = {}
# a['some_flag'] = True 
# a['array'] = (1,2,3,4,5)

# with open(file_name, 'w+') as json_file_handle:
#     json_obj = json.dumps(a)
#     json_file_handle.write(json_obj)
    # try:
    #     json_str = json.load(json_file_handle)
    # except json.decoder.JSONDecodeError:
    #     print('empty file')
    # # print(json_str)
    
# json_file_handle.close()    
while True:
    cur_info = read(file_name)
    print(cur_info)
    key = input('key that you want to change:')
    content = input('value for this value:')
    value = True if content == '1' else False 
    write(file_name,key,value)
