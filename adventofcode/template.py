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


config.YEAR = int(Path.cwd().parts[-1])
config.DAY = int(Path(__file__).stem)
config.PROBLEM_NUM = str(config.DAY).zfill(2)


@solution
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
