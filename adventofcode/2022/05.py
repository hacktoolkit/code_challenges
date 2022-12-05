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


EXPECTED_ANSWERS = ('LJSVLTWQM', 'BRQWDBBJM')
TEST_VARIANT = ''  # '', 'b', 'c', 'd', ...
TEST_EXPECTED_ANSWERS = {
    '': ('CMZ', 'MCD'),
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
        as_groups=True,
        strip_lines=False,
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

    def solve1(self) -> str:
        crates = Crates(self.data[0], self.data[1])
        debug(crates.stacks)
        crates.do_moves()
        debug(crates.stacks)

        answer = crates.top()
        return answer

    def solve2(self) -> str:
        crates = Crates(self.data[0], self.data[1])
        debug(crates.stacks)
        crates.do_moves_p2()
        debug(crates.stacks)

        answer = crates.top()
        return answer


class Crates:
    @dataclass
    class Move:
        MOVE_REGEX = re.compile(
            r'^move (?P<num>\d+) from (?P<src>\d+) to (?P<dest>\d+)$'
        )

        num: int
        src: int
        dest: int

        @classmethod
        def from_raw(cls, raw_move):
            m = cls.MOVE_REGEX.match(raw_move)
            keys = ['num', 'src', 'dest']
            kwargs = {key: int(m.group(key)) for key in keys}
            move = cls(**kwargs)
            return move

        def __str__(self):
            return f'move {self.num} from {self.src} to {self.dest}'

    def __init__(self, raw_stacks, raw_moves):
        self.raw_stacks = raw_stacks[::-1]
        self.moves = [
            self.__class__.Move.from_raw(raw_move) for raw_move in raw_moves
        ]
        self.columns = list(map(int, self.raw_stacks[0].split()))

        self.stacks = [[] for i in self.columns]

        for row in self.raw_stacks[1:]:
            for i, column in enumerate(self.columns):
                value = self.get_raw_cell_value(i, row)
                if value is not None:
                    self.stacks[i].append(value)

    def get_raw_cell_value(self, i, row):
        """Representation:

            [D]
        [N] [C]
        [Z] [M] [P] [.] [.]
        0123456789012345678
         1   2   3
        """
        index = 1 + 4 * i
        try:
            value = row[index].strip() or None
        except IndexError:
            value = None
        return value

    def do_moves(self):
        for move in self.moves:
            for i in range(move.num):
                item = self.stacks[move.src - 1].pop()
                self.stacks[move.dest - 1].append(item)

    def do_moves_p2(self):
        for move in self.moves:
            debug(str(move))
            items = self.stacks[move.src - 1][-move.num :]
            debug(items)
            self.stacks[move.src - 1] = self.stacks[move.src - 1][: -move.num]
            self.stacks[move.dest - 1].extend(items)

            debug(self.stacks)

    def top(self):
        v = [stack[-1] for stack in self.stacks]
        result = ''.join(v)
        return result


if __name__ == '__main__':
    main()
