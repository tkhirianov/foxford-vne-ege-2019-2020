from random import randint
import tkinter as tk

WIDTH, HEIGHT = 450, 380
DT = 0.2
GRAVITY_CONSTANT = 3
START_PAUSE = 1000
FRAME_TIME = 20  #microseconds

# ========= Model ==========

class Tank:
    """ Танк, который будет порождать снаряды
        и тем самым сбивать пузыри.
    """
    pass


class Shell:
    """ Снаряд, который летит под действием гравитации,
        вылетая за границу экрана просто исчезает.
    """
    pass


class Bubble:
    """ Пузырик, который разрушается снарядом,
        летает без действия гравитации,
        отражается от стенок
        и в идеале упруго отталкивается от других.
    """
    pass


class GameRound:
    """ Игровой раунд.
        Здесь в атрибутах содержатся ссылки на:
        1. холст
        2. танк
        3. список текущих, "живых" снарядов
        4. список пузыриков
    """    
    def __init__(self, canvas):
        pass

    def handle_frame(self):
        print('handled frame')

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
        self._game = None
        self._restart_button = tk.Button(self._root, text="Перезапустить игру",
                                         command=self._restart_button_handler)
        self._restart_button.pack()

    def start_game(self):
        canvas = tk.Canvas(self._root, height=HEIGHT, width=WIDTH,
                           background="lightblue", border=3)
        canvas.pack()
        self._game = GameRound(canvas)
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
