import math
import numpy as np

boundary_points = []

def get_orientation(origin, p1, p2):
    difference = ((p2[0] - origin[0]) * (p1[1] - origin[1])) - (
        (p1[0] - origin[0]) * (p2[1] - origin[1])
    )
    return difference

def jarvismarch(points):
    n = len(points)
    P = points
    min_point = points[0]
    H = []

    #find p1
    for i in range(1,n):
        if points[i][1] == min_point[1] and  min_point[0] > points[i][0]:
            min_point = points[i]
        elif points[i][1] > min_point[1]:
            min_point = points[i]

    H.append(min_point)

    far_point = None
    point = min_point
    while far_point is not min_point:
        p1 = None
        for p in points:
            if p is point:
                continue
            else:
                p1 = p
                break
        far_point = p1

        for p2 in points:
            if p2 is point or p2 is p1:
                continue
            else:
                direction = get_orientation(point, far_point, p2)
                if direction > 0:
                    far_point = p2
        point = far_point
        H.append(far_point)
    print(H)
    return H

