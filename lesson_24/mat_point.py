# coding=utf-8

import tkinter as tk

WIDTH, HEIGHT = 450, 380
FPS = 5
DT = 0.002
GRAVITY_CONSTANT = 3
R0 = (100, 100)
V0 = (5, 5)


# ========= Model ==========
def forces(x, y, vx, vy, t, m):
    fx = 0
    fy = -(y - R0[1]) * 0.1
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

    def move(self):
        ax, ay = forces(self.x, self.y, self.vx, self.vy, t, self.m)
        self.x += self.vx * DT + ax * DT ** 2 / 2
        self.y += self.vy * DT + ay * DT ** 2 / 2
        self.vx += ax * DT
        self.vy += ay * DT

        if self.x <= self.r:
            self.x = self.r
            self.vx = -self.vx
        if self.x >= WIDTH - self.r - 1:
            self.x = WIDTH - self.r - 1
            self.vx = -self.vx
        if self.y >= HEIGHT - self.r - 1:
            self.y = HEIGHT - self.r - 1
            self.vy = -self.vy

    def show(self):
        print(t, self.x - R0[0], self.y - R0[1], self.vx, self.vy, sep='\t')  # DEBUG PRINT
        canvas.coords(self.id,
                      self.x - self.r, self.y - self.r,
                      self.x + self.r, self.y + self.r)

    def delete(self):
        canvas.delete(self.id)


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
    canvas.after(int(1000/FPS), world_presentation_step)


def initialization():
    global root, canvas, objects, t
    root = tk.Tk()
    # создаём холст:
    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH, background="gray", border=0)
    canvas.pack()
    # привязка событий:
    restart_button = tk.Button(root, text="Перезапустить игру", command=start_button_handler)
    restart_button.pack()

    objects = [MaterialPoint(*R0, *V0, 5, 1)]
    t = 0


def main():
    initialization()
    root.mainloop()
    print("Modelling over!")


main()
