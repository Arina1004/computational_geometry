from tkinter import *
import math
from itertools import *
from more_itertools import sort_together

root = Tk()

action = 'start'
points = []
polygon = []
localization_points=[]

def find_center():
    x_coords = [p[0] for p in polygon]
    y_coords = [p[1] for p in polygon]
    _len = len(polygon)
    centroid_x = sum(x_coords)/_len
    centroid_y = sum(y_coords)/_len
    return [centroid_x, centroid_y]

def rotation(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

def localization():
    n_p = len(polygon)
    localization_points =[]
    center = find_center()
    for j in range(0,len(points)):
        left_index = 0
        right_index = n_p
        while abs(right_index - left_index) > 1:
            if left_index < right_index:
              index = (right_index + left_index) // 2
            else:
              index = (right_index + left_index) // 2
            if rotation(polygon[left_index],center, points[j]) < 0 and rotation(polygon[index], center, points[j]) > 0:
                right_index = index
            else:
                left_index = index
        if rotation(polygon[left_index], polygon[(right_index) % n_p], points[j])  > 0:
            localization_points.append(points[j])

    return localization_points



def on_click_canvas(point):
    global polygon, points, action
    if action == 'start':
        polygon.append(point)
    elif action == 'points':
        points.append(point)




def callback(event):
    canvas.focus_set()
    on_click_canvas([event.x, event.y])

def key(event):
    global action, localization_points
    if action == 'start':
        action = 'points'
    else:
        action = 'draw'
        localization_points = localization()
    print(action)
    print(localization_points)


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
    for point in polygon:
        canvas.create_text(point[0], point[1] + 15, text=point)
        canvas.create_oval(point[0] - 3,
                                                point[1] - 3,
                                                point[0] + 3,
                                                point[1] + 3,
                                                fill="#3c32a8")
    if action == 'points':
        for i in range(0, len(polygon)):
            right_index = (i + 1) % len(polygon)
            canvas.create_line(polygon[i][0],
                                                        polygon[i][1],
                                                        polygon[right_index][0],
                                                        polygon[right_index][1],
                                                        fill="#900C3F")
    if action == 'draw':
        for point in points:
            if point in localization_points:
                color = "#4bf542"
            else:
                color = "#f54242"
            canvas.create_text(point[0], point[1] + 15, text=point)
            canvas.create_oval(point[0] - 3,
                                                        point[1] - 3,
                                                        point[0] + 3,
                                                        point[1] + 3,
                                                        fill=color)


    root.after(50, draw)


draw()

root.mainloop()
