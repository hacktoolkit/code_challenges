# Python Standard Library Imports
import re
from itertools import permutations

from utils import (
    Re,
    ingest,
)


INPUT_FILE = '9.in'
EXPECTED_ANSWERS = (117, 909, )

# INPUT_FILE = '9.test.in'
# EXPECTED_ANSWERS = (605, 982, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)
        routes = self.data
        self.graph = Graph(routes)

    def solve1(self):
        weight, itinerary = self.graph.tsp()
        answer = weight
        return answer

    def solve2(self):
        weight, itinerary = self.graph.longest_itinerary()
        answer = weight
        return answer


class Graph:
    ROUTE_REGEXP = re.compile(r'^(?P<origin>[A-Za-z]+) to (?P<destination>[A-Za-z]+) = (?P<weight>\d+)$')

    def __init__(self, routes):
        self.nodes = {}

        regex = Re()
        for route in routes:
            if regex.match(self.ROUTE_REGEXP, route):
                m = regex.last_match
                origin_name, destination_name, weight = (
                    m.group('origin'),
                    m.group('destination'),
                    int(m.group('weight')),
                )
                origin = self.get_node(origin_name)
                destination = self.get_node(destination_name)

                origin.add_edge(destination, weight, is_bidirectional=True)
            else:
                raise Exception('Misformatted route: %s' % route)

    def get_node(self, name):
        if name in self.nodes:
            node = self.nodes[name]
        else:
            node = Node(name)
            self.nodes[name] = node

        return node

    def tsp(self):
        """TSP aka Traveling Salesman Problem

        https://en.wikipedia.org/wiki/Travelling_salesman_problem

        Finds the itinerary (list of edges) that would visit each Node
        in this Graph exactly once, with the minimum total weight

        TODO: https://en.wikipedia.org/wiki/Held%E2%80%93Karp_algorithm
        """
        return self._tsp_exhaustive()

    def _tsp_exhaustive(self):
        p = permutations(self.nodes.values())

        best_weight = None
        best_itinerary = None

        for itinerary in p:
            weight = self.tour(itinerary)
            if weight is not None and (best_weight is None or weight < best_weight):
                best_itinerary = itinerary
                best_weight = weight

        return best_weight, best_itinerary

    def longest_itinerary(self):
        p = permutations(self.nodes.values())

        worst_weight = None
        worst_itinerary = None

        for itinerary in p:
            weight = self.tour(itinerary)
            if weight is not None and (worst_weight is None or weight > worst_weight):
                worst_itinerary = itinerary
                worst_weight = weight

        return worst_weight, worst_itinerary

    def tour(self, itinerary):
        """Returns the total weight for visiting each node in order of `itinerary`
        """
        cost = 0

        prev = None
        for node in itinerary:
            if prev is not None:
                edge = prev.edges.get(node)
                if edge:
                    cost += prev.edges[node].weight
                else:
                    cost = None
                    break

            prev = node

        return cost


class Node:
    def __init__(self, name):
        self.name = name
        self.edges = {}

    def add_edge(self, destination, weight, is_bidirectional=False):
        edge = Edge(self, destination, weight)
        self.edges[destination] = edge

        if is_bidirectional:
            destination.add_edge(self, weight)


class Edge:
    def __init__(self, origin, destination, weight):
        self.origin = origin
        self.destination = destination
        self.weight = weight


if __name__ == '__main__':
    main()
