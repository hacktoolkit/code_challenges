# Python Standard Library Imports
import operator
import re
import typing as T
from dataclasses import dataclass

# Third Party (PyPI) Imports
from htk import fdb  # noqa: F401

from utils import debug  # noqa: F401
from utils import (
    BaseSolution,
    config,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (187825547, 85508223)
config.TEST_CASES = {
    '': (161, 161),
    'b': (161, 48),
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


@dataclass
class Switch:
    is_on: bool = True

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False


@dataclass
class Instruction:
    do_or_dont: str
    op: str
    a: T.Optional[int] = None
    b: T.Optional[int] = None

    @classmethod
    def from_match(cls, match):
        do_or_dont = match.group('do_or_dont')
        op = match.group('op')
        a = int(match.group('a') or 0)
        b = int(match.group('b') or 0)

        instruction = cls(do_or_dont=do_or_dont, op=op, a=a, b=b)

        # fdb(f'{instruction}: {instruction.value}')
        return instruction

    def __repr__(self):
        return f'{self.op}({self.a},{self.b})'

    @property
    def value(self):
        if self.op == 'mul':
            result = getattr(operator, self.op)(self.a, self.b)
        else:
            result = 0
        return result


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = ''.join(self.data)

        pattern = re.compile(
            r'(?P<do_or_dont>do(n\'t)?\(\))|(?P<op>mul)\((?P<a>\d+),(?P<b>\d+)\)'  # noqa: E501
        )

        self.instructions = [
            Instruction.from_match(_) for _ in re.finditer(pattern, data)
        ]

    def solve1(self) -> T.Optional[int]:
        total = 0
        for instruction in self.instructions:
            total += instruction.value

        answer = total
        return answer

    def solve2(self) -> T.Optional[int]:
        switch = Switch()
        switch.turn_on()
        total = 0
        for instruction in self.instructions:
            if instruction.do_or_dont == 'do()':
                switch.turn_on()
            elif instruction.do_or_dont == "don't()":
                switch.turn_off()
            elif switch.is_on and instruction.op == 'mul':
                total += instruction.value
            else:
                # do nothing
                pass

        answer = total

        return answer


if __name__ == '__main__':
    main()
