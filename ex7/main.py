from tkinter import *
import math
from itertools import *
from more_itertools import sort_together

root = Tk()

action = 'start'
points = []
polygon = []
localization_points=[]

def rotation(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
def find_ange(p1, p2,origin):
    refvec = p2
    # Vector between point and the origin: v = p - o
    point = p1
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
    return angle

def localization():
    n_p = len(polygon)
    left = 0
    right = 0
    localization_points =[]
    angle = 0
    for j in range(0,len(points)):
        for i in range(0,n_p):
            print(rotation(polygon[i-1], points[j], polygon[i]))
            print(find_ange(polygon[i-1], polygon[i], points[j]))

            angle += rotation(polygon[i-1], points[j], polygon[i])

        if abs(angle) == 628319:
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
