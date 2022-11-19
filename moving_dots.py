"""
takes the dots and moves them around the rectangle
"""

import tkinter as tk
from pprint import pprint
from random import randint


def move_dots(event, dots):
    for dot_id in dots:
        dx = randint(-10,10) #l to r
        dy = randint(-10,10) #u to d
        event.canvas.move(dot_id, dx, dy)


top = tk.Tk()

canvas = tk.Canvas(top, bg="black", height=680, width=1050)

dots_id = []
r = 10

for i in range(0,126):
    x = randint(11,1039)
    y = randint(11,669)
    center = (x-r, y-r, x+r, y+r)
    if i % 2 == 0:
        dots_id.append(canvas.create_oval(center, fill='blue'))
    else:
        dots_id.append(canvas.create_oval(center, fill='orange'))
canvas.pack()
pprint(dots_id)
top.mainloop()

