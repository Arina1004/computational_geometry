#! /usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import math

radius = 3
width = 1200
height = 500

class Line(object):
    def __init__(self, point, id, canvas, color):
        self.canvas = canvas
        self.color = color

        self.center = point.copy()
        self.id = id
        self.idx = -1
        self.angle = 0

        self.point_start = [0, 0]
        self.point_end = [0, 0]

        self.draw()

    def draw(self):
        if self.idx >= 0:
            self.canvas.delete(self.idx)

        self.point_start = [0, 0]
        self.point_end = [0, 0]

        self.point_start[0] = self.center[0] + 1000 * math.cos(self.angle * math.pi / 180)
        self.point_start[1] = self.center[1] + 1000 * math.sin(self.angle * math.pi / 180)

        self.point_end[0] = self.center[0] + 1000 * math.cos((180 + self.angle) * math.pi / 180)
        self.point_end[1] = self.center[1] + 1000 * math.sin((180 + self.angle) * math.pi / 180)

        self.idx = self.canvas.create_line(self.point_start[0], self.point_start[1], self.point_end[0], self.point_end[1], width=2, fill=self.color)

    def set_point(self, id, point):
        self.center = point.copy()
        self.id = id

        self.draw()

    def set_angle(self, angle):
        self.angle = angle

        # self.draw()

    # def rotation(self, angle):
    #     self.angle = angle
    #     for i in range(self.count):
    #         self.points[i][0] = self.center[0] + (self.initial_points[i][0] - self.center[0]) * math.cos(angle) - (
    #                 self.initial_points[i][1] - self.center[1]) * math.sin(angle)
    #         self.points[i][1] = self.center[1] + (self.initial_points[i][0] - self.center[0]) * math.sin(
    #             angle) + (self.initial_points[i][1] - self.center[1]) * math.cos(angle)
    #
    #     self.draw_lines()
    #     self.draw_points()

