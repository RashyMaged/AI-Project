import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Connect Four")


ROWS, COLS = 6, 7
SQUARE_SIZE = 80
canvas_width = COLS * SQUARE_SIZE
canvas_height = (ROWS + 1) * SQUARE_SIZE
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

 
title_text = canvas.create_text(canvas_width//2, 50, text="CONNECT FOUR!!",
                                fill="white", font=("monospace", 30))
subtitle_text = canvas.create_text(canvas_width//2, 120, text="HAVE FUN!",
                                   fill="#17C4F3", font=("monospace", 25))


def show_message(message, color="white"):
    canvas.delete("message")
    canvas.create_text(canvas_width//2, 160, text=message, fill=color,
                       font=("monospace", 20), tags="message")


def start_game():
    show_message("Game Started!", "yellow")
    # canvas.delete("piece")  


def quit_game():
    root.destroy()

start_btn = tk.Button(root, text="Start", command=start_game, width=10, height=2)
start_btn.pack(side="left", padx=50, pady=20)

quit_btn = tk.Button(root, text="Quit", command=quit_game, width=10, height=2)
quit_btn.pack(side="right", padx=50, pady=20)

 
def draw_board():
    for c in range(COLS):
        for r in range(ROWS):
            x1 = c * SQUARE_SIZE
            y1 = (r+1) * SQUARE_SIZE
            x2 = x1 + SQUARE_SIZE
            y2 = y1 + SQUARE_SIZE
            canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
            canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="black", tags="piece")

draw_board()


def click_event(event):
    col = event.x // SQUARE_SIZE
    show_message(f"You clicked column {col+1}", "white")

canvas.bind("<Button-1>", click_event)

 
root.mainloop()