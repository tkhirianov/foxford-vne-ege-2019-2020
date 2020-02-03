import lesson_16.tanks as tanks
import lesson_16.shells as shells
from lesson_16.constants import *


class GameRound:
    """ Игровой раунд.
        Здесь в атрибутах содержатся ссылки на:
        1. холст
        2. танк
        3. список текущих, "живых" снарядов
        4. список пузыриков
    """

    def __init__(self, canvas, difficulty=1, players_number=2):
        assert difficulty < 10
        self._canvas = canvas
        self._players_number = players_number
        self._current_player = 0
        self._tanks = []
        for i in range(players_number):
            x = WIDTH // (players_number + 1) * (i + 1)
            y = HEIGHT
            tank = tanks.Tank(x, y, self._canvas)
            self._tanks.append(tank)
        self._shell = None

        canvas.after(START_PAUSE, self._handle_frame)
        canvas.bind("<Motion>", self._handle_move)
        canvas.bind("<Button-1>", self._handle_click)

    def _next_player(self):
        self._current_player = (self._current_player + 1) % self._players_number

    def _handle_frame(self):
        if self._shell is not None:
            # расчёт перемещения снаряда
            self._shell.move()
            # расчёт взаимодействия снаряда со всеми танками
            for tank in self._tanks:
                if self._shell.check_hit(tank):
                    damage = self._shell.calculate_damage(tank)
                    tank.get_damage(damage)

            if self._shell.is_zombie():
                self._shell = None
                self._next_player()
                for tank in self._tanks:
                    if tank.is_zombie():
                        print("OOOPS! Need to check if it\'s game over. And this tank shouldn\'t fire")

        self._canvas.after(FRAME_TIME, self._handle_frame)

    def _handle_move(self, event):
        if self._shell is not None:  # Во время полёта снаряда танки замирают, прицеливаться нельзя.
            return
        tank = self._tanks[self._current_player]
        tank.aim(event.x, event.y)

    def _handle_click(self, event):
        if self._shell is not None:  # Во время полёта снаряда танки замирают, прицеливаться нельзя.
            return
        tank = self._tanks[self._current_player]
        tank.aim(event.x, event.y)

        if tank.can_shoot():
            self._shell = tank.shoot(event.x, event.y)
        else:
            print('This tank can\'t shoot')
            self._next_player()
