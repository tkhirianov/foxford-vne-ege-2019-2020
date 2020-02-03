from lesson_16.constants import *


class Shell:
    """ Снаряд, который летит под действием гравитации,
        вылетая за границу экрана просто исчезает.
    """

    def __init__(self, x, y, vx, vy, r, canvas):
        self._zombie = False
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self._timeout = 200  # fixme: откалибровать по геймплею
        self._canvas = canvas
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")

    def move(self):
        self._timeout -= 1
        if self._timeout <= 0:
            self.destroy()
        self.x += self.vx * DT
        self.y += self.vy * DT + GRAVITY_CONSTANT * DT**2 / 2
        self.vy += GRAVITY_CONSTANT * DT

        if self.x < self.r:
            self.x = self.r
            self.vx = -self.vx
        if self.x > WIDTH - self.r:
            self.x = WIDTH - self.r
            self.vx = -self.vx
        if self.y < self.r:
            self.y = self.r
            self.vy = -self.vy
        if self.y > HEIGHT - self.r:
            self.y = HEIGHT - self.r
            self.vy = -self.vy

        self._canvas.coords(self.id,
                            self.x - self.r, self.y - self.r,
                            self.x + self.r, self.y + self.r)

    def check_hit(self, target):
        return target.is_inside(self)

    def destroy(self):
        self._zombie = True
        self._canvas.delete(self.id)

    def calculate_damage(self, target):
        self.destroy()
        return 10  # Некий урон, зависящий от точности попадания в target

    def is_zombie(self):
        return self._zombie
