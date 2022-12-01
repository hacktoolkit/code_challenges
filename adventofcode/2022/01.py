# Python Standard Library Imports
import copy
import heapq
import math
import re
import typing as T
from collections import defaultdict
from dataclasses import dataclass

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '01'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (69912, 208180)
TEST_VARIANT = ''  # '', 'b', 'c', 'd', ...
TEST_EXPECTED_ANSWERS = {
    '': (24000, 45000),
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
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=True,
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
        max_calories = None
        for elf in self.data:
            calories = sum([int(x) for x in elf])
            if max_calories is None or calories > max_calories:
                max_calories = calories

        answer = max_calories
        return answer

    def solve2(self):
        podium = []
        for elf in self.data:
            calories = sum([int(x) for x in elf])
            heapq.heappush(podium, calories)
            podium = heapq.nlargest(3, podium)

        answer = sum(podium)
        return answer


if __name__ == '__main__':
    main()
