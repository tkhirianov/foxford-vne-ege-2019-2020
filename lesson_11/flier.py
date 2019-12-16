import tkinter as tk

WIDTH, HEIGHT = 500, 380


def initilization():
    global root, canvas
    root = tk.Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")


def main():
    initilization()
    root.mainloop()
    print("Game over!")


main()
