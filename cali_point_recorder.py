# recoder for all calibration points 
# Author: Jingkai Zhang &  Lanyue Fang
# Date: 2021.12.11

import json  

file_name = 'cali_points.json'

cali_points = {}
# calibration point 
cali_points['(5,-1)'] = (140,96)
# row 1 
cali_points['(1,1)'] = (67,162) # (1,3)   this one is out of range
cali_points['(2,1)'] = (67,162) # (1,3)   this one is out of range 
cali_points['(3,1)'] = (67,162)
cali_points['(4,1)'] = (102,162)
cali_points['(5,1)'] = (137,161)
cali_points['(6,1)'] = (170,163)
cali_points['(7,1)'] = (206.5,160.5)
cali_points['(8,1)'] = (240.5,162.5)
cali_points['(9,1)'] = (275.5,163.5)
# row 2 
cali_points['(1,2)'] = (70,196)  # (2,3) this one is out of range 
cali_points['(2,2)'] = (70,196)  # (2,3) this one is out of range 
cali_points['(3,2)'] = (70,196)
cali_points['(4,2)'] = (104.5,197.5)
cali_points['(5,2)'] = (137.5,196.5)
cali_points['(6,2)'] = (172.5,197.5)
cali_points['(7,2)'] = (208,198)
cali_points['(8,2)'] = (241,199.5)
cali_points['(9,2)'] = (275.5,198.5)
# row 3 
cali_points['(1,3)'] = (70.5,229.5) # this one is out of range 
cali_points['(2,3)'] = (70.5,229.5) # this one is out of range 
cali_points['(3,3)'] = (70.5,229.5)
cali_points['(4,3)'] = (103.5,230)
cali_points['(5,3)'] = (138.5,230.5)
cali_points['(6,3)'] = (171.5,230.5)
cali_points['(7,3)'] = (207.5,230.5)
cali_points['(8,3)'] = (243.5,232.5)
cali_points['(9,3)'] = (276.5,230.5)
# row 4 
cali_points['(1,4)'] = (69.5,265.5) # this one is out of range 
cali_points['(2,4)'] = (69.5,265.5) # this one is out of range 
cali_points['(3,4)'] = (69.5,265.5)
cali_points['(4,4)'] = (102.5,266.5)
cali_points['(5,4)'] = (137.5,265.5)
cali_points['(6,4)'] = (173,267.5)
cali_points['(7,4)'] = (206.5,267.5)
cali_points['(8,4)'] = (241.5,267.5)
cali_points['(9,4)'] = (276.5,265.5)
# row 5 
cali_points['(1,5)'] = (68.5,300.5) # this one is out of range 
cali_points['(2,5)'] = (68.5,300.5) # this one is out of range 
cali_points['(3,5)'] = (68.5,300.5)
cali_points['(4,5)'] = (102,299.5)
cali_points['(5,5)'] = (138.5,301)
cali_points['(6,5)'] = (172.5,303)
cali_points['(7,5)'] = (206.5,299.5)
cali_points['(8,5)'] = (240.5,302)
cali_points['(9,5)'] = (274.5,300.5)
# row 6 
cali_points['(1,6)'] = (67.5,333.5) # this one is out of range 
cali_points['(2,6)'] = (67.5,333.5) # this one is out of range 
cali_points['(3,6)'] = (67.5,333.5)
cali_points['(4,6)'] = (104.5,335.5)
cali_points['(5,6)'] = (136.5,335.5)
cali_points['(6,6)'] = (171.5,336.5)
cali_points['(7,6)'] = (211.5,340.5)
cali_points['(8,6)'] = (248.5,340.5)
cali_points['(9,6)'] = (274.5,340)
# row 7
cali_points['(1,7)'] = (65.5,369.5) # this one is out of range 
cali_points['(2,7)'] = (65.5,369.5) # this one is out of range 
cali_points['(3,7)'] = (65.5,369.5)
cali_points['(4,7)'] = (101.5,370.5)
cali_points['(5,7)'] = (136.5,368.5)
cali_points['(6,7)'] = (173.5,369.5)
cali_points['(7,7)'] = (205.5,370.5)
cali_points['(8,7)'] = (240.5,368.5)
cali_points['(9,7)'] = (276.5,370)
# row 8
cali_points['(1,8)'] = (67.5,407.5) # this one is out of range 
cali_points['(2,8)'] = (67.5,407.5) # this one is out of range 
cali_points['(3,8)'] = (67.5,407.5)
cali_points['(4,8)'] = (101.5,407.5)
cali_points['(5,8)'] = (138,405)
cali_points['(6,8)'] = (172.5,405.5)
cali_points['(7,8)'] = (206.5,407.5)
cali_points['(8,8)'] = (241.5,405.5)
cali_points['(9,8)'] = (276,406.5)
# row 9 
# all of this are out of range 
cali_points['(1,9)'] = cali_points['(3,8)']
cali_points['(2,9)'] = cali_points['(3,8)']
cali_points['(3,9)'] = cali_points['(3,8)']
cali_points['(4,9)'] = cali_points['(4,8)']
cali_points['(5,9)'] = cali_points['(5,8)']
cali_points['(6,9)'] = cali_points['(6,8)']
cali_points['(7,9)'] = cali_points['(7,8)']
cali_points['(8,9)'] = cali_points['(8,8)']
cali_points['(9,9)'] = cali_points['(9,8)']


with open(file_name,'w+') as json_handle:
    json_str = json.dumps(cali_points)
    json_handle.write(json_str)
    print('write!')
    