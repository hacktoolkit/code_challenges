# Python Standard Library Imports
import copy
import math
import pathlib
import re
import typing as T
from collections import defaultdict
from dataclasses import dataclass

# Third Party (PyPI) Imports
import click

from utils import (
    BaseSolution,
    InputConfig,
)


EXPECTED_ANSWERS = (None, None)
TEST_VARIANT = ''  # '', 'b', 'c', 'd', ...
TEST_EXPECTED_ANSWERS = {
    '': (None, None),
    'b': (None, None),
    'c': (None, None),
}


YEAR = int(pathlib.Path.cwd().parts[-1])
DAY = int(pathlib.Path(__file__).stem)
PROBLEM_NUM = str(DAY).zfill(2)

TEST_MODE = True
DEBUGGING = False


def debug(*args):
    if DEBUGGING:
        print(*args)
    else:
        pass


@click.command()
@click.option('--is_real', '--real', is_flag=True, default=False)
@click.option('--submit', is_flag=True, default=False)
@click.option('--is_debug', '--debug', is_flag=True, default=False)
def main(is_real, submit, is_debug):
    global TEST_MODE
    global DEBUGGING
    TEST_MODE = not is_real
    DEBUGGING = is_debug

    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        strip_lines=True,
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

    solution = Solution(
        input_filename,
        input_config,
        expected_answers,
        year=YEAR,
        day=DAY,
    )

    solution.solve()
    if submit:
        solution.submit(is_test=TEST_MODE)
    solution.report()


class Solution(BaseSolution):
    def process_data(self):
        data = self.data

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
