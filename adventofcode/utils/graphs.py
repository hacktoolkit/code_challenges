# Python Standard Library Imports
import heapq
from collections import deque
from enum import Enum


class DataStructure(Enum):
    HEAP = 'heap'
    DEQUE = 'deque'


class Graph:
    def __init__(self):
        self.vertices = set()
        self.edges = set()

    def add_vertex(self, vertex):
        self.vertices.add(vertex)

    def add_edge(self, edge):
        self.edges.add(edge)
        self.add_vertex(edge.source)
        self.add_vertex(edge.sink)

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

        while len(S):
            if strategy == DataStructure.HEAP:
                n = heapq.heappop(S)
            elif strategy == DataStructure.DEQUE:
                n = S.popleft()

            L.append(n)
            for e in sorted(n.out_edges, key=lambda edge: edge.sink.label):
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


class Vertex:
    _cache = {}

    def __init__(self, label):
        self.label = label
        self.out_edges = set()
        self.in_edges = set()

    @classmethod
    def get_or_create(cls, label):
        if label in cls._cache:
            vertex = cls._cache[label]
        else:
            vertex = Vertex(label)
            cls._cache[label] = vertex

        return vertex

    def __str__(self):
        return self.label

    def __lt__(self, other):
        return self.label < other.label

    def __le__(self, other):
        raise Exception('Illegal operation <=')

    def __eq__(self, other):
        return id(self) == id(other)

    def __ne__(self, other):
        return id(self) != id(other)

    def __gt__(self, other):
        return self.label > other.label

    def __ge__(self, other):
        raise Exception('Illegal operation >=')

    def __hash__(self):
        return id(self)

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
    def __init__(self, source, sink):
        self.source = source
        self.sink = sink

        source.add_outgoing_edge(self)
        sink.add_incoming_edge(self)
