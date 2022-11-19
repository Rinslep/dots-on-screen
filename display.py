import math
from pprint import pprint
from tkinter import ttk
import tkinter as tk
from random import randint, choice, random
from nodes import *
from math import log2


# def init_notebook(window):
#     notebook = ttk.Notebook(window)
#     notebook.pack(pady=15)
#     return notebook
#
#
# def notebook_add_frame(notebook, label):
#     f = init_frame(notebook, label)
#     notebook.add(f, text=label)
#     return f
#
#
# def init_frame(window, frame_label):
#     frame = tk.LabelFrame(window, text=frame_label, relief=tk.RIDGE)
#     frame.grid(row=0, column=0)
#     return frame
#
#
# def init_canvas(frame):
#     c = tk.Canvas(frame, height=HEIGHT, width=WIDTH, bg='#AAAAAA')
#     c.pack(padx=10, pady=10, ipadx=10, ipady=10)
#     # c.pack(side=tk.LEFT)
#     return c
#
#
# def init_nodes_and_connections(nodes, lines, canvas):
#     def create_nodes(total_dict, canvas):
#         d = {}
#         t = sum(total_dict.values())
#
#         for k, v in total_dict.items():
#             c = randint(0, (WIDTH * HEIGHT))  # place randomly on the canvas
#             d[k] = Node(canvas, c, log2(v) * 2, k)  # creates class and places it on the canvas, visible
#         return d
#
#     def create_lines(total_dict, canvas):
#         tdk = iter(total_dict.keys())
#         for item in tdk:
#             for con_item in item.connected_items:
#                 try:
#                     Connection(canvas, total_dict[item], total_dict[con_item])
#                 except ConnectionCreationError as e:
#                     # print('Duplicate line - Not created')
#                     pass
#                 except KeyError as e:
#                     print('Not connected: ', e)
#
#     d = create_nodes(total_dict, canvas)
#     create_lines(d, canvas)
#
#     for node in Node.nodes:
#         node.raise_node()
#
#     return frame, canvas


def random_nodes(n=8):
    nodes = []
    r = 17
    pm = 10
    # create nodes
    for i in range(0, n - 1):
        c = randint(0, (WIDTH * HEIGHT))
        rad = randint(r - pm, r + pm)
        nodes.append([c, rad])
    return nodes


def random_lines(nodes, line_factor=0.7):
    lines = []
    for no in nodes:
        for de in nodes:
            if random() > line_factor and no is not de:  # dont connect to self
                lines.append([no, de, random()])
    return lines


def normalise_lines(nodes, lines):
    # for each line in lines change the values of lines[n][2]
    # based on the magnitudes of the lines that share a node
    # will get pretty damn close to 1 but not always equal 1
    print("preprocessing:")
    pprint(lines)
    prev = lines[0][0]
    values = []
    multis = {}
    for line in lines:
        if prev is line[0]:
            # print(f"value added from {line}")
            values.append(line[2])
        else:
            # gone to a new node
            if len(values) != 0:
                multi = 1 / sum(values)
                # pprint(f"values:{values} ")
                # print(f"multi: {multi}")
                i = nodes.index(prev)
                multis[i] = multi
                prev = line[0]
                values.clear()
                values.append(line[2])
            else:
                multi = 1

            # pprint(f"values:{values} ")
            # print(f"multi: {multi}")
            multi = 1 / sum(values)
            i = nodes.index(prev)
            multis[i] = multi

    for i, multi in multis.items():
        node = nodes[i]
        for line in lines:
            if line[0] is node:
                lines[i][2] = line[2] * multi

    # print("postprocessing:")
    # pprint(multis)
    # pprint(lines)
    return lines


# root = tk.Tk()
# root.title('factoRINo')
#
HEIGHT = 500
WIDTH = int(HEIGHT * (16 / 9))

nodes = random_nodes()
lines = random_lines(nodes,line_factor=.75)
new_lines = list(lines)
new_lines = normalise_lines(nodes, new_lines)

# i = 0
# while i < len(lines):
#     print("line:", lines[i])
#     print("nlin:", new_lines[i])
#     i += 1

# td = zip(nodes, lines)
#
# notebook = init_notebook(root)
# frame = notebook_add_frame(notebook, "First")
# canvas = init_canvas(frame)
# pprint(nodes)
# pprint(lines)
# first_page = init_nodes_and_connections(nodes, lines, canvas)

# for node in Node.nodes:
#     node.raise_node()
#
# while __name__ == '__main__':
#     root.mainloop()
