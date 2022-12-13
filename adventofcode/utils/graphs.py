# Python Standard Library Imports
import heapq
import typing as T
from collections import deque
from enum import Enum

# Local Imports
from . import debug
from .q import PriorityQueue


class DataStructure(Enum):
    HEAP = 'heap'
    DEQUE = 'deque'


class TriColor(Enum):
    """Tricolor algorithm

    Source: https://www.cs.cornell.edu/courses/cs2112/2012sp/lectures/lec24/lec24-12sp.html

    Abstractly, graph traversal can be expressed in terms of the tricolor algorithm due to Dijkstra and others. In this algorithm, graph nodes are assigned one of three colors that can change over time:

    White nodes are undiscovered nodes that have not been seen yet in the current traversal and may even be unreachable.
    Black nodes are nodes that are reachable and that the algorithm is done with.
    Gray nodes are nodes that have been discovered but that the algorithm is not done with yet. These nodes are on a frontier between white and black.
    The progress of the algorithm is depicted by the following figure. Initially there are no black nodes and the roots are gray. As the algorithm progresses, white nodes turn into gray nodes and gray nodes turn into black nodes. Eventually there are no gray nodes left and the algorithm is done.


    The algorithm maintains a key invariant at all times: there are no edges from white nodes to black nodes. This is clearly true initially, and because it is true at the end, we know that any remaining white nodes cannot be reached from the black nodes.

    The algorithm pseudo-code is as follows:

    Color all nodes white, except for the root nodes, which are colored gray.
    While some gray node n exists:
    color some white successors of n gray.
    if n has no white successors, optionally color n black.
    This algorithm is abstract enough to describe many different graph traversals. It allows the particular implementation to choose the node n from among the gray nodes; it allows choosing which and how many white successors to color gray, and it allows delaying the coloring of gray nodes black. We says that such an algorithm is nondeterministic because its behavior is not fully defined. However, as long as it does some work on each gray node that it picks, any implementation that can be described in terms of this algorithm will finish. Further, because the black-white invariant is maintained, it must reach all reachable nodes in the graph.

    One value of defining graph search in terms of the tricolor algorithm is that the tricolor algorithm works even when gray nodes are worked on concurrently, as long as the black-white invariant is maintained. Thinking about this invariant therefore helps us ensure that whatever graph traversal we choose will work when parallelized, which is increasingly important.
    """

    WHITE = 'white'
    GRAY = 'gray'
    BLACK = 'black'


