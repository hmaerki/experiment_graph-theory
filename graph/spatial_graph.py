from graph import BasicGraph
from graph.search import (
    shortest_path,
    breadth_first_search,
    depth_first_search,
    distance,
    degree_of_separation
)
from graph.topology import (
    subgraph,
    has_cycles,
    components,
    network_size,
    has_path,
)
from graph.flow_problem import maximum_flow


class Graph3D(BasicGraph):
    """ a graph where all (x,y)-positions are unique. """
    def __init__(self, from_dict=None, from_list=None):
        super().__init__(from_dict=from_dict, from_list=from_list)

    def __copy__(self):
        g = Graph3D(from_dict=self.to_dict())
        return g

    # spatial only function
    # ---------------------
    @staticmethod
    def _check_tuples(n1):
        if not isinstance(n1, tuple):
            raise TypeError(f"expected tuple, not {type(n1)}")
        if len(n1) != 3:
            raise ValueError(f"expected tuple in the form as (x,y,z), got {n1}")
        if not all(isinstance(i, (float, int)) for i in n1):
            raise TypeError(f"expected all values to be integer or float, but got {n1}")

    @staticmethod
    def distance(n1, n2):
        """ returns the distance between to xyz tuples coordinates
        :param n1: (x,y,z)
        :param n2: (x,y,z)
        :return: float
        """
        Graph3D._check_tuples(n1)
        Graph3D._check_tuples(n2)
        (x1, y1, z1), (x2, y2, z2) = n1, n2
        a = abs(x2-x1)
        b = abs(y2-y1)
        c = abs(z2-z1)
        return (a * a + b * b + c * c) ** (1 / 2)

    def add_edge(self, n1, n2, value=None, bidirectional=False):
        self._check_tuples(n1)
        self._check_tuples(n2)
        assert value is not None
        super().add_edge(n1, n2, value, bidirectional)

    def add_node(self, node_id, obj=None):
        self._check_tuples(node_id)
        super().add_node(node_id, obj)
        """
        :param node_id: any hashable node.
        :param obj: any object that the node should refer to.

        PRO TIP: To retrieve the node obj use g.node(node_id)
        """
        self._nodes[node_id] = obj

    def n_nearest_neighbours(self, node_id, n=1):
        """ returns the node id of the `n` nearest neighbours. """
        self._check_tuples(node_id)
        if not isinstance(n, int):
            raise TypeError(f"expected n to be integer, not {type(n)}")
        if n < 1:
            raise ValueError(f"expected n >= 1, not {n}")

        d = [(self.distance(n1=node_id, n2=n), n) for n in self.nodes() if n != node_id]
        d.sort()
        if d:
            return [b for a, b in d][:n]
        return None

    def plot(self, nodes=True, edges=True, rotation='xyz', maintain_aspect_ratio=False):
        """ plots nodes and links using matplotlib3
        :param nodes: bool: plots nodes
        :param edges: bool: plots edges
        :param rotation: str: set view point as one of [xyz,xzy,yxz,yzx,zxy,zyx]
        :param maintain_aspect_ratio: bool: rescales the chart to maintain aspect ratio.
        :return: None. Plots figure.
        """
        from mpl_toolkits.mplot3d import Axes3D  # import required by matplotlib.
        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        if not len(rotation) == 3:
            raise ValueError(f"expected viewpoint as 'xyz' but got: {rotation}")
        for c in 'xyz':
            if c not in rotation:
                raise ValueError(f"rotation was missing {c}.")
        x, y, z = rotation

        # Data for a three-dimensional line
        if edges:
            for edge in self.edges():
                n1, n2, v = edge
                xyz = dict()
                xyz[x] = [n1[0], n2[0]]
                xyz[y] = [n1[1], n2[1]]
                xyz[z] = [n1[2], n2[2]]
                ax.plot3D(xyz['x'], xyz['y'], xyz['z'], 'gray')

        # Data for three-dimensional scattered points
        if nodes:
            xyz = {x: [], y: [], z: []}
            ix = []
            for idx, node in enumerate(self.nodes()):
                vx, vy, vz = node  # value of ...
                xyz[x].append(vx)
                xyz[y].append(vy)
                xyz[z].append(vz)
                ix.append(idx)
            ax.scatter3D(xyz['x'], xyz['y'], xyz['z'], c=ix, cmap='Greens')

        if (nodes or edges) and maintain_aspect_ratio:
            nodes = [n for n in self.nodes()]
            xyz_dir = {'x': 0, 'y': 1, 'z': 2}

            xdim = xyz_dir[x]  # select the x dimension in the projection.
            # as the rotation will change the xdimension index.
            xs = [n[xdim] for n in nodes]  #  use the xdim index to obtain the values.
            xmin, xmax = min(xs), max(xs)
            dx = (xmax + xmin) / 2  # determine the midpoint for the dimension.

            ydim = xyz_dir[y]
            ys = [n[ydim] for n in nodes]
            ymin, ymax = min(ys), max(ys)
            dy = (ymax + ymin) / 2

            zdim = xyz_dir[z]
            zs = [n[zdim] for n in nodes]
            zmin, zmax = min(zs), max(zs)
            dz = (zmax + zmin) / 2

            # calculate the radius for the aspect ratio.
            max_dim = max([xmax - xmin, ymax - ymin, zmax - zmin]) / 2

            xa, xb = dx - max_dim, dx + max_dim  # lower, uppper
            ax.set_xlim(xa, xb)  # apply the lower and upper to the axis.
            ya, yb = dy - max_dim, dy + max_dim
            ax.set_ylim(ya, yb)
            za, zb = dz - max_dim, dz + max_dim
            ax.set_zlim(za, zb)

        ax.set_xlabel(f'{x} Label')
        ax.set_ylabel(f'{y} Label')
        ax.set_zlabel(f'{z} Label')
        plt.show()

    # general graph functions
    # -----------------------
    def shortest_path(self, start, end):
        """
        :param start: start node
        :param end: end node
        :return: distance, path as list
        """
        return shortest_path(self, start, end)

    def breadth_first_search(self, start, end):
        """ Determines the path with fewest nodes.
        :param start: start node
        :param end: end nodes
        :return: nodes, path as list
        """
        return breadth_first_search(graph=self, start=start, end=end)

    def depth_first_search(self, start, end):
        """
        Finds a path from start to end using DFS.
        :param start: start node
        :param end: end node
        :return: path
        """
        return depth_first_search(graph=self, start=start, end=end)

    def distance_from_path(self, path):
        """
        :param path: list of nodes
        :return: distance along the path.
        """
        return distance(graph=self, path=path)

    def maximum_flow(self, start, end):
        """ Determines the maximum flow of the graph between
        start and end.
        :param start: node (source)
        :param end: node (sink)
        :return: flow, graph of flow.
        """
        return maximum_flow(self, start, end)

    def subgraph_from_nodes(self, nodes):
        """
        constructs a copy of the graph containing only the
        listed nodes (and their links)
        :param nodes: list of nodes
        :return: class Graph
        """
        return subgraph(graph=self, nodes=nodes)

    def has_cycles(self):
        """ Checks if the graph has a cycle
        :return: bool
        """
        return has_cycles(graph=self)

    def components(self):
        """ Determines the number of components
        :return: list of sets of nodes. Each set is a component.
        """
        return components(graph=self)

    def network_size(self, n1, degrees_of_separation=None):
        """ Determines the nodes within the range given by
        a degree of separation
        :param graph: Graph
        :param n1: start node
        :param degrees_of_separation: integer
        :return: set of nodes within given range
        """
        return network_size(self, n1, degrees_of_separation)

    def has_path(self, path):
        """
        :param path: list of nodes
        :return: boolean, if the path is in G.
        """
        return has_path(graph=self, path=path)

    def degree_of_separation(self, n1, n2):
        """ determines the degree of separation between 2 nodes
        :param n1: node
        :param n2: node
        :return: degree
        """
        return degree_of_separation(self, n1, n2)