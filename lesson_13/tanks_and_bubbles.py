from random import randint
import tkinter as tk

WIDTH, HEIGHT = 450, 380
DT = 0.5
GRAVITY_CONSTANT = 3
START_PAUSE = 1000
FRAME_TIME = 20  #microseconds
TANK_RADIUS = 25
MIN_BUBBLE_RADIUS = 30
MAX_BUBBLE_RADIUS = 40

# ========= Model ==========

class Tank:
    """ Танк, который будет порождать снаряды
        и тем самым сбивать пузыри.
    """
    def __init__(self, x, y, canvas):
        self.r = r = TANK_RADIUS
        self.x = x
        self.y = y
        self._canvas = canvas
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill="darkgreen")


class Shell:
    """ Снаряд, который летит под действием гравитации,
        вылетая за границу экрана просто исчезает.
    """
    def __init__(self, x, y, vx, vy, r, canvas):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self._canvas = canvas
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")


class Bubble:
    """ Пузырик, который разрушается снарядом,
        летает без действия гравитации,
        отражается от стенок
        и в идеале упруго отталкивается от других.
    """
    def __init__(self, x, y, vx, vy, r, canvas):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self._canvas = canvas
        self.id = canvas.create_oval(x - r, y - r, x + r, y + r, fill="cyan")

    def move(self):
        self._canvas.coords(self.id,
                            self.x - self.r, self.y - self.r,
                            self.x + self.r, self.y + self.r)
        self.x += self.vx * DT
        self.y += self.vy * DT

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

    def is_inside(self, other):
        """ Проверяет, находятся ли шарики в пересечении (столкновении). """
        dx = self.x - other.x
        dy = self.y - other.y
        squared_distance = dx**2 + dy**2
        squared_radius_sum = (self.r + other.r)**2
        return squared_distance <= squared_radius_sum

    def collide(self, other):
        """ Обмен скоростями при столновении. """
        self.vx, other.vx = other.vx, self.vx
        self.vy, other.vy = other.vy, self.vy
        # FIXME!

class GameRound:
    """ Игровой раунд.
        Здесь в атрибутах содержатся ссылки на:
        1. холст
        2. танк
        3. список текущих, "живых" снарядов
        4. список пузыриков
    """    
    def __init__(self, canvas, difficulty=1):
        assert difficulty < 10
        self._canvas = canvas
        self._tank = Tank(WIDTH // 2, HEIGHT, self._canvas)
        self._shells = []

        bubbles_number = difficulty * 5
        bubbles_max_speed = difficulty * 5
        self._targets = []
        for i in range(bubbles_number):
            r = randint(MIN_BUBBLE_RADIUS - difficulty,
                        MAX_BUBBLE_RADIUS - difficulty)
            x = randint(r + 1, WIDTH - 1 - r)
            y = randint(r + 1, HEIGHT - 1 - r)
            Vx = randint(-bubbles_max_speed, +bubbles_max_speed)
            Vy = randint(-bubbles_max_speed, +bubbles_max_speed)
            bubble = Bubble(x, y, Vx, Vy, r, self._canvas)
            self._targets.append(bubble)

    def handle_frame(self):
        for target in self._targets:
            target.move()
        # Попарное взаимодействие целей друг с другом
        for i in range(len(self._targets) - 1):
            for k in range(i + 1, len(self._targets)):
                target_1 = self._targets[i]
                target_2 = self._targets[k]
                if target_1.is_inside(target_2):
                    target_1.collide(target_2)

    def handle_click(self, event):
        print('handled click')

# ======== Control and View ========

class MainWindow:
    """ Главное окно.
        Содержит:
        1. ссылку на root = Tk()
        2. ссылку на экземпляр игрового раунда.
        3*. ссылки на все необходимые виджеты: кнопку, лэйбл с очками и т.п.
    """
    def __init__(self):
        self._root = tk.Tk()
        self._restart_button = tk.Button(self._root, text="Перезапустить игру",
                                         command=self._restart_button_handler)
        self._restart_button.pack()
        self._root.geometry(str(WIDTH + 10)+ 'x' + str(HEIGHT + 35))  # костыль!
        self._game = None

    def start_game(self):
        canvas = tk.Canvas(self._root, height=HEIGHT, width=WIDTH,
                           background="lightblue", border=3)
        canvas.pack()
        self._game = GameRound(canvas, 1)
        canvas.bind("<Button-1>", self._handle_click)
        canvas.after(START_PAUSE, self._handle_frame)

    def _handle_frame(self):
        if self._game is not None:
            self._game.handle_frame()
        self._root.after(FRAME_TIME, self._handle_frame)

    def _handle_click(self, event):
        if self._game is not None:
            self._game.handle_click(event)

    def _restart_button_handler(self):
        if self._game is None:
            self.start_game()
            print("Запустили игру...")
        else:
            print("Игра уже запущена!")

    def mainloop(self):
        self._root.mainloop()


def main():
    main_window = MainWindow()
    main_window.mainloop()
    print("Game over!")


main()
