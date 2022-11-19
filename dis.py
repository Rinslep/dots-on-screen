from tkinter import *
from random import randint, choice
from math import fmod, dist, log10, sin, radians, degrees


class Node(object):
    nodes = []

    def __init__(self, window, center, radius, colour='red'):
        self.window = window
        self.center = center  # single int, converted by the class to x, y
        self.radius = radius
        Node.nodes.append(self)
        self.node_id = None
        self.create_square_node(self, fill=colour)
        # self.create_oval_node(self, fill=colour)
        self.raise_node()
        self.lastx, self.lasty = self.tl
        self.connections = {}

    @staticmethod
    def create_oval_node(parent, fill='red'):
        parent.node_id = parent.window.create_oval(parent.tl, parent.br, fill=fill)
        parent.window.tag_bind(parent.node_id, '<Button-1>', lambda e: parent.drag(e))
        parent.window.tag_bind(parent.node_id, '<B1-Motion>', lambda e: parent.drag(e), add='+')
        # self.window.tag_bind(self.node_id, '<Button-3>', lambda e: self.move(e), add='+')
        parent.window.tag_bind(parent.node_id, '<Button-2>', lambda e: parent.log(e), add='+')
        parent.window.tag_bind(parent.node_id, '<Button-3>', lambda e: parent.display_info(e), add='+')

    @staticmethod
    def create_square_node(parent, fill='red'):
        parent.node_id = parent.window.create_polygon(parent.bbox, fill=fill)
        parent.window.tag_bind(parent.node_id, '<Button-1>', lambda e: parent.drag(e))
        parent.window.tag_bind(parent.node_id, '<B1-Motion>', lambda e: parent.drag(e), add='+')
        # self.window.tag_bind(self.node_id, '<Button-3>', lambda e: self.move(e), add='+')
        parent.window.tag_bind(parent.node_id, '<Button-2>', lambda e: parent.log(e), add='+')
        parent.window.tag_bind(parent.node_id, '<Button-3>', lambda e: parent.display_info(e), add='+')

    def move_center(self, x, y):
        self.center = self.coords_to_int(x, y, self.canvas_width)
        self.window.coords(self.node_id, *self.tl, *self.br)
        self.move_connected_lines()

    @property
    def canvas_width(self):
        return int(self.window.cget('width'))

    @property
    def center_coords(self):
        x = fmod(self.center, self.canvas_width)
        y = (self.center + 1) // self.canvas_width
        return int(x), int(y)

    @property
    def tl(self):
        tl = list(self.center_coords)
        tl[0] = int(tl[0] - self.radius)
        tl[1] = int(tl[1] - self.radius)
        return tl

    @property
    def bl(self):
        bl = list(self.center_coords)
        bl[0] = int(bl[0] - self.radius)
        bl[1] = int(bl[1] + self.radius)
        return bl

    @property
    def br(self):
        br = list(self.center_coords)
        br[0] = int(br[0] + self.radius)
        br[1] = int(br[1] + self.radius)
        return br

    @property
    def tr(self):
        tr = list(self.center_coords)
        tr[0] = int(tr[0] + self.radius)
        tr[1] = int(tr[1] - self.radius)
        return tr

    @property
    def bbox(self):
        return self.tl, self.bl, self.br, self.tr

    def add_connection(self, node, line):
        self.connections[node] = line

    def move(self, e):
        if any(self.connections):
            for node, line in self.connections.items():
                # print(f'n: {node.py}, L: {line}')
                d = line.length
                m = (self.radius * node.radius) / (d ** 2)
                a = log10(m * d)
                x1, y1, x2, y2 = line.dist_along(a)
                self.move_center(x1, y1)
                node.move_center(x2, y2)

    def drag(self, e):
        self.lastx, self.lasty = self.tl
        self.center = (e.y * self.canvas_width) + e.x
        self.window.move(self.node_id, self.tl[0] - self.lastx, self.tl[1] - self.lasty)
        self.lastx, self.lasty = self.tl
        self.move_connected_lines()
        self.raise_node()


    def raise_node(self):
        self.window.tag_raise(self.node_id)

    def move_connected_lines(self):
        for line in self.connections.values():
            line.move()

    @classmethod
    def coords_to_int(cls, x, y, width):
        return int((y * width) + x)

    @classmethod
    def is_connected(cls, a, b):
        if b in a.connections.keys():
            raise LineExistsError


class Line(object):
    lines = []

    def __init__(self, window, a, b):
        self.window = window
        self.a = a
        self.b = b
        self.id = None
        self.create_line()
        Line.lines.append(self)
        a.add_connection(b, self)
        b.add_connection(a, self)

    @property
    def a_center(self):
        return self.a.center_coords

    @property
    def b_center(self):
        return self.b.center_coords

    @property
    def length(self):
        # could also minus both radius
        return dist(self.a_center, self.b_center)

    @property
    def line_slope(self):
        x1, y1 = self.a_center
        x2, y2 = self.b_center
        rise = y2 - y1
        run = x2 - x1
        return rise/run

    @property
    def canvas_width(self):
        return int(self.window.cget('width'))

    def get_direction(self):
        # a->b is opposite direction of b->a
        # down right is [True, True], up left is [False, False]
        return self.a_center[0] > self.b_center[0], self.a_center[1] > self.b_center[1]

    # def dist_along(self, multiplier):
    #     d = (self.length * multiplier) / 2
    #     c = self.a_center[1] - (self.line_slope * self.a_center[0])


    def move(self):
        self.window.coords(self.id, *self.a_center, *self.b_center)

    def create_line(self):
        self.id = self.window.create_line(self.a_center, self.b_center, fill='black', width=randint(2,10))


class LineExistsError(Exception):
    pass


root = Tk()
root.title('factoRINo')


HEIGHT = 500
WIDTH = int(HEIGHT * (16 / 9))

canvas = Canvas(root, height=HEIGHT, width=WIDTH, bg='#AAAAAA')
canvas.pack(padx=50, pady=50, ipadx=10, ipady=10, side=LEFT)

# create nodes
for i in range(5):
    c = randint(0, (WIDTH * HEIGHT))
    r = randint(10, 24)
    Node(canvas, c, r)

# create lines
for i in range(8):
    while True:
        try:
            node_a = choice(list(Node.nodes))
            node_b = choice(list(Node.nodes))
            while node_a is node_b:
                node_b = choice(list(Node.nodes))
            Node.is_connected(node_a, node_b)
            break
        except LineExistsError:
            pass
    # print(f'a:{node_a}, b:{node_b}')
    Line(canvas, node_a, node_b)

for node in Node.nodes:
    node.raise_node()

# for line in Line.lines:
#     print(f'a:{line.a_center},{line.a.center}:{Node.coords_to_int(*line.a_center, line.canvas_width)}, b:{line.b_center} = {line.length}')

while __name__ == '__main__':
    root.mainloop()