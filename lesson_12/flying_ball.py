from random import randint
import tkinter as tk

WIDTH, HEIGHT = 450, 380
DT = 1


# ========= Model ==========
class Ball:
    def __init__(self):
        self.image = tk.PhotoImage(file="ball.png")
        self.width = self.image.width()
        self.height = self.image.height()
        assert self.width == self.height, "С такой картинкой не получится"
        self.radius = self.width // 2

        self.x = randint(self.radius, WIDTH - self.radius - 1)
        self.y = randint(self.radius, HEIGHT - self.radius - 1)
        self.vx = randint(-5, +5)
        self.vy = randint(-5, +5)
        self.id = canvas.create_image(self.x, self.y, image=self.image)

    def move(self):
        canvas.coords(self.id, self.x, self.y)
        self.x += self.vx * DT
        self.y += self.vy * DT
        if self.x <= self.radius:
            self.x = self.radius
            self.vx = -self.vx
        if self.y <= self.radius:
            self.y = self.radius
            self.vy = -self.vy
        if self.x >= WIDTH - self.radius - 1:
            self.x = WIDTH - self.radius - 1
            self.vx = -self.vx
        if self.y >= HEIGHT - self.radius - 1:
            self.y = HEIGHT - self.radius - 1
            self.vy = -self.vy

    def is_inside(self, x, y):
        squared_distance = (self.x - x)**2 + (self.y - y)**2
        return squared_distance <= self.radius**2


# ======== Control and View ========
def canvas_click_handler(event):
    global scores, balls
    ball_to_delete = None
    for ball in balls:
        if ball.is_inside(event.x, event.y):
            ball_to_delete = ball
    if ball_to_delete is not None:
        scores += 10
        scores_label["text"] = str(scores)
        canvas.delete(ball_to_delete.id)
        balls.remove(ball_to_delete)


def restart_button_handler():
    global scores, balls
    scores = 0
    scores_label["text"] = str(scores)

    for ball in balls:
        canvas.delete(ball.id)
    balls[:] = [Ball() for i in range(5)]
    print("Типа перезапустили игру...")


def next_frame_job(n):
    for ball in balls:
        ball.move()
    canvas.after(20, next_frame_job, n+1)


def initilization():
    global root, canvas, scores, scores_label, balls
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

    balls = [Ball() for i in range(5)]

    # привязка событий:
    canvas.bind("<Button-1>", canvas_click_handler)
    canvas.after(2000, next_frame_job, 1)

def main():
    initilization()
    root.mainloop()
    print("Game over!")


main()
