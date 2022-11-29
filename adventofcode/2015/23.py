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


PROBLEM_NUM = '23'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (184, 231)
TEST_VARIANT = ''  # '', 'b', 'c', 'd', ...
TEST_EXPECTED_ANSWERS = {
    '': (0, 0),
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
    def process_data(self):
        data = self.data
        self.instructions = [Instruction.from_raw(_) for _ in data]

    def solve1(self):
        computer = Computer(self.instructions)
        computer.run()
        debug(str(computer))

        answer = computer.reg_b
        return answer

    def solve2(self):
        computer = Computer(self.instructions)
        computer.reg_a = 1
        computer.run()
        debug(str(computer))

        answer = computer.reg_b
        return answer


class Computer:
    def __init__(self, instructions):
        self.reg_a = 0
        self.reg_b = 0

        self.step = 0

        self.instructions = instructions

    def __str__(self):
        return (
            f'step: {str(self.step).zfill(2)}, a: {self.reg_a}, b: {self.reg_b}'
        )

    def run(self):
        self.step = 0

        while self.step < len(self.instructions):
            debug(str(self))
            instruction = self.instructions[self.step]
            self.perform_instruction(instruction)
            debug('-----')

    def register_value(self, register):
        value = getattr(self, f'reg_{register}')
        return value

    def set_register_value(self, register, value):
        setattr(self, f'reg_{register}', value)

    def perform_instruction(self, instruction):
        debug(instruction.raw)
        f = getattr(self, f'_perform_instruction__{instruction.name}')
        f(instruction)

    def _perform_instruction__hlf(self, instruction):
        self.set_register_value(
            instruction.register, self.register_value(instruction.register) // 2
        )
        self.step += 1

    def _perform_instruction__tpl(self, instruction):
        self.set_register_value(
            instruction.register, self.register_value(instruction.register) * 3
        )
        self.step += 1

    def _perform_instruction__inc(self, instruction):
        self.set_register_value(
            instruction.register, self.register_value(instruction.register) + 1
        )
        self.step += 1

    def _perform_instruction__jmp(self, instruction):
        self.step += instruction.jump_offset

    def _perform_instruction__jie(self, instruction):
        if self.register_value(instruction.register) % 2 == 0:
            self.step += instruction.jump_offset
        else:
            self.step += 1

    def _perform_instruction__jio(self, instruction):
        if self.register_value(instruction.register) == 1:
            self.step += instruction.jump_offset
        else:
            self.step += 1


@dataclass
class Instruction:
    raw: str
    name: str
    register: T.Optional[str] = None
    jump_offset: T.Optional[int] = None

    @classmethod
    def from_raw(cls, raw):
        parts = [part.strip() for part in raw.split(',')]
        if len(parts) == 1:
            name, register = parts[0].split()
            if name == 'jmp':
                jump_offset = int(register)
                register = None
            else:
                jump_offset = None
        elif len(parts) == 2:
            name, register = parts[0].split()
            jump_offset = int(parts[1])
        else:
            raise Exception(f'Too many data: {data}')

        instruction = cls(
            raw=raw, name=name, register=register, jump_offset=jump_offset
        )
        return instruction


if __name__ == '__main__':
    main()
