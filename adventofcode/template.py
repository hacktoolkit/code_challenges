# Python Standard Library Imports
import copy
import math
import re
import typing as T
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

# Third Party (PyPI) Imports
import click

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
)


EXPECTED_ANSWERS = (None, None)
TEST_CASES = {
    '': (None, None),
    # 'b': (None, None),
    # 'c': (None, None),
}


YEAR = int(Path.cwd().parts[-1])
DAY = int(Path(__file__).stem)
PROBLEM_NUM = str(DAY).zfill(2)


@click.command()
@click.option('--is_real', '--real', is_flag=True, default=False)
@click.option('--submit', is_flag=True, default=False)
@click.option('--is_debug', '--debug', is_flag=True, default=False)
def main(is_real, submit, is_debug):
    config.TEST_MODE = not is_real
    config.DEBUGGING = is_debug

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

    inputs = []

    if config.TEST_MODE:
        for test_variant, expected_answers in TEST_CASES.items():

            input_filename = f'{PROBLEM_NUM}{test_variant}.test.in'
            inputs.append((input_filename, expected_answers))
    else:
        input_filename = f'{PROBLEM_NUM}.in'
        expected_answers = EXPECTED_ANSWERS
        inputs.append((input_filename, expected_answers))

    for input_filename, expected_answers in inputs:
        print(f'Running with input file: {input_filename}')

        solution = Solution(
            input_filename,
            input_config,
            expected_answers,
            year=YEAR,
            day=DAY,
        )

        solution.solve()
        if submit:
            solution.submit(is_test=config.TEST_MODE)
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
