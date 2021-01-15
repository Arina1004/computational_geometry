import math

def rotation(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def localization(poly_points, point):
    left = 0
    right = 0

    for i in range(0, len(poly_points)):
        right_index = (i + 1) % len(poly_points)
        if rotation(poly_points[i], poly_points[right_index], point) > 0:
            left = 1
        else:
            right = 1

    return left != right