class Example(Frame):
    def __init__(self, parent):
        self.point_radius = radius

        Frame.__init__(self, parent)

        self.line_1 = False
        self.line_2 = False

        self.points = []
        self.points_ids = []

        self.canvas = Canvas(width=width, height=height, background="bisque")
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.reset = Button(parent, text="Reset", command= self.reset_canvas, width=20, height=2)
        self.process = Button(parent, text="Generate Lines", command=self.process, width=20, height=2)

        self.reset.grid(row=3, column=2, sticky=W)
        self.process.grid(row=1, column=1, sticky=W)

        self._drag_data = {"x": 0, "y": 0, "item": None, "id": -1}

        self.canvas.tag_bind("point", "<ButtonPress-3>", self.drag_start)
        self.canvas.tag_bind("point", "<ButtonRelease-3>", self.drag_stop)
        self.canvas.tag_bind("point", "<B3-Motion>", self.drag)
        self.canvas.bind("<Button-1>", self.create_point)

    def create_point(self, event):
        """Create a token at the given coordinate in the given color"""
        color = "#00FF0F"

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

    def drag_start(self, event):
        """Begining drag of an object"""
        # record the item and its location
        id = self.canvas.find_closest(event.x, event.y)[0]


        self._drag_data["item"] = id
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

        self._drag_data["id"] = self.is_intersection([event.x, event.y])

    def drag_stop(self, event):
        """End drag of an object"""
        # reset the drag information
        self.points[self._drag_data["id"]][0] = event.x
        self.points[self._drag_data["id"]][1] = event.y

        self._drag_data["item"] = None
        self._drag_data["id"] = -1
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def drag(self, event):
        """Handle dragging of an object"""
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]

        self.canvas.move(self._drag_data["item"], delta_x, delta_y)

        # record the new position
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

        self.points[self._drag_data["id"]][0] = event.x
        self.points[self._drag_data["id"]][1] = event.y

    def reset_canvas(self):
        self.points = []
        self.canvas.delete("all")

    def localization(self, point, poly):
        x = point[0]
        y = point[1]

        neighbors = []

        vertexes = poly.points

        count = len(vertexes)

        for i in range(count):
            x1 = vertexes[i][0]
            x2 = vertexes[(i + 1) % count][0]
            y1 = vertexes[i][1]
            y2 = vertexes[(i + 1) % count][1]

            if y2 > y and y1 <= y or y1 > y and y2 <= y:
                neighbors.append(((x1-x2) * y + x2 * y1 - x1 * y2)/(y1 - y2))

        if len(neighbors) < 2:
            return False
        else:
            left = []
            right = []

            for i in range(len(neighbors)):
                if x > neighbors[i]:
                    left.append(neighbors[i])
                elif x < neighbors[i]:
                    right.append(neighbors[i])

            if len(left) == len(right):
                if len(left) % 2:
                    return True
                else:
                    return False
            else:
                if len(left) % 2:
                    return True

                return False

    def is_intersection(self, point):
        for i in range(len(self.points)):
            x_condition = self.points[i][0] - self.point_radius <= point[0] and self.points[i][0] + self.point_radius >= point[0]
            y_condition = self.points[i][1] - self.point_radius <= point[1] and self.points[i][1] + self.point_radius >= point[1]

            if x_condition and y_condition:
                return i

        return -1

    def process(self):
        convex_poly = self.jarvismarch()

        convex_poly.pop()

        self.canvas.create_oval(
            convex_poly[0][0] - self.point_radius,
            convex_poly[0][1] - self.point_radius,
            convex_poly[0][0] + self.point_radius,
            convex_poly[0][1] + self.point_radius,
            outline='#FF0000',
            fill='#FF0000',
            tags=("point")
        )

        self.canvas.create_oval(
            convex_poly[1][0] - self.point_radius,
            convex_poly[1][1] - self.point_radius,
            convex_poly[1][0] + self.point_radius,
            convex_poly[1][1] + self.point_radius,
            outline='#0000FF',
            fill='#0000FF',
            tags=("point")
        )

        for point_id in range(len(convex_poly)):
            self.canvas.create_line(convex_poly[point_id][0],
                                    convex_poly[point_id][1],
                                    convex_poly[(point_id + 1) % len(convex_poly)][0],
                                    convex_poly[(point_id + 1) % len(convex_poly)][1])

        min_y = height
        max_y = 0
        min_point = -1
        max_point = -1

        for point_id in range(len(convex_poly)):
            if convex_poly[point_id][1] > max_y:
                max_y = convex_poly[point_id][1]
                max_point = [convex_poly[point_id].copy(), point_id]

            if convex_poly[point_id][1] < min_y:
                min_y = convex_poly[point_id][1]
                min_point = [convex_poly[point_id].copy(), point_id]

        self.line_1 = Line(min_point[0], min_point[1], self.canvas, '#00FF00')
        self.line_2 = Line(max_point[0], max_point[1], self.canvas, '#FF0000')

        summary_angle = 0

        min_distance = self.distance()
        min_angle = 0
        min_pt1_id = min_point[1]
        min_pt2_id = max_point[1]

        while summary_angle < 360:
            new_id_1 = (self.line_1.id + 1) % len(convex_poly)
            new_id_2 = (self.line_2.id + 1) % len(convex_poly)

            pt1 = [convex_poly[new_id_1], new_id_1]
            pt2 = [convex_poly[new_id_2], new_id_2]

            angle1 = self.get_angle(self.line_1.center, pt1[0].copy())
            angle2 = self.get_angle(self.line_2.center, pt2[0].copy())

            print('1' if angle1 < angle2 else '2')

            new_angle = angle1 if angle1 < angle2 else angle2

            summary_angle += new_angle

            self.line_1.set_angle(new_angle)
            self.line_2.set_angle(new_angle)

            if angle1 < angle2:
                self.line_1.set_point(pt1[1], pt1[0])

                new_id = self.get_far_point(self.line_1, convex_poly)

                self.line_2.set_point(new_id, convex_poly[new_id])

                print(pt1[1], new_id)
            else:
                self.line_2.set_point(pt2[1], pt2[0])

                new_id = self.get_far_point(self.line_2, convex_poly)

                self.line_1.set_point(new_id, convex_poly[new_id])

                print(new_id, pt2[1])

            distance = self.distance()

            if distance < min_distance:
                min_distance = distance
                min_angle = self.line_1.angle
                min_pt1_id = self.line_1.id
                min_pt2_id = self.line_2.id

        print(min_pt1_id, min_pt2_id, min_angle)


        self.line_1.set_angle(min_angle)
        self.line_2.set_angle(min_angle)

        self.line_1.color = '#0000FF'
        self.line_2.color = '#00FFFF'

        self.line_1.set_point(min_pt1_id, convex_poly[min_pt1_id])
        self.line_2.set_point(min_pt2_id, convex_poly[min_pt2_id])

    def line_intersection(self, line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')

        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return x, y

    def get_orientation(self, origin, p1, p2):
        difference = ((p2[0] - origin[0]) * (p1[1] - origin[1])) - (
                (p1[0] - origin[0]) * (p2[1] - origin[1])
        )
        return difference

    def jarvismarch(self):
        n = len(self.points)
        P = self.points
        min_point = self.points[0]
        H = []

        # find p1
        for i in range(1, n):
            if self.points[i][1] == min_point[1] and min_point[0] > self.points[i][0]:
                min_point = self.points[i]
            elif self.points[i][1] > min_point[1]:
                min_point = self.points[i]

        H.append(min_point)

        far_point = None
        point = min_point
        while far_point is not min_point:
            p1 = None
            for p in self.points:
                if p is point:
                    continue
                else:
                    p1 = p
                    break
            far_point = p1

            for p2 in self.points:
                if p2 is point or p2 is p1:
                    continue
                else:
                    direction = self.get_orientation(point, far_point, p2)
                    if direction > 0:
                        far_point = p2
            point = far_point
            H.append(far_point)
        print(H)
        return H

    def dist(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def distance(self,):
        tmp_point = [0, 0]

        tmp_point[0] = self.line_1.center[0] + 1000 * math.cos((90 + self.line_1.angle) * math.pi / 180)
        tmp_point[1] = self.line_1.center[1] + 1000 * math.sin((90 + self.line_1.angle) * math.pi / 180)

        intersection_point = self.line_intersection([self.line_2.point_start, self.line_2.point_end],
                                                    [tmp_point, self.line_1.center])

        return math.sqrt((intersection_point[0] - self.line_1.center[0]) ** 2 + (intersection_point[1] - self.line_1.center[1]) ** 2)

    def get_angle(self, point1, point2):
        angle_cos = math.acos((point2[0] - point1[0]) / self.dist(point1, point2))
        angle_sin = math.asin((point2[1] - point1[1]) / self.dist(point1, point2))

        if angle_sin >= 0:
            return angle_cos * 180 / math.pi
        else:
            return (2 * math.pi - angle_cos) * 180 / math.pi

    def get_far_point(self, line, points):
        distance = 0
        max_point_id = 0
        tmp_point = [0, 0]

        for point_id in range(len(points)):
            tmp_point[0] = points[point_id][0] + 1000 * math.cos((90 + line.angle) * math.pi / 180)
            tmp_point[1] = points[point_id][1] + 1000 * math.sin((90 + line.angle) * math.pi / 180)

            intersection_point = self.line_intersection([line.point_start, line.point_end],
                                                        [tmp_point, points[point_id]])
            current = self.dist(intersection_point, points[point_id])

            if current > distance:
                distance = current
                max_point_id = point_id

        return max_point_id


if __name__ == "__main__":
    root = Tk()
    r = Example(root)
    # Example(root).pack(fill="both", expand=True)
    r.grid()
    root.mainloop()
