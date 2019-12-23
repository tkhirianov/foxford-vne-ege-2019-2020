from random import randint
import tkinter as tk

WIDTH, HEIGHT = 450, 380
DT = 1


# ========= Model ==========
class Ball:
    def init(self):
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


# ======== Control and View ========
def canvas_click_handler(event):
    global scores
    # print(event.x, event.y)
    squared_distance = (ball.x - event.x)**2 + (ball.y - event.y)**2
    if squared_distance <= ball.radius**2:
        scores += 10
        scores_label["text"] = str(scores)
        canvas.delete(ball.id)
        ball.init()


def restart_button_handler():
    global scores
    scores = 0
    scores_label["text"] = str(scores)
    canvas.delete(ball.id)
    ball.init()
    print("Типа перезапустили игру...")


def next_frame_job(n):
    ball.move()
    canvas.after(20, next_frame_job, n+1)


def initilization():
    global root, canvas, scores, scores_label, ball
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

    ball = Ball()
    ball.init()

    # привязка событий:
    canvas.bind("<Button-1>", canvas_click_handler)
    canvas.after(2000, next_frame_job, 1)

def main():
    initilization()
    root.mainloop()
    print("Game over!")


main()
