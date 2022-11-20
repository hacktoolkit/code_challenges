# Python Standard Library Imports
import copy
import math
import re
from collections import defaultdict
from dataclasses import dataclass

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '06'

TEST_MODE = False
TEST_MODE = True

EXPECTED_ANSWERS = (
    None,
    None,
)
TEST_EXPECTED_ANSWERS = (
    None,
    None,
)

DEBUGGING = False
# DEBUGGING = True


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
        as_groups=False,
        as_oneline=False,
        as_coordinates=True,
        coordinate_delimeter=', ',
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
        print(data)

    def solve1(self):
        #
        # TODO: FILL THIS IN
        #
        answer = None
        return answer

    def solve2(self):
        #
        # TODO: FILL THIS IN
        #
        answer = None
        return answer


if __name__ == '__main__':
    main()
