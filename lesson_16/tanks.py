import lesson_16.shells as shells
from lesson_16.constants import *


class Tank:
    """ Танк, который будет порождать снаряды
        и тем самым сбивать пузыри.
    """

    def __init__(self, x, y, canvas):
        self.r = r = TANK_RADIUS
        self.muzzle_l = TANK_RADIUS * 2
        self.x = x
        self.y = y
        self.muzzle_dx = 0
        self.muzzle_dy = -self.muzzle_l
        self._canvas = canvas
        self._muzzle_id = canvas.create_line(x, y, x + self.muzzle_dx, y + self.muzzle_dy, width=MUZZLE_WIDTH)
        self._turret_id = canvas.create_oval(x - r, y - r, x + r, y + r, fill="darkgreen")

    def aim(self, event_x, event_y):
        """ Прицеливание дула по направлению к точке (event_x, event_y)
            Используется подобобие треугольников по двум углам.
            muzzle_l / length == muzzle_dx / dx == muzzle_dy / dy
        """
        dx = event_x - self.x
        dy = event_y - self.y
        length = (dx**2 + dy**2) ** 0.5
        self.muzzle_dx = self.muzzle_l / length * dx
        self.muzzle_dy = self.muzzle_l / length * dy
        self._canvas.coords(self._muzzle_id, self.x, self.y, self.x + self.muzzle_dx, self.y + self.muzzle_dy)

    def can_shoot(self):
        return True  # fixme: хорошо бы считать сколько снарядов осталось

    def shoot(self, x, y):
        self.aim(x, y)
        velocity = SHELL_START_VELOCITY
        vx = velocity * self.muzzle_dx / self.muzzle_l
        vy = velocity * self.muzzle_dy / self.muzzle_l
        shell = shells.Shell(self.x + self.muzzle_dx, self.y + self.muzzle_dy, vx, vy,
                      MUZZLE_WIDTH // 2, self._canvas)
        return shell

    def is_zombie(self):
        return False  # В данный момент танк не имеет параметра "здоровье" и не может умереть

    def get_damage(self, shell):
        pass  # В данный момент танк не имеет параметра "здоровье" и не может получать дамагу...

    def is_inside(self, other):
        """ Проверяет, находятся ли шарики в пересечении (столкновении). """
        dx = self.x - other.x
        dy = self.y - other.y
        squared_distance = dx ** 2 + dy ** 2
        squared_radius_sum = (self.r + other.r) ** 2
        return squared_distance <= squared_radius_sum
