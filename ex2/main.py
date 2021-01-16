from tkinter import *
import math
import random

width = 1000
height = 400

class Interface(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.eps = 15

        self.canvas = Canvas(width=width, height=height, background="#CBC3F0")
        self.canvas.pack(fill="both", expand=True)

        self.d1_d2_label = Label(parent, text="D1 D2", font="Arial 14")
        self.d1_input = Entry(parent, width=20, bd=3)
        self.d2_input = Entry(parent, width=20, bd=3)

        self.r1_r2_label = Label(parent, text="R1 R2", font="Arial 14")
        self.r1_input = Entry(parent, width=20, bd=3)
        self.r2_input = Entry(parent, width=20, bd=3)

        self.but = Button(parent, command=self.create_poly, text="Создать", width=20, height=2)

        self.d1_d2_label.pack()
        self.d1_input.pack()
        self.d2_input.pack()
        self.r1_r2_label.pack()
        self.r1_input.pack()
        self.r2_input.pack()
        self.but.pack()

    def create_poly(self):
        self.canvas.delete('all')
        if self.d1_input.get() and self.d2_input.get() and self.r1_input.get() and self.r2_input.get():
            points = self.generate(int(self.d1_input.get()), int(self.d2_input.get()), int(self.r1_input.get()), int(self.r2_input.get()))

            for point_id in range(len(points)):
                self.canvas.create_oval(
                    points[point_id][0] - 3,
                    points[point_id][1] - 3,
                    points[point_id][0] + 3,
                    points[point_id][1] + 3,
                    outline="#6C60A1",
                    fill="#6C60A1",
                    tags=("point")
                )

                self.canvas.create_line(points[point_id][0],
                                        points[point_id][1],
                                        points[(point_id + 1) % len(points)][0],
                                        points[(point_id + 1) % len(points)][1])
        else:
            print('Error')

    def distance(self, p1, p2):
        return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

    def get_angle(self, point1, point2):
        angle_cos = math.acos((point2[0] - point1[0]) / self.distance(point1, point2))
        angle_sin = math.asin((point2[1] - point1[1]) / self.distance(point1, point2))

        if angle_sin >= 0:
            return angle_cos
        else:
            return 2 * math.pi - angle_cos

    def generate(self, d1, d2, r1, r2):
        p = [[width / 2, height / 2]]
        f = [0]
        r = [0]

        for i in range(1, 100):
            f.append(f[i - 1] + random.randrange(d1, d2))
            r.append(random.randrange(r1, r2))

            q = [p[i - 1][0] + r[i] * math.cos(f[i] * math.pi / 180),
                p[i - 1][1] + r[i] * math.sin(f[i] * math.pi / 180)]

            if i > 1:
                angle_p1_q = 180 * self.get_angle(p[0], q) / math.pi
                angle_pi1_p1 = 180 * self.get_angle(p[i - 1], p[0]) / math.pi
                tmp = [p[i - 1][0] + r1 * math.cos(f[i] * math.pi / 180),
                    p[i - 1][1] + r1 * math.sin(f[i] * math.pi / 180)]

                angle_p1_tmp = 180 * self.get_angle(p[0], tmp) / math.pi

                if (angle_p1_tmp < f[1] or angle_p1_tmp > 180 + f[1]):
                    return p

                if f[i - 1] + d1 >= angle_pi1_p1:
                    return p

                while i > 1 and (angle_p1_q < f[1] or angle_p1_q > 180 + f[1]) or (f[i] > angle_pi1_p1):
                    delta = random.randrange(d1, d2)

                    f[i] = f[i - 1] + delta
                    r[i] = random.randrange(r1, r2)

                    q = [p[i - 1][0] + r[i] * math.cos(f[i] * math.pi / 180),
                        p[i - 1][1] + r[i] * math.sin(f[i] * math.pi / 180)]

                p.append(q)

                if int(angle_pi1_p1) == int(180 + angle_p1_q):
                    return p
            else:
                p.append(q)

            if self.distance(q, p[0]) < self.eps:
                return p


if __name__ == "__main__":
    root = Tk()
    Interface(root).pack(fill="both", expand=True)
    root.mainloop()