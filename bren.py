import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import numpy as np
from algorithms import evklid


start_time = time.time()

open_list = []


def algoritm_bren( map_matrix, x_self, y_self, x_target, y_target):
    map_matrix[y_target][x_target] = 7

    while x_target > x_self and y_target > y_self:
        rot_koff = (y_target-y_self)/(x_target-x_self)
        #print("Rotation coefficient:", rot_koff)
        old_x_self = x_self
        old_y_self = y_self
        x_self += 1
        if rot_koff > 0.5:
            y_self += 1
            
        if map_matrix[y_self][x_self] == 1:
            print("🚧 Обнаружено препятствие на пути!")
            print("Brent algorithm stopped at:", (x_self, y_self))
            return False, 0, old_x_self, old_y_self
            
            
        map_matrix[y_self][x_self] = 5
        open_list.append((x_self, y_self))
    return True, open_list, x_self, y_self
        
    # end_time = time.time()
    # print("Path:", open_list) 
    # print("Execution time: %s seconds" % (end_time - start_time))
    # print(map_matrix)
    