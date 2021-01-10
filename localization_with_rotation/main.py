#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from xml.dom import minidom
import xml.etree.cElementTree as ET
from tkinter import filedialog as fd
import math
import operator


radius = 3
width = 1200
height = 500

class MyPolygon(object):
    def __init__(self, points, points_ids, canvas):
        self.point_radius = radius
        self.canvas = canvas

        self.points = points.copy()
        self.initial_points = []

        for point in self.points:
            self.initial_points.append([point[0], point[1]])

        self.count = len(points)

        self.lines_ids = []

        self.points_ids = points_ids.copy()

        self.draw_lines()
        self.draw_points()

        self.scale = 1

        self.angle = 0

        self.center = 0
        self.calculate_center()

    def draw_lines(self):
        for line in self.lines_ids:
            self.canvas.delete(line)

        self.lines_ids = []

        for point_id in range(self.count):
            self.lines_ids.append(self.canvas.create_line(self.points[point_id][0],
                           self.points[point_id][1],
                           self.points[(point_id + 1) % self.count][0],
                           self.points[(point_id + 1) % self.count][1]))

    def draw_points(self):
        for point in self.points_ids:
            self.canvas.delete(point)

        self.points_ids = []

        for point_id in range(self.count):
            self.points_ids.append(self.canvas.create_oval(
                self.points[point_id][0] - self.point_radius,
                self.points[point_id][1] - self.point_radius,
                self.points[point_id][0] + self.point_radius,
                self.points[point_id][1] + self.point_radius,
                outline="#0000FF",
                fill="#0000FF",
                tags=("point")
            ))

    def set_vertex(self, id, point):
        self.points[id] = point.copy()

        self.draw_lines()
        self.draw_points()

    def is_intersection(self, point):
        for i in range(self.count):
            x_condition = self.points[i][0] - self.point_radius <= point[0] and self.points[i][0] + self.point_radius >= point[0]
            y_condition = self.points[i][1] - self.point_radius <= point[1] and self.points[i][1] + self.point_radius >= point[1]

            if x_condition and y_condition:
                return i

        return -1

    def get_points(self):
        return self.points

    def set_scale(self, scale):
        if scale == self.scale:
            return

        new_points = []
        new_initial_points = []

        for i in range(len(self.points)):
            x_offset = (self.points[i][0] - self.center[0]) * scale / self.scale
            y_offset = (self.points[i][1] - self.center[1]) * scale / self.scale

            new_points.append([self.center[0] + x_offset, self.center[1] + y_offset])

        for i in range(len(self.initial_points)):
            x_offset = (self.initial_points[i][0] - self.center[0]) * scale / self.scale
            y_offset = (self.initial_points[i][1] - self.center[1]) * scale / self.scale

            new_initial_points.append([self.center[0] + x_offset, self.center[1] + y_offset])

        self.initial_points = new_initial_points
        self.points = new_points
        self.scale = scale

        self.calculate_center()

        self.draw_lines()
        self.draw_points()

    def rotation(self, angle):
        self.angle = angle
        for i in range(self.count):
            self.points[i][0] = self.center[0] + (self.initial_points[i][0] - self.center[0]) * math.cos(angle) - (
                    self.initial_points[i][1] - self.center[1]) * math.sin(angle)
            self.points[i][1] = self.center[1] + (self.initial_points[i][0] - self.center[0]) * math.sin(
                angle) + (self.initial_points[i][1] - self.center[1]) * math.cos(angle)

        self.draw_lines()
        self.draw_points()

    def calculate_center(self):
        summa_x = 0
        summa_y = 0

        for i in range(self.count):
            summa_x += self.points[i][0]
            summa_y += self.points[i][1]

        self.center = [summa_x // self.count, summa_y // self.count]

class Example(Frame):
    def __init__(self, parent):
        self.point_radius = radius

        Frame.__init__(self, parent)

        self.poly = False

        self.points = []
        self.points_ids = []

        self.canvas = Canvas(width=width, height=height, background="bisque")
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.scale = Scale(parent, digits=3,command=self.change_scale, orient=HORIZONTAL, length=300, from_=0.25, to=2,
                           tickinterval=0.25, resolution=0.05, label="Масштаб")
        self.scale.set(1)

        self.rotation = Scale(parent, digits=3, command=self.rotate, orient=HORIZONTAL, length=300, from_=-180,
                           to=180,
                           tickinterval=30, resolution=1, label="Поворот")

        self.loading = Button(parent, text="Import Polygon", command= self.import_polygons, width=20, height=2)
        self.export = Button(parent, text="Export Polygons", command= self.export_polygons, width=20, height=2)
        self.reset = Button(parent, text="Reset", command= self.reset_canvas, width=20, height=2)

        self.reset.grid(row=3, column=2, sticky=W)
        self.loading.grid(row=1, column=1, sticky=W)
        self.export.grid(row=3, column=1, sticky=W)
        self.scale.grid(row=2, column=0, columnspan=2, sticky=W)
        self.rotation.grid(row=3, column=0, columnspan=2, sticky=W)

        self._drag_data = {"x": 0, "y": 0, "item": None, "id": -1, "is_poly": False}

        self.canvas.tag_bind("point", "<ButtonPress-3>", self.drag_start)
        self.canvas.tag_bind("point", "<ButtonRelease-3>", self.drag_stop)
        self.canvas.tag_bind("point", "<B3-Motion>", self.drag)
        self.canvas.bind("<ButtonPress-2>", self.finish_poly)
        self.canvas.bind("<Button-1>", self.create_point)

    def finish_poly(self, event):
        if len(self.points) > 2:
            self.create_poly(self.points, self.points_ids)

            self.points = []
            self.points_ids = []

    def create_point(self, event):
        """Create a token at the given coordinate in the given color"""
        color = "#0000FF"

        if self.poly:
            color = "#00FF00" if self.localization_with_turn([event.x, event.y]) else "#FF0000"

        self.points.append([event.x, event.y, color])
        self.points_ids.append(self.canvas.create_oval(
            event.x - self.point_radius,
            event.y - self.point_radius,
            event.x + self.point_radius,
            event.y + self.point_radius,
            outline=color,
            fill=color,
            tags=("point")
        ))

    def create_poly(self, points, points_ids):
        if len(points) > 2:
            self.poly = MyPolygon(points, points_ids, self.canvas)

    def drag_start(self, event):
        """Begining drag of an object"""
        # record the item and its location
        id = self.canvas.find_closest(event.x, event.y)[0]


        self._drag_data["item"] = id
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

        if self.is_intersection([event.x, event.y]) != -1:
            self._drag_data["id"] = self.is_intersection([event.x, event.y])
            self._drag_data["is_poly"] = False
        else:
            self._drag_data["is_poly"] = True

            point_id = self.poly.is_intersection([event.x, event.y])

            if point_id > -1:
                self._drag_data["id"] = point_id

    def drag_stop(self, event):
        """End drag of an object"""
        # reset the drag information
        if self._drag_data["is_poly"]:
            self.poly.set_vertex(self._drag_data["id"], [event.x, event.y])
        else:
            self.points[self._drag_data["id"]][0] = event.x
            self.points[self._drag_data["id"]][1] = event.y

        self._drag_data["item"] = None
        self._drag_data["id"] = -1
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0
        self._drag_data["is_poly"] = False

        self.recalculate_colors()

    def drag(self, event):
        """Handle dragging of an object"""
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]

        self.canvas.move(self._drag_data["item"], delta_x, delta_y)

        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

        if self._drag_data["is_poly"]:
            self.poly.get_points()[self._drag_data["id"]] = [event.x, event.y]
            self.poly.draw_lines()
        else:
            self.points[self._drag_data["id"]][0] = event.x
            self.points[self._drag_data["id"]][1] = event.y

    def reset_canvas(self):
        self.poly = False
        self.points = []
        self.canvas.delete("all")

    def localization_with_turn(self, point):
        points = self.poly.points

        init_sign = self.get_turn_sign([points[0], points[1]], point)

        for i in range(1, len(points)):
            if init_sign != self.get_turn_sign([points[i], points[(i + 1) % len(points)]], point):
                return False

        return True

    def change_color(self, id, color):
        self.canvas.itemconfig(id, fill=color, outline=color)

    def recalculate_colors(self):
        for i in range(len(self.points)):
            predicted_color = "#00FF00" if self.localization_with_turn(self.points[i]) else "#FF0000"

            if self.points[i][2] != predicted_color:
                self.change_color(self.points_ids[i], predicted_color)
                self.points[i][2] = predicted_color

    def is_intersection(self, point):
        for i in range(len(self.points)):
            x_condition = self.points[i][0] - self.point_radius <= point[0] and self.points[i][0] + self.point_radius >= point[0]
            y_condition = self.points[i][1] - self.point_radius <= point[1] and self.points[i][1] + self.point_radius >= point[1]

            if x_condition and y_condition:
                return i

        return -1

    def change_scale(self, event):
        if self.poly:
            self.poly.set_scale(float(event))

            self.recalculate_colors()

    def rotate(self, event):
        if self.poly:
            self.poly.rotation(math.pi * int(event) / 180)

            self.recalculate_colors()

    def import_polygons(self):
        color = "#0000FF"

        file_name = fd.askopenfilename()
        tree = ET.ElementTree(file=file_name)

        for polygon in tree.getroot():
            points = []
            points_ids = []
            for point in polygon:
                points.append([int(point.attrib['x']), int(point.attrib['y']), color])
                points_ids.append(self.canvas.create_oval(
                    int(point.attrib['x']) - self.point_radius,
                    int(point.attrib['y']) - self.point_radius,
                    int(point.attrib['x']) + self.point_radius,
                    int(point.attrib['y']) + self.point_radius,
                    outline=color,
                    fill=color,
                    tags=("point")
                ))

            self.create_poly(points, points_ids)
            return

    def export_polygons(self):
        file_name = fd.asksaveasfilename()
        root = ET.Element("polygons")

        polygon = ET.Element("polygon")
        root.append(polygon)
        for _point in self.poly.points:
            point = ET.SubElement(polygon, "point")
            point.attrib['x'] = str(_point[0])
            point.attrib['y'] = str(_point[1])
        tree = ET.ElementTree(root)
        tree.write(file_name)

    def get_turn_sign(self, vector, point):
        x1, y1 = vector[0][:2]

        x2, y2 = vector[1][:2]

        x3, y3 = point[:2]

        a = (x2 - x1, y2 - y1)
        b = (x3 - x2, y3 - y2)

        result = 1 if ((x2 - x1) * (y3 - y2) - (x3 - x2) * (y2 - y1)) > 0 else -1

        print(result, sum(map(operator.mul, a, b)))

        return result

if __name__ == "__main__":
    root = Tk()
    r = Example(root)
    # Example(root).pack(fill="both", expand=True)
    r.grid()
    root.mainloop()
