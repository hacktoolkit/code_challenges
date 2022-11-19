# Python Standard Library Imports
import copy
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
)


PROBLEM_NUM = '07'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (
    'ABGKCMVWYDEHFOPQUILSTNZRJX',
    None,
)
TEST_EXPECTED_ANSWERS = (
    'CABDFE',
    None,
)


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=False,
        row_func=None,
        cell_func=None,
    )

    if TEST_MODE:
        input_filename = f'{PROBLEM_NUM}.test.in'
        expected_answers = TEST_EXPECTED_ANSWERS
    else:
        input_filename = f'{PROBLEM_NUM}.in'
        expected_answers = EXPECTED_ANSWERS

    solution = Solution(input_filename, input_config, expected_answers)

    solution.solve()
    solution.report()


class Solution(BaseSolution):
    def process_data(self):
        data = self.data

        pattern = re.compile(
            r'^Step (?P<source>[A-Z]) must be finished before step (?P<sink>[A-Z]) can begin\.$'
        )

        graph = Graph()

        for line in data:
            m = pattern.match(line)
            source = Vertex.get_or_create(m.group('source'))
            sink = Vertex.get_or_create(m.group('sink'))
            edge = Edge(source, sink)

            graph.add_edge(edge)

        self.graph = graph

    def solve1(self):
        graph = self.graph
        vertices = graph.topological_sort(strategy=DataStructure.HEAP)
        answer = ''.join([vertex.label for vertex in vertices])
        return answer

    def solve2(self):
        #
        # TODO: FILL THIS IN
        #
        answer = None
        return answer


if __name__ == '__main__':
    main()
