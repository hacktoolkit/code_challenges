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


PROBLEM_NUM = '04'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (483, 874)
TEST_VARIANT = ''  # '', 'b', 'c', 'd', ...
TEST_EXPECTED_ANSWERS = {
    '': (2, 4),
    'b': (None, None),
    'c': (None, None),
}

DEBUGGING = False
# DEBUGGING = True


def debug(*args):
    if DEBUGGING:
        print(*args)
    else:
        pass


def main():
    input_config = InputConfig(
        as_integers=False,
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
    REGEX = re.compile(r'^(?P<a>\d+)-(?P<b>\d+),(?P<c>\d+)-(?P<d>\d+)$')

    def process_data(self):
        data = self.data

    def solve1(self):
        total = 0
        for line in self.data:
            m = self.REGEX.match(line)
            a, b, c, d = map(int, [m.group(_) for _ in 'abcd'])
            debug(a, b, c, d)

            s1 = set(range(a, b + 1))
            s2 = set(range(c, d + 1))

            if len(s1 | s2) == max(len(s1), len(s2)):
                total += 1

        answer = total
        return answer

    def solve2(self):
        total = 0
        for line in self.data:
            m = self.REGEX.match(line)
            a, b, c, d = map(int, [m.group(_) for _ in 'abcd'])
            debug(a, b, c, d)

            s1 = set(range(a, b + 1))
            s2 = set(range(c, d + 1))

            if len(s1 | s2) < len(s1) + len(s2):
                total += 1

        answer = total
        return answer


if __name__ == '__main__':
    main()
