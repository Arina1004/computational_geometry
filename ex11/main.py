from tkinter import *
import math
from itertools import *
from more_itertools import sort_together

root = Tk()

action = 'stop'
points = []
boundary_points = []

def clockwise(points):
  n = len(points)

  min_point_index = 0
  min_point = points[0]
  for i in range(1,n):
      if points[i][1] == min_point[1] and  min_point[0] > points[i][0]:
          min_point = points[i]
          min_point_index = i
      elif points[i][1] > min_point[1]:
          min_point = points[i]
          min_point_index = i
  if rotation(points[min_point_index-1], points[min_point_index], points[(min_point_index + 1) % n]) < 0:
      return False
  return True

def distance(point):
    global current_point
    origin = current_point
    refvec = [1, 1]
    # Vector between point and the origin: v = p - o
    vector = [point[0]-origin[0], point[1]-origin[1]]
    # Length of vector: ||v||
    lenvector = math.hypot(vector[0], vector[1])

    return lenvector

def rotation(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def localization(point, polygon):
    left = 0
    right = 0
    for i in range(0,len(polygon)):
        right_index = (i + 1) % len(polygon)
        if rotation(polygon[i], polygon[right_index], point) > 0:
            left = 1
        else:
            right = 1
        if left == right:
            return False
    else:
        return True

def crossing(point, vertex, boundary_points):
    left = 0
    right = 0
    for j in range(len(boundary_points)):
        rotate = rotation(point,vertex, boundary_points[j])
        if rotate == 0:
            continue
        elif rotate > 0:
            left = 1
        else:
            right = 1
        if left == right:
            return True
    return False


def graham_scan():
    global min_point, current_point
    n = len(points)
    boundary_points = points[:3]
    if not clockwise(boundary_points):
        boundary_points.reverse()

    for i in range(3,n):
        current_point = points[i]
        if not localization(current_point, boundary_points):
            sorted_points = sorted(boundary_points, key=distance)
            start_point_index = boundary_points.index(sorted_points[0])
            left = 0
            right = 0
            for j in range(len(boundary_points)):
                rotate = rotation(current_point,boundary_points[start_point_index], boundary_points[j])
                if rotate == 0:
                    continue
                elif rotate > 0:
                    left = 1
                else:
                    right = 1
                if left == right:
                    left_point_index = (start_point_index + 1 ) % len(boundary_points)
                    right_point_index = start_point_index - 1
                    break
            else:
                if left > 0:
                    left_point_index = start_point_index
                    right_point_index = start_point_index - 1
                else:
                    left_point_index = (start_point_index + 1 ) % len(boundary_points)
                    right_point_index = start_point_index
            while crossing(current_point, boundary_points[left_point_index], boundary_points):
                left_point_index = (left_point_index + 1) % len(boundary_points)
            while crossing(current_point, boundary_points[right_point_index], boundary_points):
                right_point_index = right_point_index - 1
            # print("boundary_points:", boundary_points)
            # print("current_point:", current_point)
            # print("right_point_index:", right_point_index)
            # print("left_point_index:", left_point_index)

            if left_point_index == 0:
                boundary_points = boundary_points[:(right_point_index % len(boundary_points)) +1] + [current_point]
            else:
                boundary_points = boundary_points[:right_point_index+1] + [current_point] + boundary_points[left_point_index:len(boundary_points)]
    print(boundary_points)
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
        boundary_points = graham_scan()

canvas = Canvas(root, width=1000, height=600, bg='white')
canvas.bind("<Button-1>", callback)
canvas.bind("<Key>", key)
canvas.pack()

def draw():
    global time
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
