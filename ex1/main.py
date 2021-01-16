from tkinter import *
import math
import random

width = 1000
height = 400

class Interface(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.canvas = Canvas(width=width, height=height, background="#CBC3F0")
        self.canvas.pack(fill="both", expand=True)

        self.d1_d2_label = Label(parent, text="D1 D2", font="Arial 14")
        self.d1_input = Entry(parent, width=20, bd=3)
        self.d2_input = Entry(parent, width=20, bd=3)

        self.r1_r2_label = Label(parent, text="R1 R2", font="Arial 14")
        self.r1_input = Entry(parent, width=20, bd=3)
        self.r2_input = Entry(parent, width=20, bd=3)

        self.input = Entry(root, width=20,bd=3)
        self.button = Button(root, command=self.create_poly, text="Создать", width=20, height=2)

        self.d1_d2_label.pack()
        self.d1_input.pack()
        self.d2_input.pack()
        self.r1_r2_label.pack()
        self.r1_input.pack()
        self.r2_input.pack()
        self.button.pack()

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

    def generate(self, d1, d2, r1, r2):
        center = [width / 2, height / 2]
        p = []
        f = [0]
        r = []

        for i in range(1000):
            delta = random.randrange(d1, d2)
            if f[i] + d1 > 360:
                return p

            while f[i] + delta >= 360:
                delta = random.randrange(d1, d2)

            f.append(f[i] + delta)
            r.append(random.randrange(r1, r2))

            q = [center[0] + r[i] * math.cos(f[i + 1] * math.pi / 180),
                center[1] + r[i] * math.sin(f[i + 1] * math.pi / 180)]

            p.append(q)

if __name__ == "__main__":
    root = Tk()
    Interface(root).pack(fill="both", expand=True)
    root.mainloop()