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


config.EXPECTED_ANSWERS = (1834060, 21607792)
config.TEST_CASES = {
    '': (11, 31),
    # 'b': (None, None),
    # 'c': (None, None),
}

config.INPUT_CONFIG.as_integers = False
config.INPUT_CONFIG.as_comma_separated_integers = False
config.INPUT_CONFIG.as_json = False
config.INPUT_CONFIG.as_groups = False
config.INPUT_CONFIG.strip_lines = True
config.INPUT_CONFIG.as_oneline = False
config.INPUT_CONFIG.as_coordinates = False
config.INPUT_CONFIG.coordinate_delimeter = None
config.INPUT_CONFIG.as_table = True
config.INPUT_CONFIG.row_func = None
config.INPUT_CONFIG.cell_func = int


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        col1 = []
        col2 = []
        col2_occurrences = defaultdict(int)
        for row in data:
            col1.append(row[0])
            col2.append(row[1])
            col2_occurrences[row[1]] += 1

        self.col1_sorted = sorted(col1)
        self.col2_sorted = sorted(col2)
        self.col2_occurrences = col2_occurrences

    def solve1(self):
        dist = 0
        for i, (c1, c2) in enumerate(zip(self.col1_sorted, self.col2_sorted)):
            dist += abs(c1 - c2)

        answer = dist
        return answer

    def solve2(self):
        similarity = 0
        for c1 in self.col1_sorted:
            similarity += c1 * self.col2_occurrences[c1]

        answer = similarity
        return answer


if __name__ == '__main__':
    main()
