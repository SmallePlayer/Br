import time 
import numpy as np  
from A_bren import algoritm_A
from bren import algoritm_bren

start_time = time.time()

reach = False
map_matrix = np.zeros((10, 10))

x_self = 0
y_self = 0

x_target = 9
y_target = 7

obstacle = np.ones((2,2))

map_matrix[2:4, 2:4] = obstacle

rows, cols = map_matrix.shape

print("Initial map:")
print(map_matrix)


while reach == False:
    print("Starting brent algorithm...")
    reach, path, x_self, y_self = algoritm_bren( map_matrix, x_self, y_self, x_target, y_target) 
    
    print(f"reach, path, x_self, y_self: {reach}, {path}, {x_self}, {y_self}")
    
    if path == 0:
        print("🚧 Brent hit obstacle, starting A* algorithm...")
        reach, path = algoritm_A(map_matrix, rows, cols, x_self, y_self, x_target, y_target)
        print("Path found by A* algorithm:", path)
    else:
        print("✅ Path found by brent algorithm:", path)
        
print(f"Execution time: {time.time() - start_time} seconds")