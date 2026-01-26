import time 
import numpy as np  
from A_bren import algoritm_A
from bren import algoritm_bren

start_time = time.time()

reach = False
map_matrix = np.zeros((50, 50))

x_self = 0
y_self = 0

x_target = 47
y_target = 49

obstacle = np.ones((5,5))

map_matrix[30:35, 35:40] = obstacle

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