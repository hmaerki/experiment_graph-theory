import dataclasses
from typing import Dict, FrozenSet, List, Set

import matplotlib
import matplotlib.pyplot
from matplotlib import pyplot as plt
from matplotlib.markers import MarkerStyle
from matplotlib.text import TextPath
from matplotlib.transforms import Affine2D

# from graph import Graph

STR_GAME_6A = "6:0-1,0-3,0-4,1-2,1-3,1-5,2-3,2-5,3-4"
STR_GAME_10A = "10:0-1,0-2,0-3,0-5,1-2,1-9,3-5,3-6,3-7,4-7,4-8,4-9,5-6,6-8,7-8,7-9"
STR_GAME_20A = "20:0-3,0-10,0-12,1-5,1-11,1-15,1-16,2-3,2-7,2-19,3-5,3-11,4-15,4-17,4-18,5-11,5-15,6-8,6-19,7-8,7-16,7-19,8-16,8-19,9-10,9-12,9-13,9-14,10-12,10-14,11-16,12-18,13-17,13-18,15-18"
STR_GAME_20B = "20:0-4,0-5,0-14,0-19,1-10,1-11,1-15,1-16,2-3,2-9,2-11,2-18,3-9,3-17,4-8,4-12,4-19,5-6,5-14,6-7,6-14,7-14,7-17,8-12,8-13,8-15,9-17,9-18,10-12,10-15,11-16,13-15,13-16,13-19,16-18,17-18"
STR_GAME_100A = "100:0-21,0-61,0-70,0-98,1-17,1-22,1-43,1-58,2-33,2-96,2-99,3-16,3-74,3-82,3-94,4-20,4-25,4-45,4-60,5-24,5-37,5-41,5-63,6-29,6-35,6-69,6-92,7-31,7-47,7-50,8-49,8-59,8-87,9-47,9-49,9-59,10-32,10-41,10-64,10-83,11-38,11-42,11-51,11-79,12-16,12-67,12-71,12-72,13-28,13-62,13-79,13-84,14-53,14-74,14-82,15-29,15-35,15-40,15-98,16-67,16-94,17-22,17-81,17-89,18-26,18-55,18-86,18-93,19-40,19-70,19-88,19-98,20-56,20-60,20-62,21-61,21-70,22-39,22-91,23-46,23-54,23-55,23-95,24-27,24-37,24-71,25-42,25-45,25-84,26-33,26-43,26-93,27-65,27-82,28-62,30-54,30-64,30-73,30-97,31-44,31-50,31-67,32-46,32-54,32-58,33-96,33-99,34-81,34-89,34-96,35-36,35-40,36-44,36-72,36-92,37-63,37-71,38-56,38-66,38-80,39-65,39-90,39-91,40-88,41-58,41-83,42-45,42-60,43-58,43-89,44-69,44-92,45-60,46-54,46-95,47-50,48-52,48-56,48-77,48-87,49-50,49-87,51-66,51-78,51-79,52-56,52-77,52-85,53-57,53-74,53-94,55-86,55-95,57-68,57-77,57-85,61-98,62-84,63-71,63-83,64-73,64-88,65-80,65-90,66-75,66-76,67-72,68-80,68-82,68-85,69-92,70-97,72-88,73-97,74-94,75-76,75-91,76-78,76-81,77-85,79-84,80-90,81-89,86-93,86-99,90-91,93-99"


@dataclasses.dataclass(unsafe_hash=True, order=True, repr=True)
class Node:
    name: str = dataclasses.field(hash=True, compare=True)
    edges: List["Node"] = dataclasses.field(
        hash=False, compare=False, default_factory=list
    )
    x: float = dataclasses.field(hash=False, compare=False, default=-10.0)
    y: float = dataclasses.field(hash=False, compare=False, default=-10.0)


