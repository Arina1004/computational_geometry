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

        self.ent = Entry(root, width=20,bd=3)
        self.but = Button(root,
            command=self.create_poly,
            text="Создать", # надпись на кнопке
            width=15, height=1,  # ширина и высота
            bg="white", fg="blue") # цвет фона и надписи

        self.ent.pack()
        self.but.pack()

    def create_poly(self):
        if self.ent.get():

            points = self.generate_polygon( ctrX=int(random.random() * self.width), ctrY=int(random.random() * self.height),
                                            aveRadius=100, numVerts=int(self.ent.get()) )

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

    def generate_polygon(self, ctrX, ctrY, aveRadius,numVerts):
        irregularity = random.random()
        spikeyness = random.random()

        irregularity = self.clip(irregularity, 0, 1) * 2 * math.pi / numVerts
        spikeyness = self.clip(spikeyness, 0, 1) * aveRadius

        # generate n angle steps
        angleSteps = []
        lower = (2 * math.pi / numVerts) - irregularity
        upper = (2 * math.pi / numVerts) + irregularity
        sum = 0
        for i in range(numVerts):
            tmp = random.uniform(lower, upper)
            angleSteps.append(tmp)
            sum = sum + tmp

        # normalize the steps so that point 0 and point n+1 are the same
        k = sum / (2 * math.pi)
        for i in range(numVerts):
            angleSteps[i] = angleSteps[i] / k

        # now generate the points
        points = []
        angle = random.uniform(0, 2 * math.pi)
        for i in range(numVerts):
            r_i = self.clip(random.gauss(aveRadius, spikeyness), 0, 2 * aveRadius)
            x = self.clip(ctrX + r_i * math.cos(angle), 0, self.width)
            y = self.clip(ctrY + r_i * math.sin(angle), 0, self.height)
            points.append((int(x), int(y)))

            angle = angle + angleSteps[i]

        return points

    def clip(self, x, min, max):
        if (min > max):
            return x
        elif (x < min):
            return min
        elif (x > max):
            return max
        else:
            return x

if __name__ == "__main__":
    root = Tk()
    Example(root).pack(fill="both", expand=True)
    root.mainloop()