import math

def euclidean_distance(point1, point2):
    answer = math.sqrt(pow((point2[0] - point1[0]), 2) + pow((point2[1] - point1[1]), 2))
    print("Euclidean Distance:", answer)
    return answer