@dataclasses.dataclass(order=True, repr=True)
class Game:
    nodes: Dict[str, Node] = dataclasses.field(default_factory=dict)

    def add_edge(self, a: str, b: str) -> None:
        # edge = Edge(a=self.get_node(a), b=self.get_node(b))
        # a.edges.append(edge)
        # b.edges.append(edge)
        node_a = self.get_node(a)
        node_b = self.get_node(b)
        node_a.edges.append(node_b)
        node_b.edges.append(node_a)

    def get_node(self, name: str) -> Node:
        try:
            return self.nodes[name]
        except KeyError:
            node = Node(name=name)
            self.nodes[name] = node
            return node


def plot_2d(graph, nodes=True, edges=True):
    plt.figure()
    if nodes:
        for a in graph.nodes.values():
            s = TextPath((-3.0, -5.0), a.name)
            m = MarkerStyle(s)
            plt.plot(a.x, a.y, marker=m, markersize=20)

    if edges:
        for node in graph.nodes.values():
            for node_edge in node.edges:
                attrs = "b-"
                plt.plot(
                    [node.x, node_edge.x], [node.y, node_edge.y], attrs, clip_on=False
                )

    plt.axis("scaled")
    plt.axis("off")
    # plt.axis("on")
    # plt.margins(0.1)
    return plt


def set_xy(g: Game, name: str, x: float, y: float):
    for n in g.nodes.values():
        if n.name == name:
            n.x = x
            n.y = y
            return
    raise ValueError()


def create_graph(str_game: str) -> Game:
    _count_edges, text_edges = str_game.split(":")
    list_edges = [e.split("-", 2) for e in text_edges.split(",")]
    g = Game()
    for a, b in list_edges:
        g.add_edge(a=a, b=b)
    return g


class PathCollector:
    def __init__(self):
        self.path_set: Set[FrozenSet[Node]] = set()

    def iter_path(self, g: Game) -> None:
        """
        Start with the lowest node.
        """
        current_path: Set[Node] = set()

        def is_superpath(current_path: FrozenSet[Node]) -> bool:
            """
            return if 'current_path' is embracing a smaller path.
            """
            if len(current_path) < 4:
                # This path is to short to be able to embrace another path
                return False
            for path in self.path_set:
                if path.issubset(current_path):
                    # dropped
                    # print(
                    #     f"DROPPED: {text_path(path)} contains {text_path(current_path)}"
                    # )
                    return True
            return False

        def recurse(path_len: int, start_node: Node, node: Node):
            current_path.add(node)
            # for next_node in sorted(g.nodes(from_node=node)):
            for edge_node in sorted(node.edges):
                # print(edge)
                if edge_node.name == "2":
                    pass
                if edge_node is start_node:
                    if len(current_path) > 2:
                        if is_superpath(current_path=current_path):
                            continue
                        self.path_set.add(frozenset(current_path))
                    continue
                if edge_node in current_path:
                    continue
                if len(current_path) >= path_len:
                    continue
                recurse(path_len=path_len, start_node=start_node, node=edge_node)
            current_path.remove(node)

        node_count = len(g.nodes)
        # for path_len in range(3, node_count+ 1):
        for path_len in range(3, 5):
            for start_node in sorted(g.nodes.values()):
                # print(start_node)
                recurse(path_len=path_len, start_node=start_node, node=start_node)

    def smallest_paths(self) -> Set[FrozenSet[Node]]:
        pass

    @staticmethod
    def print_paths(path_set: Set[FrozenSet[Node]]) -> None:
        print("------")
        l: List[str] = []
        for path in path_set:
            l.append(text_path(path))
        for p in sorted(l):
            print(p)


def text_path(path: Set[Node]) -> str:
    return ",".join([n.name for n in sorted(path)])


def collect_path(g: Game):
    pc = PathCollector()
    pc.iter_path(g=g)
    PathCollector.print_paths(pc.path_set)
    # for path in iter_path(g=g):
    # print(sorted(path))


def doit(str_game: str = STR_GAME_10A):
    g = create_graph(str_game)
    # print(g)
    # plot = plot_2d(graph=g)
    # plot.show()
    collect_path(g=g)


if __name__ == "__main__":
    doit(STR_GAME_6A)
    # doit(STR_GAME_10A)
    # doit(STR_GAME_20A)
    # doit(STR_GAME_100A)
