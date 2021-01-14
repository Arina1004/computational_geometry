from tkinter import *
import math
from itertools import *
from more_itertools import sort_together

root = Tk()

action = 'stop'
points = []

def rotation(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def is_convex():
  n = len(points)
  left = 0
  right = 0

  for i in range(0,n):
    for j in range(0,n):
      right_index = (j + 1) % len(points)
      rotate = rotation(points[i-1], points[i], points[right_index])
      if rotate > 0:
          left = 1
      elif rotate < 0:
          right = 1
    if left == right:
      return False
  return True



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
        print(is_convex())

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
    if  action == 'start':
        canvas.delete('all')
        for point in points:
            canvas.create_text(point[0], point[1] + 15, text=point)
            canvas.create_oval(point[0] - 3,
                                                    point[1] - 3,
                                                    point[0] + 3,
                                                    point[1] + 3,
                                                    fill="#3c32a8")
        for i in range(0, len(points)):
            right_index = (i + 1) % len(points)
            canvas.create_line(points[i][0],
                                                        points[i][1],
                                                        points[right_index][0],
                                                        points[right_index][1],
                                                        fill="#900C3F")

    root.after(50, draw)


draw()

root.mainloop()
