import math
import time 
import numpy as np
from algorithms import evklid
from algorithms import manhed

start_time = time.time()

# start position
x_self = 0
y_self = 0

# target position
x_target = 474
y_target = 458

#obstacle position | позиция препятствия
obstacle = (7,3)

# create map matrix
map_matrix = np.zeros((500, 500))

# mark obstacle on map
map_matrix[obstacle[0]][obstacle[1]] = 1

#print(map_matrix)

#size of the map
rows, cols = map_matrix.shape

#infinity matrices for G and F costs
g_matrix = np.full((rows, cols), np.inf)
f_matrix = np.full((rows, cols), np.inf)
parent_matrix = [[None for _ in range(cols)] for _ in range(rows)]

open_list = []
closed_set = set()


g_matrix[x_self][y_self] = 0
h_start = manhed.manhed_distance((x_self, y_self), (x_target, y_target))
f_matrix[x_self][y_self] = h_start
open_list.append((h_start, x_self, y_self))
#print(open_list)

while open_list:
    current = min(open_list, key=lambda x: x[0])
    open_list.remove(current)
    current_f, current_x, current_y = current
    current_pos = (current_x, current_y)

    closed_set.add(current_pos)
    
    if current_pos != (x_self, y_self) and current_pos != (x_target, y_target):
        map_matrix[current_x][current_y] = 2
    
    #print("Current position:", current_pos)
    if current_pos == (x_target, y_target):
        print("🎯 Достигли цели!")
        
        # Восстанавливаем путь
        path = []
        r, c = current_x, current_y
        while (r, c) != (x_self, y_self):
            path.append((r, c))
            r, c = parent_matrix[r][c]
        path.append((x_self, y_self))
        path.reverse()
        
        #print(f"Путь ({len(path)} шагов): {path}")
        print("Время выполнения: %s секунд" % (time.time() - start_time))
        
        # Отмечаем путь на карте
        # for r, c in path:
        #     if (r, c) != (x_self, y_self) and (r, c) != (x_target, y_target):
        #         map_matrix[r][c] = 8  # путь
        #         #print("Marking path on map at:", (r, c))
        
        break
    # else:
    #     print(f"Еще не цель, продолжаем...") #current: {current_pos}")
        
    neighbors = []
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        neighbor_x, neighbor_y = current_x + dx, current_y + dy
        if 0 <= neighbor_x < rows and 0 <= neighbor_y < cols:
            neighbors.append((neighbor_x, neighbor_y))
            
    for neighbor in neighbors:
        nx, ny = neighbor

        if (nx, ny) in closed_set:
            continue
        
        if map_matrix[nx][ny] == 1:
            continue 
        
        new_g = g_matrix[current_x][current_y] + 1
        
        if new_g < g_matrix[nx][ny]:
            g_matrix[nx][ny] = new_g
            h_heigbors = manhed.manhed_distance((nx, ny), (x_target, y_target))
            # print("Heigbors h:", h_heigbors)
            new_f = new_g + h_heigbors
            f_matrix[nx][ny] = new_f
            
            parent_matrix[nx][ny] = (current_x, current_y)

            found = False
            for i, (f_val, row, col) in enumerate(open_list):
                if row == nx and col == ny:
                    # Обновляем запись в open_list
                    open_list[i] = (new_f, nx, ny)
                    found = True
                    break
            
            # Если не нашли - добавляем
            if not found:
                open_list.append((new_f, nx, ny))
                
print("Final map:")
print(map_matrix)   
