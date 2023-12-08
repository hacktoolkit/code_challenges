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
from itertools import (
    combinations,
    permutations,
    product,
)
from operator import (
    add,
    mul,
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
    '': (2, None),
    'b': (6, None),
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
        #
        # TODO: FILL THIS IN
        #
        answer = None
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

        fdb('%s' % self.nodes)

    def traverse(self, start_node, end_node):
        self.steps = 0

        def _next(node):
            direction = self.directions[self.steps % self.num_dirs]
            fdb(direction)
            pointer = 0 if direction == 'L' else 1
            next_node = self.nodes[node][pointer]

            self.steps += 1

            return next_node

        cur_node = start_node

        while cur_node != end_node:
            cur_node = _next(cur_node)

        return self.steps


if __name__ == '__main__':
    main()
