# Python Standard Library Imports
import re
from collections import defaultdict

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '22'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (610196, None, )

# TEST_VARIANT = 'a'
# TEST_EXPECTED_ANSWERS = (39, None, )

# TEST_VARIANT = 'b'
# TEST_EXPECTED_ANSWERS = (590784, None, )

TEST_VARIANT = 'c'
TEST_EXPECTED_ANSWERS = (474140, 2758514936282235, )


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=False,
        row_func=None,
        cell_func=None
    )

    if TEST_MODE:
        input_filename = f'{PROBLEM_NUM}{TEST_VARIANT}.test.in'
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
        self.instructions = [Instruction(i) for i in data]

    def solve1(self):
        cubes_on = set()

        instructions = self.instructions

        for instruction in instructions:
            for coord in instruction.get_init_coords():
                if Instruction.in_initialization_region(*coord):
                    if instruction.on:
                        cubes_on.add(coord)
                    elif coord in cubes_on:
                        cubes_on.remove(coord)
                    else:
                        # do nothing
                        pass
                else:
                    # do nothing
                    pass

        answer = len(cubes_on)
        return answer

    def solve2(self):
        cubes_on = set()

        instructions = self.instructions

        for instruction in instructions:
            for coord in instruction.get_coords():
                if instruction.on:
                    cubes_on.add(coord)
                elif coord in cubes_on:
                    cubes_on.remove(coord)
                else:
                    # do nothing
                    pass

        answer = len(cubes_on)
        return answer


class Instruction:
    REGEX = re.compile(r'(?P<on_or_off>on|off) x=(?P<x1>-?\d+)\.\.(?P<x2>-?\d+),y=(?P<y1>-?\d+)\.\.(?P<y2>-?\d+),z=(?P<z1>-?\d+)\.\.(?P<z2>-?\d+)')
    INIT_RANGE_LOWER = -50
    INIT_RANGE_UPPER = 50

    def __init__(self, raw_instruction):
        m = Instruction.REGEX.match(raw_instruction)
        if m:
            (
                self.on_or_off,
                self.x1,
                self.x2,
                self.y1,
                self.y2,
                self.z1,
                self.z2,
            ) = (
                m.group('on_or_off'),
                int(m.group('x1')),
                int(m.group('x2')),
                int(m.group('y1')),
                int(m.group('y2')),
                int(m.group('z1')),
                int(m.group('z2')),
            )
            self.on = self.on_or_off == 'on'
        else:
            raise Exception('Illegal format')

    @classmethod
    def in_initialization_region(cls, x, y, z):
        in_initialization_region = (
            Instruction.INIT_RANGE_LOWER <= x <= Instruction.INIT_RANGE_UPPER
            and Instruction.INIT_RANGE_LOWER <= y <= Instruction.INIT_RANGE_UPPER
            and Instruction.INIT_RANGE_LOWER <= z <= Instruction.INIT_RANGE_UPPER
        )
        return in_initialization_region

    def get_init_xrange(self):
        x1 = max(Instruction.INIT_RANGE_LOWER, self.x1)
        x2 = min(Instruction.INIT_RANGE_UPPER, self.x2)
        for x in range(x1, x2 + 1):
            yield x

    def get_init_yrange(self):
        y1 = max(Instruction.INIT_RANGE_LOWER, self.y1)
        y2 = min(Instruction.INIT_RANGE_UPPER, self.y2)
        for y in range(y1, y2 + 1):
            yield y

    def get_init_zrange(self):
        z1 = max(Instruction.INIT_RANGE_LOWER, self.z1)
        z2 = min(Instruction.INIT_RANGE_UPPER, self.z2)
        for z in range(z1, z2 + 1):
            yield z

    def get_init_coords(self):
        for x in self.get_init_xrange():
            for y in self.get_init_yrange():
                for z in self.get_init_zrange():
                    yield (x, y, z)

    def get_xrange(self):
        for x in range(self.x1, self.x2 + 1):
            yield x

    def get_yrange(self):
        for y in range(self.y1, self.y2 + 1):
            yield y

    def get_zrange(self):
        for z in range(self.z1, self.z2 + 1):
            yield z

    def get_coords(self):
        for x in self.get_xrange():
            for y in self.get_yrange():
                for z in self.get_zrange():
                    yield (x, y, z)


if __name__ == '__main__':
    main()
