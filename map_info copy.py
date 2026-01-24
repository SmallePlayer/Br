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

# Матрица для визуализации (копия исходной)
vis_matrix = map_matrix.copy()

# Отмечаем начальную позицию
vis_matrix[x_self, y_self] = 2

# Отмечаем цель
vis_matrix[x_target, y_target] = 9

while reach == False:
    print(f"Current position: ({x_self}, {y_self})")
    reach, path, x_self, y_self = algoritm_bren(map_matrix, x_self, y_self, x_target, y_target) 
    
    if path == 0:
        #print("🚧 Using A* algorithm")
        reach, path, x_self, y_self = algoritm_A(map_matrix, rows, cols, x_self, y_self, x_target, y_target, step=1)
        #print("A* path:", path)
    else:
        print("✅ Path found:", path)
        
    # Отмечаем путь на матрице визуализации
    if path != 0:
        # Предполагаем, что path - это список координат [(x1, y1), (x2, y2), ...]
        # или в другом формате, который нужно адаптировать
        for point in path:
            if hasattr(point, '__len__') and len(point) >= 2:
                x, y = point[0], point[1]
                # Проверяем, что координаты в пределах матрицы
                if 0 <= x < 100 and 0 <= y < 100:
                    # Не перезаписываем цель (9) и препятствия (1)
                    if vis_matrix[x, y] != 9 and vis_matrix[x, y] != 1:
                        vis_matrix[x, y] = 2
            else:
                # Если path имеет другой формат, возможно это одиночная точка
                try:
                    x, y = point
                    if 0 <= x < 100 and 0 <= y < 100:
                        if vis_matrix[x, y] != 9 and vis_matrix[x, y] != 1:
                            vis_matrix[x, y] = 2
                except:
                    pass

print(f"Execution time: {time.time() - start_time} seconds")

# Визуализация матрицы
print("\n" + "="*50)
print("VISUALIZATION OF THE MAP (100x100)")
print("Legend: 0=empty, 1=obstacle, 2=path, 9=target")
print("="*50 + "\n")

# Поскольку матрица 100x100 слишком большая для вывода в консоль,
# давайте выведем ее в компактном виде или только интересную область

# Вариант 1: Вывод всей матрицы (будет очень большим)
print("Full matrix visualization (100x100):")
for i in range(100):
    row_str = ""
    for j in range(100):
        if vis_matrix[i, j] == 0:
            row_str += " "
        elif vis_matrix[i, j] == 1:
            row_str += "█"  # Блок препятствия
        elif vis_matrix[i, j] == 2:
            row_str += "·"  # Точка пути
        elif vis_matrix[i, j] == 9:
            row_str += "★"  # Звезда - цель
    print(row_str)

# Вариант 2: Вывод только области вокруг пути (рекомендуется)
print("\n" + "="*50)
print("ZOOMED VIEW AROUND THE PATH AND OBSTACLE")
print("="*50)

# Определяем границы для отображения
min_x = max(0, min(x_self, x_target, 70) - 5)
max_x = min(99, max(x_self, x_target, 79) + 5)
min_y = max(0, min(y_self, y_target, 70) - 5)
max_y = min(99, max(y_self, y_target, 79) + 5)

print(f"Displaying area: rows [{min_x}:{max_x}], cols [{min_y}:{max_y}]")
print("\nLegend: ' '=empty, '█'=obstacle, '·'=path, '★'=target, 'S'=start\n")

# Заголовок с координатами столбцов
header = "     "
for j in range(min_y, max_y + 1):
    header += f"{j:2d}" if j % 5 == 0 else "  "
print(header)

for i in range(min_x, max_x + 1):
    # Номер строки
    row_label = f"{i:3d}: "
    row_str = ""
    
    for j in range(min_y, max_y + 1):
        if i == 0 and j == 0 and vis_matrix[i, j] != 2:
            row_str += "S"  # Стартовая позиция
        elif vis_matrix[i, j] == 0:
            row_str += " "
        elif vis_matrix[i, j] == 1:
            row_str += "█"
        elif vis_matrix[i, j] == 2:
            # Проверяем, не является ли это текущей позицией
            if i == x_self and j == y_self:
                row_str += "○"  # Текущая позиция
            else:
                row_str += "·"
        elif vis_matrix[i, j] == 9:
            row_str += "★"
    
    print(row_label + row_str)

# Статистика
print("\n" + "="*50)
print("STATISTICS:")
print(f"Start position: (0, 0)")
print(f"Target position: ({x_target}, {y_target})")
print(f"Final position: ({x_self}, {y_self})")
print(f"Obstacle area: rows [70:80], cols [70:80]")
path_cells = np.sum(vis_matrix == 2)
print(f"Path cells: {path_cells}")
print(f"Execution time: {time.time() - start_time:.2f} seconds")