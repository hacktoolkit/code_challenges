# Python Standard Library Imports
import copy
import heapq
import math
import re
import typing as T
from collections import (
    defaultdict,
    deque,
)
from dataclasses import (
    dataclass,
    field,
)
from functools import (
    cache,
    lru_cache,
)

# Third Party (PyPI) Imports
from htk import fdb

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (12643, None)
config.TEST_CASES = {
    '': (2, 2),
    'b': (6, 6),
    # 'c': (None, None),
}

config.INPUT_CONFIG.as_groups = True


@solution
class Solution(BaseSolution):
    def process_data(self):
        self.network_map = NetworkMap(self.data[0][0], self.data[1])

    def solve1(self):
        answer = self.network_map.traverse('AAA', 'ZZZ')
        return answer

    def solve2(self):
        answer = self.network_map.traverse_as_ghost('A', 'Z')
        return answer


class NetworkMap:
    NODE_PATTERN = re.compile(
        r'^(?P<node>[A-Z]+) = \((?P<left>[A-Z]+), (?P<right>[A-Z]+)\)$'
    )

    def __init__(self, raw_dirs, raw_nodes):
        self.directions = raw_dirs
        self.num_dirs = len(self.directions)
        self.nodes = {}

        self.steps = 0

        for raw_node in raw_nodes:
            if RE.match(self.NODE_PATTERN, raw_node):
                node, left, right = (
                    RE.m.group('node'),
                    RE.m.group('left'),
                    RE.m.group('right'),
                )
                self.nodes[node] = (left, right)
            else:
                raise Exception(f'Invalid node: {raw_node}')

    def traverse(self, start_node, end_node):
        self.steps = 0

        def _next(node):
            direction = self.directions[self.steps % self.num_dirs]
            pointer = 0 if direction == 'L' else 1
            next_node = self.nodes[node][pointer]

            self.steps += 1

            return next_node

        cur_node = start_node

        while cur_node != end_node:
            cur_node = _next(cur_node)

        return self.steps

    def traverse_as_ghost(self, start_node_suffix, end_node_suffix):
        self.steps = 0

        def _is_finished(nodes):
            return all(node.endswith(end_node_suffix) for node in nodes)

        def _next(nodes):
            direction = self.directions[self.steps % self.num_dirs]
            pointer = 0 if direction == 'L' else 1

            next_nodes = [self.nodes[node][pointer] for node in nodes]

            self.steps += 1

            return next_nodes

        cur_nodes = [
            node for node in self.nodes if node.endswith(start_node_suffix)
        ]

        while not _is_finished(cur_nodes):
            cur_nodes = _next(cur_nodes)

        return self.steps


if __name__ == '__main__':
    main()
