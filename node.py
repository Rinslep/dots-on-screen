"""
    Make nodes here! Square, rectangle, oval :) you decide
"""
import itertools


class Node(object):
    id_iter = itertools.count()

    def __init__(self):
        self.connections = {}
        self.id = next(Node.id_iter)


class NodeDisplay(Node):
    pass