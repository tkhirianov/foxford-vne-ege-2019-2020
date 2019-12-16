import tkinter as tk

WIDTH, HEIGHT = 450, 380


# ========= Model ==========
def flier_init():
    global flier, flier_image
    global flier_x, flier_y, flier_width, flier_height
    flier_image = tk.PhotoImage(file="ball.png")
    flier_x, flier_y = 50, 75
    flier_width = flier_image.width()
    flier_height = flier_image.height()
    flier = canvas.create_image(flier_x,
                                flier_y,
                                image=flier_image)

def flier_move():
    global flier_x
    canvas.coords(flier, flier_x, flier_y)
    flier_x += 1


# ======== Control and View ========
def next_frame_job(n):
    print("frame", n)
    flier_move()
    canvas.after(20, next_frame_job, n+1)


def initilization():
    global root, canvas
    root = tk.Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH,
                       background="lightblue")
    canvas.pack()
    flier_init()
    canvas.after(2000, next_frame_job, 1)

def main():
    initilization()
    root.mainloop()
    print("Game over!")


main()
