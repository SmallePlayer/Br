import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import numpy as np
from algorithms import evklid


start_time = time.time()

x_self = 0
y_self = 0

x_target = 9
y_target = 7

obstacle = (8,6)

open_list = []

map_matrix = np.zeros((10, 10))



map_matrix[y_target][x_target] = 7

# map_matrix[obstacle[1]][obstacle[0]] = 1
# print(map_matrix)

while x_target > x_self and y_target > y_self:
    rot_koff = (y_target-y_self)/(x_target-x_self)
    #print("Rotation coefficient:", rot_koff)
    x_self += 1
    if rot_koff > 0.5:
        y_self += 1
        
    if map_matrix[y_self][x_self] == 1:
        print("🚧 Препятствие на пути!")
        break
        
    map_matrix[y_self][x_self] = 5
    open_list.append((x_self, y_self))
    
end_time = time.time()
print("Path:", open_list) 
print("Execution time: %s seconds" % (end_time - start_time))
print(map_matrix)
  