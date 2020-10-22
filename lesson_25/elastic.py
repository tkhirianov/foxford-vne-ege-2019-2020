# coding=utf-8

import tkinter as tk

WIDTH, HEIGHT = 450, 380
FPS = 25
DT = 1/25
R0 = (100, 100)
V0X = 10
NORMAL_SPRING_LENGTH = 40
HOOKE_CONSTANT = 10


# ========= Model ==========
def force(x1, y1, x2, y2):
    distance = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
    nx = (x2 - x1) / distance
    ny = (y2 - y1) / distance
    f = (distance - NORMAL_SPRING_LENGTH) * HOOKE_CONSTANT
    fx = f * nx
    fy = f * ny
    return fx, fy


class MaterialPoint:
    def __init__(self, x, y, vx, vy, r, m):
        self.m = m
        self.r = r
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill="cyan")

    def move(self, force_x, force_y):
        ax, ay = force_x / self.m, force_y / self.m
        self.x += self.vx * DT + ax * DT ** 2 / 2
        self.y += self.vy * DT + ay * DT ** 2 / 2
        self.vx += ax * DT
        self.vy += ay * DT

    def show(self):
        canvas.coords(self.id,
                      self.x - self.r, self.y - self.r,
                      self.x + self.r, self.y + self.r)

    def delete(self):
        canvas.delete(self.id)


class ElasticBody:
    def __init__(self, x0, y0, w_num, h_num, width, height):
        self.h_num = h_num
        self.w_num = w_num
        self.M = [[None] * self.w_num for i in range(self.h_num)]
        for i in range(self.h_num):
            for k in range(self.w_num):
                x = x0 + (width / (self.w_num - 1)) * k
                y = y0 + (height / (self.h_num - 1)) * i
                self.M[i][k] = MaterialPoint(x, y, 0, 0, 5, 1)

    def show(self):
        for i in range(self.h_num):
            for k in range(self.w_num):
                self.M[i][k].show()

    def move(self):
        # вычисление всех сил упругости:
        f = [[None] * self.w_num for i in range(self.h_num)]
        for i in range(self.h_num):
            for k in range(self.w_num):
                fx, fy = 0, 0
                if i != 0:
                    dfx, dfy = force(self.M[i][k].x, self.M[i][k].y, self.M[i-1][k].x, self.M[i-1][k].y)
                    fx, fy = fx + dfx, fy + dfy
                if i != self.h_num - 1:
                    dfx, dfy = force(self.M[i][k].x, self.M[i][k].y, self.M[i+1][k].x, self.M[i+1][k].y)
                    fx, fy = fx + dfx, fy + dfy
                if k != 0:
                    dfx, dfy = force(self.M[i][k].x, self.M[i][k].y, self.M[i][k-1].x, self.M[i][k-1].y)
                    fx, fy = fx + dfx, fy + dfy
                if k != self.w_num - 1:
                    dfx, dfy = force(self.M[i][k].x, self.M[i][k].y, self.M[i][k+1].x, self.M[i][k+1].y)
                    fx, fy = fx + dfx, fy + dfy

                f[i][k] = (fx, fy)

        # сдвиги всех точек с учётом вычисленных сил упругости:
        for i in range(self.h_num):
            for k in range(self.w_num):
                self.M[i][k].move(*f[i][k])


def start_button_handler():
    print("Modelling started...")
    canvas.after(10, world_calculation_step)
    canvas.after(10, world_presentation_step)


def world_calculation_step():
    global t
    for obj in objects:
        obj.move()
    t += DT
    canvas.after(int(1000 * DT), world_calculation_step)


def world_presentation_step():
    for obj in objects:
        obj.show()
    canvas.after(int(1000 / FPS), world_presentation_step)


def initialization():
    global root, canvas, objects, t
    root = tk.Tk()
    # создаём холст:
    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, background="gray", border=0)
    canvas.pack()
    # привязка событий:
    restart_button = tk.Button(root, text="Перезапустить игру", command=start_button_handler)
    restart_button.pack()

    w_num = 6
    h_num = 5
    body = ElasticBody(*R0, w_num, h_num,
                       NORMAL_SPRING_LENGTH*(w_num-1), NORMAL_SPRING_LENGTH*(h_num-1))

    body.M[1][0].vx = V0X  # сообщаю скорость конкретной точке!
    body.M[2][0].vx = V0X  # сообщаю скорость конкретной точке!
    body.M[3][0].vx = V0X  # сообщаю скорость конкретной точке!
    objects = [body]

    t = 0


def main():
    initialization()
    root.mainloop()
    print("Modelling over!")


main()
