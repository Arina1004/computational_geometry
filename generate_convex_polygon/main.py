from tkinter import *
import math
import random

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.width = 1200
        self.height = 520
        self.eps = 15

        self.canvas = Canvas(width=self.width, height=self.height, background="bisque")
        self.canvas.pack(fill="both", expand=True)

        self.d1_d2_label = Label(parent, text="D1 D2", font="Arial 14")
        self.r1_r2_label = Label(parent, text="R1 R2", font="Arial 14")

        self.d1_ent = Entry(parent, width=20, bd=3)
        self.d2_ent = Entry(parent, width=20, bd=3)
        self.r1_ent = Entry(parent, width=20, bd=3)
        self.r2_ent = Entry(parent, width=20, bd=3)

        self.but = Button(parent,
            command=self.create_poly,
            text="Создать", # надпись на кнопке
            width=15, height=1,  # ширина и высота
            bg="white", fg="blue") # цвет фона и надписи

        self.d1_d2_label.pack()
        self.d1_ent.pack()
        self.d2_ent.pack()
        self.r1_r2_label.pack()
        self.r1_ent.pack()
        self.r2_ent.pack()
        self.but.pack()

    def create_poly(self):
        if self.d1_ent.get() and self.d2_ent.get() and self.r1_ent.get() and self.r2_ent.get():
            points = self.generate(int(self.d1_ent.get()), int(self.d2_ent.get()), int(self.r1_ent.get()), int(self.r2_ent.get()))

            for point_id in range(len(points)):
                self.canvas.create_oval(
                    points[point_id][0] - 5,
                    points[point_id][1] - 5,
                    points[point_id][0] + 5,
                    points[point_id][1] + 5,
                    outline="#FF0000",
                    fill="#FF0000",
                    tags=("point")
                )

                self.canvas.create_line(points[point_id][0],
                                        points[point_id][1],
                                        points[(point_id + 1) % len(points)][0],
                                        points[(point_id + 1) % len(points)][1])
        else:
            print('No')

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

    def check_if_lines_intersects(self, line1, line2):
        xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
        ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)

        if div == 0:
            return False

        return True

    def clip(self, x, min, max):
        if (min > max):
            return x
        elif (x < min):
            return min
        elif (x > max):
            return max
        else:
            return x

    def generate(self, d1, d2, r1, r2):
        p = [[self.width / 2 + int(random.random() * self.width / 2), int(random.random() * self.height / 2)]]

        f = [0]

        r = [0]

        for i in range(1, 100):
            delta = d1 + random.random() * (d2 - d1)

            f.append(f[i - 1] + delta)
            r.append(r1 + random.random() * (r2 - r1))

            q = [0, 0]

            q[0] = p[i - 1][0] + r[i] * math.cos(f[i] * math.pi / 180)
            q[1] = p[i - 1][1] + r[i] * math.sin(f[i] * math.pi / 180)

            if i > 1:
                angle_p1_q = 180 * self.get_angle(p[0], q) / math.pi

                angle_last_p1 = 180 * self.get_angle(p[i - 1], p[0]) / math.pi
				
				tmp = [0, 0]

                tmp[0] = p[i - 1][0] + r1 * math.cos(f[i] * math.pi / 180)
                tmp[1] = p[i - 1][1] + r1 * math.sin(f[i] * math.pi / 180)

                angle_p1_tmp = 180 * self.get_angle(p[0], q) / math.pi

                if (angle_p1_tmp < f[1] or angle_p1_tmp > 180 + f[1]):
                    print('oy')
                    return p

                if f[i - 1] + d1 >= angle_last_p1:
                    print('he')
                    return p

                while i > 1 and (angle_p1_q < f[1] or angle_p1_q > 180 + f[1]) or (f[i] > angle_last_p1):
                    delta = d1 + random.random() * (d2 - d1)

                    f[i] = f[i - 1] + delta
                    r[i] = r1 + random.random() * (r2 - r1)

                    q = [0, 0]

                    q[0] = p[i - 1][0] + r[i] * math.cos(f[i] * math.pi / 180)
                    q[1] = p[i - 1][1] + r[i] * math.sin(f[i] * math.pi / 180)

                p.append(q)

                if int(angle_last_p1) == int(180 + angle_p1_q):
                    print('!!!!', len(p))
                    return p
            else:
                p.append(q)

            if self.distance(q, p[0]) < self.eps:
                print(f)
                print(180 * self.get_angle(p[-1], p[0]) / math.pi)
                return p

    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def get_angle(self, point1, point2):
        angle_cos = math.acos((point2[0] - point1[0]) / self.distance(point1, point2))
        angle_sin = math.asin((point2[1] - point1[1]) / self.distance(point1, point2))

        if angle_sin >= 0:
            return angle_cos
        else:
            return 2 * math.pi - angle_cos

    def is_right_side(self, start, point):
        pass
if __name__ == "__main__":
    root = Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()