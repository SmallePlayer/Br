import math

def manhed_distance(point1, point2):
    answer = abs(point2[0] - point1[0]) + abs(point2[1] - point1[1])
    print("Manhattan Distance:", answer)
    return answer