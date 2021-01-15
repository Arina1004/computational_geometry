from tkinter import *
import math
import random

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.width = 1280
        self.height = 520

        self.canvas = Canvas(width=self.width, height=self.height, background="bisque")
        self.canvas.pack(fill="both", expand=True)

        self.d1_d2_label = Label(parent, text="D1 D2", font="Arial 14")
        self.r1_r2_label = Label(parent, text="R1 R2", font="Arial 14")

        self.d1_ent = Entry(parent, width=20, bd=3)
        self.d2_ent = Entry(parent, width=20, bd=3)
        self.r1_ent = Entry(parent, width=20, bd=3)
        self.r2_ent = Entry(parent, width=20, bd=3)

        self.ent = Entry(root, width=20,bd=3)
        self.but = Button(root,
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

            points = self.generate( int(self.d1_ent.get()), int(self.d2_ent.get()), int(self.r1_ent.get()), int(self.r2_ent.get()))

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

    def generate(self, d1, d2, r1, r2):
        ctr = [int(random.random() * self.width / 2), int(random.random() * self.height / 2)]

        p = []

        f = [0]

        r = []

        for i in range(1000):
            delta = d1 + random.random() * (d2 - d1)

            if f[i] + d1 > 360:
                return p

            while f[i] + delta >= 360:
                delta = d1 + random.random() * (d2 - d1)

            f.append(f[i] + delta)
            r.append(r1 + random.random() * (r2 - r1))

            q = [0, 0]

            q[0] = ctr[0] + r[i] * math.cos(f[i + 1] * math.pi / 180)
            q[1] = ctr[1] + r[i] * math.sin(f[i + 1] * math.pi / 180)

            # if i > 1:
            #     angle_p1_q = 180 * self.get_angle(p[0], q) / math.pi
            #
            #     angle_last_p1 = 180 * self.get_angle(p[i - 1], p[0]) / math.pi
            #
            #     if f[i - 1] + d1 >= angle_last_p1:
            #         print('he')
            #         return p
            #
            #     while i > 1 and (angle_p1_q < f[1] or angle_p1_q > 180 + f[1]) or (f[i] > angle_last_p1):
            #         delta = d1 + random.random() * (d2 - d1)
            #
            #         f[i] = f[i - 1] + delta
            #         r[i] = r1 + random.random() * (r2 - r1)
            #
            #         q = [0, 0]
            #
            #         q[0] = ctr[0] + r[i] * math.cos(f[i] * math.pi / 180)
            #         q[1] = ctr[1] + r[i] * math.sin(f[i] * math.pi / 180)
            #
            #     p.append(q)
            #
            #     if int(angle_last_p1) == int(180 + angle_p1_q):
            #         print('!!!!', len(p))
            #         return p
            # else:

            p.append(q)

if __name__ == "__main__":
    root = Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()