class Graph:
    def __init__(self, INFINITY=10**9):
        """Initialized `Graph` object

        Parameters:
        `INFINITY` - Used for calculating shortest paths in Dijkstra's algorithm.
          Defaults to 1B, but can be any number higher than the rest of the expected shortest paths.
        """
        self.INFINITY = INFINITY

        self.vertices_by_label = {}
        self.vertices = set()
        self.edges = set()

    ##
    #  Accessors

    def add_vertex(self, vertex, map_by_label=False):
        self.vertices.add(vertex)

        if map_by_label:
            self.vertices_by_label[vertex.label] = vertex

    def add_edge(self, edge):
        self.edges.add(edge)
        self.add_vertex(edge.source)
        self.add_vertex(edge.sink)

    def neighbors_of(self, vertex) -> T.Collection[T.Tuple['Vertex', int]]:
        """Finds the neighbors of `vertex`

        This method MAY be overwritten if reusing `Vertex.in_edges` or `Vertex.out_edges`
        This method SHOULD be overwritten if finding neighbors is custom

        Returns a collection of `(Vertex, edge-weight)` pairs
        """

        neighbors = [(edge.sink, edge.sink.weight) for edge in vertex.out_edges]
        return neighbors

    ##
    # Sorting Algorithms

    def topological_sort(self, strategy=None):
        if strategy is None:
            strategy = DataStructure.HEAP
            # strategy = DataStructure.DEQUE

        return self.topological_sort__kahn(strategy=strategy)

    def topological_sort__kahn(self, strategy=None):
        """Performs topological sort using Kahn's algorithm

        https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm

        Pseudocode:

        L ← Empty list that will contain the sorted elements
        S ← Set of all nodes with no incoming edge

        while S is not empty do
            remove a node n from S
            add n to L
            for each node m with an edge e from n to m do
                remove edge e from the graph
                if m has no other incoming edges then
                    insert m into S

        if graph has edges then
            return error   (graph has at least one cycle)
        else
            return L   (a topologically sorted order)

        """
        if strategy is None:
            strategy = DataStructure.HEAP

        L = []

        root_vertices = [
            vertex
            for vertex in sorted(
                self.vertices,
                key=lambda vertex: vertex.label,
            )
            if vertex.is_root
        ]

        if strategy == DataStructure.HEAP:
            S = []
            for vertex in root_vertices:
                heapq.heappush(S, vertex)
        elif strategy == DataStructure.DEQUE:
            S = deque(root_vertices)

        edges = set(self.edges)

        while len(S) > 0:
            if strategy == DataStructure.HEAP:
                n = heapq.heappop(S)
            elif strategy == DataStructure.DEQUE:
                n = S.popleft()

            L.append(n)

            for e in sorted(n.out_edges, key=lambda edge: edge.sink):
                m = e.sink
                edges.remove(e)
                m.remove_incoming_edge(e)
                if len(m.in_edges) == 0:
                    if strategy == DataStructure.HEAP:
                        heapq.heappush(S, m)
                    elif strategy == DataStructure.DEQUE:
                        S.append(m)

        if len(edges) > 0:
            raise Exception('Detected cycle in graph')
        else:
            return L

    ##
    # Pathfinding Algorithms

    def shortest_path(self, source, target):
        path, distance = self.shortest_path__dijkstra__priority_queue(
            source, target
        )
        return path, distance

    def shortest_path__dijkstra__priority_queue(self, source, target):
        """Calculates the shortest path to traverse a graph from `source` to `target` vertices

        CAVEAT: Dijkstra's algorithm does not work with negative edge weights

        References:
        - https://en.wikipedia.org/wiki/Pathfinding
        - https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Using_a_priority_queue
        - https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
        """
        dist = {}  # best distances to `target` from `v`
        prev = {}  # predecessors of `v`
        Q = PriorityQueue()

        dist[source] = 0
        Q.add_with_priority(source, 0)

        for v in self.vertices:
            if v != source:
                dist[v] = self.INFINITY  # unknown distance from source to `v`
                prev[v] = None  # predecessor of `v`

        # the main loop
        while not Q.is_empty:
            priority, u = Q.extract_min()  # remove and return best vertex

            # go through all `v` neighbors of `u`
            for v, edge_weight in self.neighbors_of(u):
                alt = dist[u] + edge_weight
                if alt < dist[v]:
                    # current known shortest path to `v` is...
                    dist[v] = alt  # with distance `alt`
                    prev[v] = u  # through vertex `u`

                    if not Q.contains(v):
                        Q.add_with_priority(v, alt)

            if u == target:
                # break as soon as `target` is reached
                # no need to calculate shortest path between every pair of vertices
                break

        S = []  # holds the shortest path, or empty if None
        u = target
        if u in prev or u == source:
            while u is not None:
                S.append(u)
                u = prev.get(u)

        path = list(reversed(S))
        distance = sum([v.weight for v in S])

        return path, distance


class Vertex:
    _cache = {}

    def __init__(self, label, weight: T.Optional[int] = None):
        self.label = label
        self.weight = weight

        self.color = TriColor.WHITE

        self.out_edges = set()
        self.in_edges = set()

    def __str__(self):
        return f'{self.label} ({self.weight})'

    @classmethod
    def reset(cls):
        cls._cache = {}

    @classmethod
    def get_or_create(cls, label, weight=None):
        if label in cls._cache:
            vertex = cls._cache[label]
        else:
            vertex = Vertex(label, weight=weight)
            cls._cache[label] = vertex

        return vertex

    def __str__(self):
        return self.label

    def __lt__(self, other):
        if (
            self.weight is not None
            and other.weight is not None
            and self.weight != other.weight
        ):
            result = self.weight < other.weight
        else:
            result = self.label < other.label
        return result

    def __le__(self, other):
        raise Exception('Illegal operation <=')

    def __eq__(self, other):
        return id(self) == id(other)

    def __ne__(self, other):
        return id(self) != id(other)

    def __gt__(self, other):
        if (
            self.weight is not None
            and other.weight is not None
            and self.weight != other.weight
        ):
            result = self.weight > other.weight
        else:
            result = self.label > other.label
        return result

    def __ge__(self, other):
        raise Exception('Illegal operation >=')

    def __hash__(self):
        h = id(self)
        return h

    @property
    def is_root(self):
        return len(self.in_edges) == 0

    @property
    def is_leaf(self):
        return len(self.out_edges) == 0

    def add_outgoing_edge(self, edge):
        self.out_edges.add(edge)

    def add_incoming_edge(self, edge):
        self.in_edges.add(edge)

    def remove_outgoing_edge(self, edge):
        self.out_edges.remove(edge)

    def remove_incoming_edge(self, edge):
        self.in_edges.remove(edge)


class Edge:
    def __init__(self, source, sink, weight: T.Optional[int] = None):
        self.source = source
        self.sink = sink
        self.weight = weight

        source.add_outgoing_edge(self)
        sink.add_incoming_edge(self)
