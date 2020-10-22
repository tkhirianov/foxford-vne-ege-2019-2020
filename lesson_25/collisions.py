# coding=utf-8

import tkinter as tk

WIDTH, HEIGHT = 450, 380
FPS = 25
DT = 0.01
GRAVITY_CONSTANT = 3
R0 = (300, 100)
V0 = (0, 25)
R1 = (400, 200)
V1 = (-25, 0)


# ========= Model ==========
def forces(x, y, vx, vy, t, m):
    fx = 0
    fy = 0 # -(y - R0[1]) * 0.1
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
        if self.y <= self.r:
            self.y = self.r
            self.vy = -self.vy
        if self.y >= HEIGHT - self.r - 1:
            self.y = HEIGHT - self.r - 1
            self.vy = -self.vy

    def show(self):
        # print(t, self.x - R0[0], self.y - R0[1], self.vx, self.vy, sep='\t')  # DEBUG PRINT
        canvas.coords(self.id,
                      self.x - self.r, self.y - self.r,
                      self.x + self.r, self.y + self.r)

    def delete(self):
        canvas.delete(self.id)

    def is_inside(self, other):
        """ Проверяет, находятся ли шарики в пересечении (столкновении). """
        dx = self.x - other.x
        dy = self.y - other.y
        squared_distance = dx**2 + dy**2
        squared_radius_sum = (self.r + other.r)**2
        return squared_distance <= squared_radius_sum

    def collide(self, other):
        """ Обмен скоростями при столновении. """
        dx, dy = (other.x - self.x, other.y - self.y)
        distance = (dx ** 2 + dy ** 2) ** 0.5
        nx, ny = (dx / distance, dy / distance)
        print(nx**2 + ny**2)
        v1_normal = self.vx * nx + self.vy * ny
        v2_normal = other.vx * nx + other.vy * ny
        # обмен нормальными компонентами скорости
        v1_new_normal = v2_normal
        v2_new_normal = v1_normal

        self.vx += (v1_new_normal - v1_normal) * nx
        self.vy += (v1_new_normal - v1_normal) * ny
        other.vx += (v2_new_normal - v2_normal) * nx
        other.vy += (v2_new_normal - v2_normal) * ny



def start_button_handler():
    print("Modelling started...")
    canvas.after(10, world_calculation_step)
    canvas.after(10, world_presentation_step)


def world_calculation_step():
    global t
    for obj in objects:
        obj.move()
    # Попарное взаимодействие целей друг с другом
    for i in range(len(objects) - 1):
        for k in range(i + 1, len(objects)):
            target_1 = objects[i]
            target_2 = objects[k]
            if target_1.is_inside(target_2):
                target_1.collide(target_2)
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

    objects = [MaterialPoint(*R0, *V0, 50, 1),
               MaterialPoint(*R1, *V1, 50, 1)]
    t = 0


def main():
    initialization()
    root.mainloop()
    print("Modelling over!")


main()
