import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from algorithms import evklid


# # matrix = np.array([[1, 2, 3],
# #                    [4, 5, 6],
# #                    [7, 8, 9]])


# zeroz_matrix = np.zeros((10, 10))
# random_matrix = np.random.rand(10, 10)



# euclid_distance = evklid.euclidean_distance((1, 1), (8, 8))



# sec = 5
# distance = 10
# speed = distance / sec

# time_road = euclid_distance / speed
# print("Time of road:", time_road)



x_self = 0
y_self = 0

x_target = 7
y_target = 3

object_map = (6,3)

map_matrix = np.zeros((10, 10))

map_matrix[y_target][x_target] = 7
euclid_distance = evklid.euclidean_distance((x_self, y_self), (x_target, y_target))

map_matrix[object_map[1]][object_map[0]] = 10

while x_target > x_self and y_target > y_self:
    rot_koff = (y_target-y_self)/(x_target-x_self)
    print("Rotation coefficient:", rot_koff)
    x_self += 1
    if rot_koff > 0.5:
        y_self += 1
        
    map_matrix[y_self][x_self] = 5
    
    
print(map_matrix)
        