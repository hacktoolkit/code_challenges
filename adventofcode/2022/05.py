# Python Standard Library Imports
import re
import typing as T
from collections import defaultdict
from dataclasses import dataclass

from utils import (
    BaseSolution,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = ('LJSVLTWQM', 'BRQWDBBJM')
config.TEST_CASES = {
    '': ('CMZ', 'MCD'),
}

config.INPUT_CONFIG.as_integers = False
config.INPUT_CONFIG.as_comma_separated_integers = False
config.INPUT_CONFIG.as_json = False
config.INPUT_CONFIG.as_groups = True
config.INPUT_CONFIG.strip_lines = False
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
