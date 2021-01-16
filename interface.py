from tkinter import *
import math
from ex3.main import is_convex
from ex4.main1 import localization as localization_n
from ex4.main2 import localization as localization_logn
from ex5.main import clockwise
from ex6.main import localization_with_turn
from ex8.main import convex_hull
from ex9.main import jarvismarch
from ex10.main import graham_scan
from ex11.main import scan

radius = 3
width = 1000
height = 400

class Polygon(object):
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

    def calculate_center(self):
        summa_x = 0
        summa_y = 0

        for i in range(self.count):
            summa_x += self.points[i][0]
            summa_y += self.points[i][1]

        self.center = [summa_x // self.count, summa_y // self.count]

    def draw_lines(self, color='black'):
        for line in self.lines_ids:
            self.canvas.delete(line)

        self.lines_ids = []

        for point_id in range(self.count):
            self.lines_ids.append(self.canvas.create_line(self.points[point_id][0],
                           self.points[point_id][1],
                           self.points[(point_id + 1) % self.count][0],
                           self.points[(point_id + 1) % self.count][1], fill=color, width=2))

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
                outline="#6C60A1",
                fill="#6C60A1",
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


class Interface(Frame):
    def __init__(self, parent):
        self.poly = False
        self.point_radius = radius

        Frame.__init__(self, parent)

        self.mode = 'init'

        self.points = []
        self.points_ids = []

        self.canvas = Canvas(width=width, height=height, background="#CBC3F0")
        self.canvas.grid(row=0, column=0, columnspan=3)

        self.scale = Scale(parent, digits=3,command=self.change_scale, orient=HORIZONTAL, length=300, from_=0.25, to=2,
                           tickinterval=0.25, resolution=0.05, label="Масштаб")
        self.scale.set(1)

        self.rotation = Scale(parent, digits=3, command=self.rotate, orient=HORIZONTAL, length=400, from_=-180,
                           to=180,
                           tickinterval=30, resolution=1, label="Поворот")

        self.reset = Button(parent, text="Очистить", command= self.reset_canvas, width=20, height=2)

        self.scale.grid(row=2, column=0, columnspan=2, sticky=W)
        self.rotation.grid(row=2, column=1, columnspan=2, sticky=W, padx=40)
        self.reset.grid(row=2, column=2, sticky=E)

        self.convex = Button(parent, text="3. Выпуклость", command= self.is_convex, width=20, height=2)
        self.convex.grid(row=3, column=0, columnspan=2, sticky=W, pady=10)

        self.localizationN = Button(parent, text="4.1 Локализация (n)", command= self.localization_n, width=20, height=2)
        self.localizationN.grid(row=3, column=1, columnspan=2, sticky=W)

        self.localizationLOGN = Button(parent, text="4.2 Локализация (log n)", command= self.localization_logn, width=20, height=2)
        self.localizationLOGN.grid(row=3, column=2, columnspan=2, sticky=W)

        self.clockwise = Button(parent, text="5. Направление", command= self.determine_clockwise, width=20, height=2)
        self.clockwise.grid(row=4, column=0, columnspan=2, sticky=W, pady=10)

        self.localizationWT = Button(parent, text="6. Локализация (п)", command= self.localization_wt, width=20, height=2)
        self.localizationWT.grid(row=4, column=1, columnspan=2, sticky=W)

        self.convexH = Button(parent, text="8. Оболочка", command= self.convex_hull, width=20, height=2)
        self.convexH.grid(row=5, column=0, columnspan=2, sticky=W)

        self.jarvismarchB = Button(parent, text="9. Джарвис", command= self.jarvismarch, width=20, height=2)
        self.jarvismarchB.grid(row=5, column=1, columnspan=2, sticky=W)

        self.grahamB = Button(parent, text="10. Грехем", command= self.graham, width=20, height=2)
        self.grahamB.grid(row=5, column=2, columnspan=2, sticky=W)

        self.iterB = Button(parent, text="11. Итерационный", command= self.convex_iter, width=20, height=2)
        self.iterB.grid(row=5, column=3, columnspan=2, sticky=W)

        self._drag_data = {"x": 0, "y": 0, "item": None, "id": -1, "is_poly": False}

        self.canvas.tag_bind("point", "<ButtonPress-3>", self.drag_start)
        self.canvas.tag_bind("point", "<ButtonRelease-3>", self.drag_stop)
        self.canvas.tag_bind("point", "<B3-Motion>", self.drag)
        self.canvas.bind("<ButtonPress-2>", self.create_poly)
        self.canvas.bind("<Button-1>", self.create_point)

    def create_point(self, event):
        color = "#6C60A1"

        if self.poly:
          if self.mode == 'localization_n':
            color = "#60A181" if localization_n(self.poly.points, [event.x, event.y]) else "#6C60A1"
          elif self.mode == 'localization_logn':
            color = "#60A181" if localization_logn(self.poly.points, self.poly.center, [event.x, event.y]) else "#6C60A1"
          elif self.mode == 'localization_wt':
            color = "#60A181" if localization_with_turn(self.poly.points, [event.x, event.y], 1.5) else "#6C60A1"

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

    def create_poly(self, event):
        if not self.poly:
            self.poly = Polygon(self.points, self.points_ids, self.canvas)

            self.points = []
            self.points_ids = []

    def drag_start(self, event):
        self._drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
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
        delta_x = event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]

        self.canvas.move(self._drag_data["item"], delta_x, delta_y)

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
        self.mode = 'init'
        self.points = []
        self.points_ids = []
        self.canvas.delete("all")

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

    def localization_n(self):
        self.mode = 'localization_n'
        self.recalculate_colors()
    
    def localization_logn(self):
        self.mode = 'localization_logn'
        self.recalculate_colors()

    def change_color(self, id, color):
        self.canvas.itemconfig(id, fill=color, outline=color)

    def recalculate_colors(self):
        for i in range(len(self.points)):
          predicted_color = "#6C60A1"
          if self.mode == 'localization_n':
            predicted_color = "#60A181" if localization_n(self.poly.points, self.points[i]) else "#6C60A1"
          elif self.mode == 'localization_logn':
            predicted_color = "#60A181" if localization_logn(self.poly.points, self.poly.center, self.points[i]) else "#6C60A1"
          elif self.mode == 'localization_wt':
            predicted_color = "#60A181" if localization_with_turn(self.poly.points, self.points[i], 1.5) else "#6C60A1"
          if self.points[i][2] != predicted_color:
              self.change_color(self.points_ids[i], predicted_color)
              self.points[i][2] = predicted_color

    def is_convex(self):
      self.mode = 'convex'
      color = '#867ABF' if is_convex(self.poly.get_points()) else '#CA6F6F'
      self.poly.draw_lines(color)

    def determine_clockwise(self):
      result = 'По ЧС' if clockwise(self.poly.points) else 'Не по ЧС'
      self.canvas.create_text(50, 20, text=result)
    
    def localization_wt(self):
      self.mode = 'localization_wt'
      self.recalculate_colors()

    def convex_hull(self):
      self.mode = 'convex_hull'
      self.poly = False
      self.points_ids = []
      color = "#6C60A1"
      self.canvas.delete('all')
      for p in self.points:
        self.points_ids.append(self.canvas.create_oval(
            p[0] - self.point_radius,
            p[1] - self.point_radius,
            p[0]+ self.point_radius,
            p[1] + self.point_radius,
            outline=color,
            fill=color,
            tags=("point")
        ))
      result = convex_hull(self.points)
      b_points = result[0]
      b_points_id = []
      print(result)
      for point in b_points:
        b_points_id.append(self.points_ids[self.points.index(point)])

      self.poly = Polygon(b_points, b_points_id, self.canvas)
      self.canvas.create_oval(
          result[1][0] - self.point_radius,
          result[1][1] - self.point_radius,
          result[1][0]+ self.point_radius,
          result[1][1] + self.point_radius,
          outline='#E8A4DB',
          fill='#E380D1',
          tags=("point")
      )

    def jarvismarch(self):
      self.mode = 'jarvismarch'
      self.poly = False
      self.points_ids = []
      color = "#6C60A1"
      self.canvas.delete('all')
      for p in self.points:
        self.points_ids.append(self.canvas.create_oval(
            p[0] - self.point_radius,
            p[1] - self.point_radius,
            p[0]+ self.point_radius,
            p[1] + self.point_radius,
            outline=color,
            fill=color,
            tags=("point")
        ))
      b_points = jarvismarch(self.points)
      b_points_id = []
      for point in b_points:
        b_points_id.append(self.points_ids[self.points.index(point)])

      self.poly = Polygon(b_points, b_points_id, self.canvas)

    def graham(self):
      self.mode = 'graham'
      self.poly = False
      self.points_ids = []
      color = "#6C60A1"
      self.canvas.delete('all')
      for p in self.points:
        self.points_ids.append(self.canvas.create_oval(
            p[0] - self.point_radius,
            p[1] - self.point_radius,
            p[0]+ self.point_radius,
            p[1] + self.point_radius,
            outline=color,
            fill=color,
            tags=("point")
        ))
      b_points = graham_scan(self.points)
      b_points_id = []
      for point in b_points:
        b_points_id.append(self.points_ids[self.points.index(point)])

      self.poly = Polygon(b_points, b_points_id, self.canvas)
      
    def convex_iter(self):
      self.mode = 'iter'
      self.poly = False
      self.points_ids = []
      color = "#6C60A1"
      self.canvas.delete('all')
      for p in self.points:
        self.points_ids.append(self.canvas.create_oval(
            p[0] - self.point_radius,
            p[1] - self.point_radius,
            p[0]+ self.point_radius,
            p[1] + self.point_radius,
            outline=color,
            fill=color,
            tags=("point")
        ))
      b_points = scan(self.points)
      b_points_id = []
      for point in b_points:
        b_points_id.append(self.points_ids[self.points.index(point)])

      self.poly = Polygon(b_points, b_points_id, self.canvas)

if __name__ == "__main__":
    root = Tk()
    Interface(root).grid()
    root.mainloop()
