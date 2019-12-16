import tkinter as tk

WIDTH, HEIGHT = 450, 380


def next_frame_job(x):
    print("frame", x)
    canvas.after(200, next_frame_job, x+1)


def initilization():
    global root, canvas
    root = tk.Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH,
                       background="lightblue")
    canvas.pack()
    flier = canvas.create_rectangle(50, 25, 150, 75,
                                    fill="blue")
    canvas.after(1000, next_frame_job, 1)


def main():
    initilization()
    root.mainloop()
    print("Game over!")


main()
