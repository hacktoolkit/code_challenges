# Python Standard Library Imports
import copy
import heapq
import math
import re
from collections import defaultdict
from dataclasses import dataclass

from utils import (
    BaseSolution,
    DataStructure,
    Edge,
    Graph,
    InputConfig,
    Vertex,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (
    'ABGKCMVWYDEHFOPQUILSTNZRJX',
    898,  # ABGYKMWCEVDHOFQUPILTSNZRJX
)
config.TEST_CASES = {
    '': (
        'CABDFE',
        15,  #  CABFDE
    )
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        # data = self.data
        pass

    def build_graph(self):
        graph = P7Graph()

        pattern = re.compile(
            r'^Step (?P<source>[A-Z]) must be finished before step (?P<sink>[A-Z]) can begin\.$'
        )

        base_cost = 0 if config.TEST_MODE else 60

        for line in self.data:
            m = pattern.match(line)

            source_label = m.group('source')
            sink_label = m.group('sink')

            source_weight = base_cost + ord(source_label) - ord('A') + 1
            sink_weight = base_cost + ord(sink_label) - ord('A') + 1

            source = Vertex.get_or_create(source_label, weight=source_weight)
            sink = Vertex.get_or_create(sink_label, weight=sink_weight)

            edge = Edge(source, sink)

            graph.add_edge(edge)

        return graph

    def solve1(self):
        graph = self.build_graph()
        vertices = graph.topological_sort(strategy=DataStructure.HEAP)

        order = ''.join([vertex.label for vertex in vertices])
        answer = order
        return answer

    def solve2(self):
        graph = self.build_graph()
        n_workers = 2 if config.TEST_MODE else 5
        vertices, elapsed = graph.toposort_traverse_n_workers(n_workers)

        order = ''.join([vertex.label for vertex in vertices])
        print(order)

        answer = elapsed
        return answer


class P7Graph(Graph):
    def toposort_traverse_n_workers(self, n_workers):
        """Modified topological sort using Kahn's algorithm

        Like a topological sort, but "root nodes" go into a work queue to be worked on by workers first, instead of directly on to L

        Pseudocode:

        L ← Empty list that will contain the sorted elements
        S ← Set of all nodes with no incoming edge
        W ← Pool of workers

        while S is not empty or W is not empty do
            while W has an available worker do
                remove a node n with least weight from S
                add n to W (GRAY)

            C ← Empty list
            n, w ← Pop node n having min weight w amongs nodes in W
            add n to C

            for m in W do
                subtract w from m.weight
                if m.weight == 0
                    move m from W to C

            for n in C do
                add n to L (BLACK)

                for each node m with an edge e from n to m do
                    remove edge e from the graph
                    if m has no other incoming edges then
                        insert m into S

        if graph has edges then
            return error   (graph has at least one cycle)
        else
            return L   (a topologically sorted order)
        """
        L = []

        root_vertices = [
            vertex
            for vertex in sorted(
                self.vertices,
                key=lambda vertex: vertex.label,
            )
            if vertex.is_root
        ]

        S = []
        for vertex in root_vertices:
            heapq.heappush(S, vertex)

        W = []

        edges = set(self.edges)

        elapsed = 0

        def debug_state():
            S_str = ', '.join([f'{x.label} ({x.weight})' for x in S]) or '[]'
            W_str = ', '.join([f'{x.label} ({x.weight})' for x in W]) or '[]'
            L_str = ''.join([x.label for x in L]) or '[]'

            debug(f'S: {S_str} | W: {W_str} | L: {L_str}')

        debug_state()
        while (len(S) + len(W)) > 0:
            debug('-------------')
            while len(W) < n_workers and len(S) > 0:
                n = heapq.heappop(S)
                heapq.heappush(W, n)
                debug(f'Move {n.label} from S to W')

            debug_state()

            # perform 1 round of work
            # collect all nodes who complete on this turn in C
            C = []
            n = heapq.heappop(W)
            weight = n.weight
            n.weight = 0
            elapsed += weight
            C.append(n)
            debug(f'Queueing {n.label} ({weight}) for completion')

            for m in W:
                m.weight -= weight

            heapq.heapify(W)
            while len(W) > 0 and W[0].weight == 0:
                n = heapq.heappop(W)
                C.append(n)

            debug(f'Completed: {"".join([x.label for x in C])}')

            for n in C:
                L.append(n)

                for e in sorted(n.out_edges, key=lambda edge: edge.sink.weight):
                    m = e.sink
                    edges.remove(e)
                    m.remove_incoming_edge(e)
                    if len(m.in_edges) == 0:
                        heapq.heappush(S, m)
                        debug(f'Moving {n.label} edge {m.label} to S')

            debug_state()

        if len(edges) > 0:
            raise Exception('Detected cycle in graph')
        else:
            return L, elapsed


if __name__ == '__main__':
    main()
