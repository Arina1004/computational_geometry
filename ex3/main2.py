from tkinter import *
import math
from itertools import *
from more_itertools import sort_together

root = Tk()

prevAction = 'init'
action = 'init'
points = []
cpoints = []
mpoint = -1


def rotation(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def is_convex():
  n = len(points)
  left_turn = 0
  right_turn = 0

  for i in range(1,n):
    right_index = (i + 1) % len(points)
    if rotation(points[i-1], points[i], points[right_index]) > 0:
        left_turn = 1
    else:
        right_turn = 1
  return left_turn != right_turn



def on_click_canvas(point):
    global state, points, action, moving_point, time

    points.append(point)


def callback(event):
    global action, prevAction, mpoint

    canvas.focus_set()
    if action == 'move':
        action = prevAction
        if action == 'start':
            print(is_convex())
    else:
        for i in range(len(points)):
            if points[i][0] - 3 <= event.x and points[i][0] + 3 >= event.x and points[i][1] - 3 <= event.y and points[i][1] + 3 >= event.y:
                mpoint = i
                prevAction = action
                action = 'move'
                return
        on_click_canvas([event.x, event.y])

def key(event):
    global action, boundary_points, center

    if action == 'move':
        action = prevAction
    elif action == 'init':
        action = 'lines'
    elif action == 'start':
        action = 'stop'
    else:
        action = 'init'

    if action == 'start':
        print(is_convex())

def move(event):
    global action, points

    if action == 'move':
        point = points[mpoint]
        canvas.move(cpoints[mpoint][1], event.x - point[0], event.y - point[1])
        canvas.delete(cpoints[mpoint][0])
        text = canvas.create_text(point[0], point[1] + 15, text=point)
        if prevAction == 'start':
            canvas.delete(cpoints[mpoint][2])
            canvas.delete(cpoints[mpoint][3])
            left_index = (mpoint - 1) % len(points)
            right_index = (mpoint + 1) % len(points)
            line1 = canvas.create_line(points[mpoint][0],
                                        points[mpoint][1],
                                        points[right_index][0],
                                        points[right_index][1],
                                        fill="#900C3F")
            line2 = canvas.create_line(points[left_index][0],
                                        points[left_index][1],
                                        points[mpoint][0],
                                        points[mpoint][1],
                                        fill="#900C3F")
            try:
                cpoints[left_index].remove(cpoints[mpoint][2])
                cpoints[right_index].remove(cpoints[mpoint][3])
            except ValueError:
                cpoints[left_index].remove(cpoints[mpoint][3])
                cpoints[right_index].remove(cpoints[mpoint][2])
            cpoints[mpoint][2] = line1
            cpoints[mpoint][3] = line2
            cpoints[left_index].append(line2)
            cpoints[right_index].append(line1)
        cpoints[mpoint][0] = text
        points[mpoint] = [event.x, event.y]
        

canvas = Canvas(root, width=1000, height=600, bg='white')
canvas.bind("<Button-1>", callback)
canvas.bind("<Key>", key)
canvas.bind('<Motion>', move)
canvas.pack()

def draw():
    global time, points, cpoints, action
    if action == 'init':
        cpoints = []
        canvas.delete('all')
        for point in points:
            text = canvas.create_text(point[0], point[1] + 15, text=point)
            oval = canvas.create_oval(point[0] - 3,
                                                    point[1] - 3,
                                                    point[0] + 3,
                                                    point[1] + 3,
                                                    fill="#3c32a8")
            cpoints.append([text, oval])
    if  action == 'lines':
        for i in range(0, len(points)):
            right_index = (i + 1) % len(points)
            line = canvas.create_line(points[i][0],
                                                        points[i][1],
                                                        points[right_index][0],
                                                        points[right_index][1],
                                                        fill="#900C3F")
            cpoints[i].append(line)
            cpoints[right_index].append(line)
            action = 'start'
    elif action == 'stop':
        canvas.delete('all')
        points=[]
        cpoints = []
        action='init'

    root.after(50, draw)


draw()

root.mainloop()
