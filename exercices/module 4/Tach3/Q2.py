import math

def distance(point):
    x, y = point
    return math.sqrt(x**2 + y**2)

print(distance((3, 4)))