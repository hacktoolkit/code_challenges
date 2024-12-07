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
from htk import fdb  # noqa: F401

from utils import debug  # noqa: F401
from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (None, None)
config.TEST_CASES = {
    '': (None, None),
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
config.INPUT_CONFIG.as_table = False
config.INPUT_CONFIG.row_func = None
config.INPUT_CONFIG.cell_func = None


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data

    def solve1(self) -> T.Optional[int]:
        #
        # TODO: FILL THIS IN
        #
        answer = None
        return answer

    def solve2(self) -> T.Optional[int]:
        #
        # TODO: FILL THIS IN
        #
        answer = None
        return answer


if __name__ == '__main__':
    main()
