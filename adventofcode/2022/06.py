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


EXPECTED_ANSWERS = (1198, 3120)
TEST_VARIANT = ''  # '', 'b', 'c', 'd', ...
TEST_EXPECTED_ANSWERS = {
    '': (7, 19),
    'b': (5, 23),
    'c': (6, 23),
    'd': (10, 29),
    'e': (11, 26),
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
        self.s = data[0]

    def solve1(self):
        s = self.s
        answer = find_first_marker(s)
        return answer

    def solve2(self):
        s = self.s
        answer = find_first_packet(s)
        return answer


def find_first_marker(s, L=4):
    debug(s)

    i = 0
    j = None
    found_marker = False

    while not found_marker:
        j = i + L
        candidate = s[i:j]
        if len(set(candidate)) < L:
            i += 1
        elif len(set(candidate)) == L:
            debug(candidate, j)
            found_marker = True

    return j


def find_first_packet(s, L=14):
    return find_first_marker(s, L=L)


if __name__ == '__main__':
    main()
