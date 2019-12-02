import tkinter as tk
from random import choice, randint


def canvas_click_handler(event):
    global scores
    # print(event.x, event.y)
    squared_distance = (x - event.x)**2 + (y - event.y)**2
    if squared_distance <= r*r:
        print("OUCH!!!")
        scores += 60 - r
        scores_label["text"] = str(scores)
        canvas.delete(ball_id)
        create_ball()


def restart_button_handler():
    global scores
    scores = 0
    scores_label["text"] = str(scores)
    canvas.delete(ball_id)
    create_ball()
    print("Типа перезапустили игру...")


def create_ball():
    global r, x, y, ball_id
    r = randint(10, 50)
    x = randint(r, 450-r)
    y = randint(r, 380-r)
    ball_color = choice(["blue", "green", "magenta", "orange"])
    ball_id = canvas.create_oval(x - r, y - r, x + r, y + r,
                                 fill=ball_color)


def initialization_of_the_game():
    global root, scores, scores_label, restart_button, canvas

    root = tk.Tk()
    root.geometry("450x380")
    root.pack_propagate(0)

    scores = 0
    scores_label = tk.Label(root, text=str(scores))
    scores_label.pack(anchor=tk.NE)
    restart_button = tk.Button(root, text="Перезапустить игру",
                               command=restart_button_handler)
    restart_button.place(relx=0, rely=0)
    canvas = tk.Canvas(root)
    canvas.pack(fill="both", expand=True)
    canvas.bind("<Button-1>", canvas_click_handler)

    create_ball()


initialization_of_the_game()
root.mainloop()
