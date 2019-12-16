from random import randint
import tkinter as tk

WIDTH, HEIGHT = 450, 380


# ========= Model ==========
def ball_init():
    global ball_id, ball_image
    global ball_x, ball_y, ball_radius
    ball_image = tk.PhotoImage(file="ball.png")
    ball_width = ball_image.width()
    ball_height = ball_image.height()
    assert ball_width == ball_height, "С такой картинкой не получится"
    ball_radius = ball_width // 2
    ball_x = randint(ball_radius, WIDTH - ball_radius - 1)
    ball_y = randint(ball_radius, HEIGHT - ball_radius - 1)    
    ball_id = canvas.create_image(ball_x,
                                ball_y,
                                image=ball_image)

def ball_move():
    global ball_x
    canvas.coords(ball_id, ball_x, ball_y)
    ball_x += 1


# ======== Control and View ========
def canvas_click_handler(event):
    global scores
    # print(event.x, event.y)
    squared_distance = (ball_x - event.x)**2 + (ball_y - event.y)**2
    if squared_distance <= ball_radius**2:
        scores += 10
        scores_label["text"] = str(scores)
        canvas.delete(ball_id)
        ball_init()


def restart_button_handler():
    global scores
    scores = 0
    scores_label["text"] = str(scores)
    canvas.delete(ball_id)
    ball_init()
    print("Типа перезапустили игру...")


def next_frame_job(n):
    ball_move()
    canvas.after(20, next_frame_job, n+1)


def initilization():
    global root, canvas, scores, scores_label
    root = tk.Tk()
    # создаём холст:
    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH,
                       background="lightblue", border=3)
    canvas.pack()

    scores = 0
    scores_label = tk.Label(root, text=str(scores))
    scores_label.pack()

    restart_button = tk.Button(root, text="Перезапустить игру",
                               command=restart_button_handler)
    restart_button.pack()

    ball_init()

    # привязка событий:
    canvas.bind("<Button-1>", canvas_click_handler)
    canvas.after(2000, next_frame_job, 1)

def main():
    initilization()
    root.mainloop()
    print("Game over!")


main()
