#!/usr/bin/env python3
"""http://projecteuler.net/problem=107

Minimal network

The following undirected network consists of seven vertices and twelve edges with a total weight of 243.



The same network can be represented by the matrix below.


-,A,B,C,D,E,F,G
A,-,16,12,21,-,-,-
B,16,-,-,17,20,-,-
C,12,-,-,28,-,31,-
D,21,17,28,-,18,19,23
E,-,20,-,18,-,-,11
F,-,-,31,19,-,-,27
G,-,-,-,23,11,27,-


However, it is possible to optimise the network by removing some edges and still ensure that all points on the network remain connected. The network which achieves the maximum saving is shown below. It has a weight of 93, representing a saving of 243 - 93 = 150 from the original network.


Using network.txt (right click and 'Save Link/Target As...'), a 6K text file containing a network with forty vertices, and given in matrix form, find the maximum saving which can be achieved by removing redundant edges whilst ensuring that the network remains connected.

Solution by jontsai <hello@jontsai.com>
"""
# PE Solution Library Imports
from lib.graph import Graph
from utils import *


class Solution(object):
    TEST_NETWORK = """-,16,12,21,-,-,-
16,-,-,17,20,-,-
12,-,-,28,-,31,-
21,17,28,-,18,19,23
-,20,-,18,-,-,11
-,-,31,19,-,-,27
-,-,-,23,11,27,-
"""

    # EXPECTED_ANSWER = 150
    EXPECTED_ANSWER = 259679

    def __init__(self):
        pass

    def build_matrix(self, network):
        matrix = [
            [
                None if x == '-' else int(x)
                for x
                in line.strip().split(',')
            ]
            for line
            in network.strip().split('\n')
        ]
        return matrix

    def solve(self):
        answer = None

        # network = self.TEST_NETWORK
        with open('p107_network.txt', 'r') as f:
            network = f.read()

        matrix = self.build_matrix(network)
        graph = Graph.from_matrix(matrix, directed=False)

        cost = graph.cost
        tree = graph.get_mst()
        savings = cost - tree.cost

        answer = savings

        return answer


def main():
    solution = Solution()
    answer = solution.solve()

    print(f'Expected: {Solution.EXPECTED_ANSWER}, Answer: {answer}')


if __name__ == '__main__':
    main()
