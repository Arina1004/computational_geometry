from tkinter import *
import math
import numpy as np

radius = 3
width = 1000
height = 400


class Interface(Frame):
    def __init__(self, parent):
        self.point_radius = radius

        Frame.__init__(self, parent)

        self.points = []
        self.points_ids = []
        self.x_list = [0]
        self.y_list = [0]
        self.rect_points = []
        self.matrix = []

        self.mode = 'init'

        self.canvas = Canvas(parent, width=width,
                             height=height, background="#CBC3F0")
        self.canvas.grid(row=0, column=0, columnspan=4)

        self.gridB = Button(parent, text="Построить сетку",
                                 command=self.calculate_grid, width=20, height=2)
        self.gridB.grid(row=1, column=0, sticky=W)

        self.calc = Button(parent, text="Посчитать",
                           command=self.calculate_count, width=20, height=2)
        self.calc.grid(row=1, column=1, sticky=W)

        self.result = Entry(width=20)
        self.result.grid(row=1, column=3, sticky=W)

        self.canvas.bind("<Button-1>", self.create_element)

    def create_element(self, event):
        if self.mode == 'init':
            color = "#6C60A1"
            self.points.append([event.x, event.y])

            if event.x not in self.x_list:
                self.x_list.append(event.x)
            if event.y not in self.y_list:
                self.y_list.append(event.y)

            self.points_ids.append(self.canvas.create_oval(
                event.x - self.point_radius,
                event.y - self.point_radius,
                event.x + self.point_radius,
                event.y + self.point_radius,
                outline=color,
                fill=color,
                tags=("point")
            ))
        else:
            color = "#867ABF"
            self.canvas.create_oval(
                event.x - self.point_radius,
                event.y - self.point_radius,
                event.x + self.point_radius,
                event.y + self.point_radius,
                outline=color,
                fill=color,
                tags=("point")
            )
            self.rect_points.append([event.x, event.y])
            if len(self.rect_points) == 2:
                self.canvas.create_rectangle(self.rect_points[0][0], self.rect_points[0][1], self.rect_points[1][0], self.rect_points[1][1], outline="#867ABF")

    def calculate_grid(self):
        self.matrix = [[0]*len(self.x_list) for k in range(len(self.y_list))]

        self.x_list.append(width)
        self.x_list.sort()
        self.y_list.append(height)
        self.y_list.sort()

        print(self.x_list, self.y_list)

        for i in range(len(self.y_list) - 1):
          for j in range(len(self.x_list) - 1):
            self.canvas.create_rectangle(self.x_list[j], self.y_list[i], self.x_list[j+1], self.y_list[i+1])
            for point in self.points:
              if self.x_list[j+1] > point[0] and self.y_list[i] < point[1]:
                self.matrix[i][j] += 1

        self.mode = 'rectangle'
        print(self.matrix)

    def calculate_count(self):
        x1 = self.binary(self.x_list, self.rect_points[0][0])
        y1 = self.binary(self.y_list, self.rect_points[0][1])
        x2 = self.binary(self.x_list, self.rect_points[1][0])
        y2 = self.binary(self.y_list, self.rect_points[1][1])

        ru = self.matrix[y1][x2]
        lu = self.matrix[y1][x1]
        ld = self.matrix[y2][x1]
        rd = self.matrix[y2][x2]

        result = abs(ru - lu - rd + ld)
        self.result.delete(0, 'end')
        self.result.insert(0, result)

        self.rect_points = []

    def binary(self, arr, value):
        s = 0
        e = len(arr)-1
        while s <= e:
            middle = (s+e) // 2
            if value < arr[middle]:
                e = middle - 1
            elif value > arr[middle]:
                s = middle + 1
            else:
                return(middle)
                break
        else:
            if value < arr[middle]:
                return middle - 1
            else:
                return middle


if __name__ == "__main__":
    root = Tk()
    r = Interface(root)
    r.grid()
    root.mainloop()