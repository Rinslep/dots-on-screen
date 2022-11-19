"""
3 orange, 3 blue, and 1 white dots inside a rectangle
"""
import tkinter as tk
from random import randint

top = tk.Tk()

canvas = tk.Canvas(top, bg="black", height=680, width=1050)

dots = []
r = 10

for i in range(0,6):
    x = randint(11,1039)
    y = randint(11,669)
    center = (x-r, y-r, x+r, y+r)
    if i % 2 == 0:
        colour = 'blue'
    else:
        colour = 'orange'
    dots.append(canvas.create_oval(center, fill=colour))


canvas.pack()
top.mainloop()

