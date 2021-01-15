import math
from itertools import *

h_center = 0
boundary_points = []

def clockwiseangle_and_distance(point):
    global boundary_points

    origin = h_center
    refvec = [1, 1]
    # Vector between point and the origin: v = p - o
    vector = [point[0]-origin[0], point[1]-origin[1]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])
    # If length is zero there is no angle
    if lenvector == 0:
        return -math.pi, 0
    # Normalize vector: v/||v||
    normalized = [vector[0]/lenvector, vector[1]/lenvector]
    dotprod  = normalized[0]*refvec[0] + normalized[1]*refvec[1]     # x1*x2 + y1*y2
    diffprod = refvec[1]*normalized[0] - refvec[0]*normalized[1]     # x1*y2 - y1*x2
    angle = math.atan2(diffprod, dotprod)
    # Negative angles represent counter-clockwise angles so we need to subtract them
    # from 2*pi (360 degrees)
    if angle < 0:
        return 2*math.pi+angle, lenvector
    # I return first the angle because that's the primary sorting criterium
    # but if two vectors have the same angle then the shorter distance should come first.
    return angle, lenvector

def sorted_by_center():
    return sorted(boundary_points, key=clockwiseangle_and_distance)

def find_center():
    x_coords = [p[0] for p in boundary_points]
    y_coords = [p[1] for p in boundary_points]
    _len = len(boundary_points)
    centroid_x = sum(x_coords)/_len
    centroid_y = sum(y_coords)/_len
    return [centroid_x, centroid_y]

def inPolygon(x, y, p):
    c=0
    for i in range(len(p)):
        if (((p[i][1]<=y and y<p[i-1][1]) or (p[i-1][1]<=y and y<p[i][1])) and
            (x > (p[i-1][0] - p[i][0]) * (y - p[i][1]) / (p[i-1][1] - p[i][1]) + p[i][0])): c = 1 - c
    return c

def find_boundary_points(points):
    global boundary_points

    boundary_points = points
    for current_point in points:
        points_without_current = [x for x in points if x != current_point]

        for trigon_points in combinations(points_without_current, 3):
            if inPolygon(current_point[0], current_point[1], trigon_points):
                boundary_points= [x for x in boundary_points if x != current_point]

    return boundary_points

def convex_hull(points):
    global h_center

    boundary_points = find_boundary_points(points)
    h_center = find_center()
    boundary_points = sorted(boundary_points, key=clockwiseangle_and_distance)

    return [boundary_points, h_center]
