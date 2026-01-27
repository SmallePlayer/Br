import math
import time
import numpy as np
from br.pathfinding import heuristics
from br.utils import euclid


def algoritm_A(map_matrix,rows, cols, x_self, y_self, x_target, y_target, step):
    #infinity matrices for G and F costs
    g_matrix = np.full((rows, cols), np.inf)
    f_matrix = np.full((rows, cols), np.inf)
    parent_matrix = [[None for _ in range(cols)] for _ in range(rows)]

    open_list = []
    closed_set = set()


    g_matrix[x_self][y_self] = 0
    h_start = heuristics.manhed_distance((x_self, y_self), (x_target, y_target))
    f_matrix[x_self][y_self] = h_start
    open_list.append((h_start, x_self, y_self))

    steps = 0
    best_nx, best_ny = x_self, y_self

    while steps < 1:
        steps += step
        current = min(open_list, key=lambda x: x[0])
        open_list.remove(current)
        current_f, current_x, current_y = current
        current_pos = (current_x, current_y)

        closed_set.add(current_pos)
        
        if current_pos != (x_self, y_self) and current_pos != (x_target, y_target):
            map_matrix[current_x][current_y] = 2
        
        if current_pos == (x_target, y_target):
            #print("🎯  цели!")
            
            path = []
            r, c = current_x, current_y
            while (r, c) != (x_self, y_self):
                path.append((r, c))
                r, c = parent_matrix[r][c]
            path.append((x_self, y_self))
            path.reverse()
            
            return True, path, nx, ny
            
            
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
                h_heigbors = heuristics.manhed_distance((nx, ny), (x_target, y_target))
    
                new_f = new_g + h_heigbors
                f_matrix[nx][ny] = new_f
                
                parent_matrix[nx][ny] = (current_x, current_y)

                found = False
                for i, (f_val, row, col) in enumerate(open_list):
                    if row == nx and col == ny:
                        open_list[i] = (new_f, nx, ny)
                        best_nx = nx
                        best_ny = ny
                        found = True
                        break
                
                if not found:
                    open_list.append((new_f, nx, ny))
                    best_nx = nx
                    best_ny = ny
                    
    return False, None, best_nx, best_ny
