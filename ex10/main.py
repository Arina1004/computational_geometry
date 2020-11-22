from tkinter import *
import math
from itertools import *

root = Tk()

action = 'stop'
points = []
boundary_points = []

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
    global action, boundary_points

    action = 'start' if action == 'stop' else 'stop'
    print(action)

    if action == 'start':
        boundary_points = find_boundary_points()

canvas = Canvas(root, width=1000, height=600, bg='white')
canvas.bind("<Button-1>", callback)
canvas.bind("<Key>", key)
canvas.pack()

def draw():
    global time

    for point in points:
        canvas.create_text(point[0], point[1] + 15, text=point)
        canvas.create_oval(point[0] - 3,
                                                    point[1] - 3,
                                                    point[0] + 3,
                                                    point[1] + 3,
                                                    fill="#3c32a8")
    for boundary_point in boundary_points:
        canvas.create_oval(boundary_point[0] - 3,
                                                    boundary_point[1] - 3,
                                                    boundary_point[0] + 3,
                                                    boundary_point[1] + 3,
                                                    fill="#a83e32")
    root.after(50, draw)


draw()

root.mainloop()
