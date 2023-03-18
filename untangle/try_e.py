import math
import time
import cProfile

import matplotlib
import matplotlib.pyplot

STR_GAME_10A = "10:0-1,0-2,0-3,0-5,1-2,1-9,3-5,3-6,3-7,4-7,4-8,4-9,5-6,6-8,7-8,7-9"
STR_GAME_20A = "20:0-3,0-10,0-12,1-5,1-11,1-15,1-16,2-3,2-7,2-19,3-5,3-11,4-15,4-17,4-18,5-11,5-15,6-8,6-19,7-8,7-16,7-19,8-16,8-19,9-10,9-12,9-13,9-14,10-12,10-14,11-16,12-18,13-17,13-18,15-18"
STR_GAME_20B = "20:0-4,0-5,0-14,0-19,1-10,1-11,1-15,1-16,2-3,2-9,2-11,2-18,3-9,3-17,4-8,4-12,4-19,5-6,5-14,6-7,6-14,7-14,7-17,8-12,8-13,8-15,9-17,9-18,10-12,10-15,11-16,13-15,13-16,13-19,16-18,17-18"
STR_GAME_100A = "100:0-21,0-61,0-70,0-98,1-17,1-22,1-43,1-58,2-33,2-96,2-99,3-16,3-74,3-82,3-94,4-20,4-25,4-45,4-60,5-24,5-37,5-41,5-63,6-29,6-35,6-69,6-92,7-31,7-47,7-50,8-49,8-59,8-87,9-47,9-49,9-59,10-32,10-41,10-64,10-83,11-38,11-42,11-51,11-79,12-16,12-67,12-71,12-72,13-28,13-62,13-79,13-84,14-53,14-74,14-82,15-29,15-35,15-40,15-98,16-67,16-94,17-22,17-81,17-89,18-26,18-55,18-86,18-93,19-40,19-70,19-88,19-98,20-56,20-60,20-62,21-61,21-70,22-39,22-91,23-46,23-54,23-55,23-95,24-27,24-37,24-71,25-42,25-45,25-84,26-33,26-43,26-93,27-65,27-82,28-62,30-54,30-64,30-73,30-97,31-44,31-50,31-67,32-46,32-54,32-58,33-96,33-99,34-81,34-89,34-96,35-36,35-40,36-44,36-72,36-92,37-63,37-71,38-56,38-66,38-80,39-65,39-90,39-91,40-88,41-58,41-83,42-45,42-60,43-58,43-89,44-69,44-92,45-60,46-54,46-95,47-50,48-52,48-56,48-77,48-87,49-50,49-87,51-66,51-78,51-79,52-56,52-77,52-85,53-57,53-74,53-94,55-86,55-95,57-68,57-77,57-85,61-98,62-84,63-71,63-83,64-73,64-88,65-80,65-90,66-75,66-76,67-72,68-80,68-82,68-85,69-92,70-97,72-88,73-97,74-94,75-76,75-91,76-78,76-81,77-85,79-84,80-90,81-89,86-93,86-99,90-91,93-99"


class Node:
    def __init__(self, i, x, y):
        self.i = i
        self.c = complex(real=x, imag=y)
        self.edges = []

    def __repr__(self):
        return f"Node({self.i})"

    @property
    def x(self):
        return self.c.real

    @property
    def y(self):
        return self.c.imag


class Edge:
    def __init__(self, a, b):
        assert isinstance(a, Node)
        assert isinstance(b, Node)
        a.edges.append(self)
        b.edges.append(self)
        self.a = a
        self.b = b

    def other_node(self, node):
        assert isinstance(node, Node)
        if node == self.a:
            return self.b
        if node == self.b:
            return self.a
        raise f"Node {node} is not part of {self}"

    def __repr__(self):
        return f"Edge({self.a.i}-{self.b.i})"


class Graph:
    def __init__(self):
        self.nodes = []


class Path:
    def __init__(self, path):
        assert isinstance(path, list)
        self.path = path
        self.indexes = [str(node.i) for node in path]
        self.unique = "-".join(sorted(self.indexes))
        self.set_indexes = set(self.path)

    def issuper(self, path):
        assert isinstance(path, Path)
        return self.set_indexes.issuperset(path.set_indexes)

    def __repr__(self):
        return "-".join(self.indexes)


def doit(str_game):
    g = Graph()
    size, edges_ = str_game.split(":")
    size = int(size)
    delta_angle = 2 * math.pi / size
    g.nodes = [
        Node(i, x=math.sin(i * delta_angle), y=math.cos(i * delta_angle))
        for i in range(size)
    ]
    g.edges = []
    for edge_ in edges_.split(","):
        a, b = map(int, edge_.split("-", 2))
        g.edges.append(Edge(a=g.nodes[a], b=g.nodes[b]))

    start_s = time.time()
    pr = cProfile.Profile()
    pr.enable()
    c = Circles()
    c.all(nodes=g.nodes)
    print(f"duration: {time.time()-start_s:0.1f}s")
    print(f"c.count: {len(c.paths)}")
    pr.disable()

    # pr.print_stats(sort=2) # Cumulative
    pr.print_stats(sort=1)  # time

    count_issub = 0
    for path in c.paths:
        if c.issuper(path):
            continue
        count_issub += 1
    print(f"count_issub: {count_issub}")
    for path in c.paths:
        issuper = c.issuper(path)
        if not issuper:
            print(f"path: {path}")
            # print(f'path: {path} {c.issuper(path)}')

    plt = plot_2d(g)
    plt.show()


class Circles:
    def __init__(self):
        self.paths = []
        self.path_uniques = set()

    def issuper(self, path):
        assert isinstance(path, Path)
        for path_ in self.paths:
            if path_.unique == path.unique:
                continue
            if path.issuper(path_):
                return True
        return False

    def append(self, p):
        assert isinstance(p, Path)
        self.path_uniques.add(p.unique)
        self.paths.append(p)

    def recurse(self, path):
        # print(f'recurse: {path}')
        first_node = path[0]
        last_node = path[-1]
        for edge in last_node.edges:
            new_node = edge.other_node(last_node)
            if len(path) > 2:
                if new_node == first_node:
                    p = Path(path)
                    if p.unique in self.path_uniques:
                        continue
                    self.append(p)
                    continue
            if new_node in path:
                # This is a circle
                continue
            self.recurse(
                path
                + [
                    new_node,
                ]
            )

    def all(self, nodes):
        for node in nodes:
            self.recurse(
                path=[
                    node,
                ]
            )


def plot_2d(g):
    matplotlib.pyplot.figure()

    for edge in g.edges:
        matplotlib.pyplot.plot(
            [edge.a.x, edge.b.x], [edge.a.y, edge.b.y], "bo-", clip_on=False
        )

    for node in g.nodes:
        matplotlib.pyplot.annotate(
            node.i,
            (node.x, node.y),
            textcoords="offset points",  # how to position the text
            xytext=(0, 10),  # distance from text to points (x,y)
            ha="center",  # horizontal alignment can be left, right or center
        )

    matplotlib.pyplot.axis("scaled")
    matplotlib.pyplot.axis("off")
    return matplotlib.pyplot


doit(STR_GAME_20A)
