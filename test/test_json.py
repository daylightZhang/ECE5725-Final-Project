import json 

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
        # print('write successed')   
        
        
if __name__ == '__main__':
    try:
        a = read('./test.json')
    except json.decoder.JSONDecodeError:
        print('the file is being written')