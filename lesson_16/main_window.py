import tkinter as tk

from lesson_16.game_logic import GameRound
from lesson_16.constants import *


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
        self._root.geometry(str(WIDTH + 10) + 'x' + str(HEIGHT + 35))  # костыль!
        self._game = None

    def start_game(self):
        canvas = tk.Canvas(self._root, height=HEIGHT, width=WIDTH,
                           background="lightblue", border=3)
        canvas.pack()
        self._game = GameRound(canvas, 1, PLAYERS_NUMBER)

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
