from tkinter import *
import math
from itertools import *
from more_itertools import sort_together
import numpy as np

root = Tk()

action = 'stop'
points = []
boundary_points = []


def get_orientation(origin, p1, p2):
    difference = ((p2[0] - origin[0]) * (p1[1] - origin[1])) - (
        (p1[0] - origin[0]) * (p2[1] - origin[1])
    )
    return difference

def jarvismarch():
    n = len(points)
    P = points
    min_point = points[0]
    H = []

    #find p1
    for i in range(1,n):
        if points[i][1] == min_point[1] and  min_point[0] < points[i][0]:
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
    return H


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
        boundary_points = jarvismarch()

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

    root.after(50, draw)


draw()

root.mainloop()
