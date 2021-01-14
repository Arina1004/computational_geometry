from tkinter import *
import math
from itertools import *
from more_itertools import sort_together

root = Tk()

action = 'stop'
points = []
boundary_points = []

def clockwiseangle_and_distance(point):
    origin = center
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

def sorted_by_center(center):
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

def find_boundary_points():
    global boundary_points

    boundary_points = points
    for current_point in points:
        points_without_current = [x for x in points if x != current_point]

        for trigon_points in combinations(points_without_current, 3):
            if inPolygon(current_point[0], current_point[1], trigon_points):
                boundary_points= [x for x in boundary_points if x != current_point]

    return boundary_points


def on_click_canvas(point):
    global state, points, action, moving_point, time

    points.append(point)


def callback(event):
    canvas.focus_set()
    on_click_canvas([event.x, event.y])

def key(event):
    global action, boundary_points, center

    action = 'start' if action == 'stop' else 'stop'
    print(action)

    if action == 'start':
        boundary_points = find_boundary_points()
        center = find_center()
        boundary_points = sorted(boundary_points, key=clockwiseangle_and_distance)

canvas = Canvas(root, width=1000, height=600, bg='white')
canvas.bind("<Button-1>", callback)
canvas.bind("<Key>", key)
canvas.pack()

def draw():
    global time, center
    if  action == 'start':
        canvas.delete('all')
    for point in points:
        canvas.create_text(point[0], point[1] + 15, text=point)
        canvas.create_oval(point[0] - 3,
                                                    point[1] - 3,
                                                    point[0] + 3,
                                                    point[1] + 3,
                                                    fill="#3c32a8")
    for i in range(0, len(boundary_points)):
        right_index = (i + 1) % len(boundary_points)

        canvas.create_oval(boundary_points[i][0] - 3,
                                                    boundary_points[i][1] - 3,
                                                    boundary_points[i][0] + 3,
                                                    boundary_points[i][1] + 3,
                                                    fill="#a83e32")
        canvas.create_line(boundary_points[i][0],
                                                    boundary_points[i][1],
                                                    boundary_points[right_index][0],
                                                    boundary_points[right_index][1],
                                                    fill="#900C3F")

        canvas.create_oval(center[0] - 3,
                                                    center[1] - 3,
                                                    center[0] + 3,
                                                    center[1] + 3,
                                                    fill="#f5ec42")
    root.after(50, draw)


draw()

root.mainloop()
