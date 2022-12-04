# Python Standard Library Imports
import copy
import math
import re
import typing as T
from collections import defaultdict
from dataclasses import dataclass

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '24'

TEST_MODE = False
TEST_MODE = True

EXPECTED_ANSWERS = (None, None)
TEST_VARIANT = ''  # '', 'b', 'c', 'd', ...
TEST_EXPECTED_ANSWERS = {
    '': (None, None),
    'b': (None, None),
    'c': (None, None),
}

DEBUGGING = False
DEBUGGING = True


def debug(s):
    if DEBUGGING:
        print(s)
    else:
        pass


def main():
    input_config = InputConfig(
        as_integers=True,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_coordinates=False,
        coordinate_delimeter=None,
        as_table=False,
        row_func=None,
        cell_func=None,
    )

    if TEST_MODE:
        input_filename = f'{PROBLEM_NUM}{TEST_VARIANT}.test.in'
        expected_answers = TEST_EXPECTED_ANSWERS[TEST_VARIANT]
    else:
        input_filename = f'{PROBLEM_NUM}.in'
        expected_answers = EXPECTED_ANSWERS

    solution = Solution(input_filename, input_config, expected_answers)

    solution.solve()
    solution.report()


class Solution(BaseSolution):
    def process_data(self):
        data = self.data

    def solve1(self):
        sleigh = Sleigh(self.data)
        optimal_arrangement = sleigh.find_optimal_arrangement()

        answer = optimal_arrangement.quantum_entanglement
        return answer

    def solve2(self):
        #
        # TODO: FILL THIS IN
        #
        answer = None
        return answer


class Sleigh:
    def __init__(self, weights):
        self.weights = weights
        self.limit = sum(weights) // 3

    class Arrangement:
        def __init__(self, weights):
            self.weights = weights
            self.key = tuple(sorted(weights))

        def __hash__(self):
            return self.key

        @property
        def quantum_entanglement(self):
            return math.prod(self.weights)

        def __cmp__(self, other):
            if len(self.weights) < len(other.weights):
                result = -1
            elif len(self.weights) == len(other.weights):
                result = (
                    -1
                    if self.quantum_entanglement < other.quantum_entanglement
                    else 0
                    if self.quantum_entanglement == other.quantum_entanglement
                    else 1
                )
            else:
                result = 1
            return result

    def find_optimal_arrangement(self):
        arrangements = self.make_arrangements()
        print('ddi we find any?')
        print(arrangements)
        print('ddi we? DID WE?')
        optimal_arrangement = sorted(arrangements)[0]
        return optimal_arrangement

    def make_arrangements(
        self, remain_weights=None, used_weights=None, limit=None
    ):
        """While the large problem is to find all arrangments:

        `[c1, c2, c3]` such that `sum(c1) == sum(c2) == sum(c3) == self.limit`

        An optimization can be made to simply find all _possible_ arrangements for 1 compartment
        """
        if remain_weights is None:
            remain_weights = self.weights

        if used_weights is None:
            used_weights = set()

        if limit is None:
            limit = None

        arrangements = self.make_sub_arrangements(
            remain_weights, used_weights, limit=self.limit
        )

        return arrangements

    def make_sub_arrangements(self, remain_weights, used_weights, limit):
        print(remain_weights, used_weights, limit)
        arrangements = set()

        if limit == 0:
            # print('got here')
            arrangements.add(tuple(sorted(used_weights)))
        elif len(remain_weights) == 0:
            print('case b')
            # no more weights to add, incomplete arrangement
            pass
        else:
            # print('case c')
            for w in sorted(remain_weights, reverse=True):
                if w + sum(used_weights) <= limit:
                    print(f'adding {w} to {used_weights}')
                    next_remain_weights = copy.copy(remain_weights)
                    next_remain_weights.remove(w)
                    next_used_weights = copy.copy(used_weights)
                    next_used_weights.add(w)

                    # print(next_remain_weights, next_used_weights)

                    # print(f'before: {arrangements}')

                    arrangements = arrangements.union(
                        self.make_sub_arrangements(
                            next_remain_weights,
                            next_used_weights,
                            limit - w,
                        )
                    )

                    # print(f'after: {arrangements}')
                else:
                    # weight w is too large for arrangement
                    print(f'here we are: {w}')
                    pass

        return arrangements


if __name__ == '__main__':
    main()
