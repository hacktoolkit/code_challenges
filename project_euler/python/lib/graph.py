"""graph.py

A set of data strucutres and algorithms for graphs, trees, etc

Test cases:
- 107
"""

# Python Standard Library Imports
import copy
import json


class GraphEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Tree):
            return obj.as_json()
        elif isinstance(obj, Edge):
            return obj.as_json()
        elif type(obj) == set:
            return list(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class Graph:
    def __init__(self, vertices=None, edges=None):
        self.vertices = vertices or set()
        self.edges = edges or []

    @classmethod
    def from_matrix(cls, matrix, directed=True):
        vertices = {
            x
            for x
            in range(len(matrix))
        }

        edges = []
        visited_edges = {}
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if directed:
                    a, b = i, j
                else:
                    # sort vertices to prevent adding duplicate edges
                    a, b = sorted([i, j])

                weight = matrix[a][b]
                edge_key = f'{a}.{b}'

                if weight is not None and edge_key not in visited_edges:
                    edge = Edge(a, b, weight)
                    edges.append(edge)
                    visited_edges[edge_key] = True

        graph = Graph(vertices, edges)
        return graph

    @property
    def cost(self):
        total = sum([edge.weight for edge in self.edges])
        return total

    def get_mst(self):
        mst = self.kruskals()
        return mst

    def kruskals(self):
        """Builds a minimum spanning tree using Kruskal's algorithm

        https://en.wikipedia.org/wiki/Kruskal's_algorithm

        - create a forest F (a set of trees), where each vertex in the graph is a separate tree
        - create a set S containing all the edges in the graph
        - while S is nonempty and F is not yet spanning
          - remove an edge with minimum weight from S
          - if the removed edge connects two different trees then add it to the forest F, combining two trees into a single tree

        At the termination of the algorithm, the forest forms a minimum spanning forest of the graph. If the graph is connected, the forest has a single component and forms a minimum spanning tree.
        """
        forest = [
            Tree(x)
            for x
            in self.vertices
        ]

        edges = sorted(
            copy.copy(self.edges),
            key=lambda edge: edge.weight
        )

        while len(edges) > 0:
            edge = edges.pop(0)

            tree1 = None
            tree2 = None

            for i in range(len(forest)):
                tree = forest[i]
                if tree.has_connection(edge):
                    tree1 = tree
                    for j in range(i + 1, len(forest)):
                        tree2 = forest[j]
                        if tree2.has_connection(edge):
                            tree1.add_edge(edge)
                            tree1.merge(tree2)
                            forest.pop(j)
                            break
                        else:
                            pass
                    if tree2:
                        break
                else:
                    pass

            if len(forest) == 1:
                break

        mst = forest[0]
        print(mst)
        return mst


class Tree:
    def __init__(self, vertex):
        self.vertices = { vertex }
        self.edges = []

    def __str__(self):
        s = f'Tree({json.dumps(self.as_json(), indent=2, cls=GraphEncoder)})'
        return s

    def as_json(self):
        value = {
            'vertices': self.vertices,
            'edges': self.edges,
            'cost': self.cost,
        }
        return value

    @property
    def cost(self):
        total = sum([edge.weight for edge in self.edges])
        return total

    def add_edge(self, edge):
        self.edges.append(edge)

    def merge(self, tree):
        """Merges another `tree` into this `Tree`
        """
        self.vertices = self.vertices.union(tree.vertices)
        self.edges.extend(tree.edges)

    def has_connection(self, edge):
        result = edge.src in self.vertices or edge.dest in self.vertices
        return result


class Edge:
    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight

    def __str__(self):
        s = f'Edge({json.dumps(self.as_json(), indent=2)})'
        return s

    def as_json(self):
        value = {
            'src': self.src,
            'dest': self.dest,
            'weight': self.weight,
        }
        return value
