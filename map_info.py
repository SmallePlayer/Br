import time 
import numpy as np  
from A_bren import algoritm_A
from bren import algoritm_bren

start_time = time.time()

reach = False
map_matrix = np.zeros((100, 100))

x_self = 0
y_self = 0

x_target = 88
y_target = 77

obstacle = np.ones((10,10))

map_matrix[70:80, 70:80] = obstacle

rows, cols = map_matrix.shape



while reach == False:
    print(x_self, y_self)
    reach, path, x_self, y_self = algoritm_bren( map_matrix, x_self, y_self, x_target, y_target) 
    
    
    if path == 0:
        #print("🚧")
        reach, path,x_self, y_self = algoritm_A(map_matrix, rows, cols, x_self, y_self, x_target, y_target, step=1)
        #print("A*", path)
    else:
        print("✅", path)
        
print(f"Execution time: {time.time() - start_time} seconds")