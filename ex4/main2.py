import math

def rotation(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def localization(poly_points, center, point):
    left_idx = 0
    right_idx = len(poly_points)

    while abs(right_idx - left_idx) > 1:
        index = (right_idx + left_idx) // 2

        if rotation(poly_points[left_idx], center, point) < 0 and 0 < rotation(poly_points[index], center, point):
            right_idx = index
        else:
            left_idx = index

    if rotation(poly_points[left_idx], poly_points[right_idx % len(poly_points)], point) > 0:
        return True

    return False