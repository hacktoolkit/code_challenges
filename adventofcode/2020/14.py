# Python Standard Library Imports
import re

from utils import (
    Re,
    ingest,
)


INPUT_FILE = '14.in'
EXPECTED_ANSWERS = (None, None, )

# INPUT_FILE = '14.test.in'
# EXPECTED_ANSWERS = (165, None, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        data = ingest(INPUT_FILE)
        self.instructions = [Instruction(raw_instruction) for raw_instruction in data]

    def solve1(self):
        program = Program()
        program.run(self.instructions)

        answer = program.total

        self.answer1 = answer
        return answer

    def solve2(self):
        answer = None

        self.answer2 = answer
        return answer


class Program:
    def __init__(self):
        self.memory = {}

    @property
    def total(self):
        return sum(self.memory.values())

    def run(self, instructions):
        on_mask = None
        off_mask = None

        for instruction in instructions:
            if instruction.is_mask:
                on_mask = instruction.on_mask
                off_mask = instruction.off_mask
            else:
                address = instruction.address
                value = instruction.value
                if on_mask:
                    value = value | on_mask
                if off_mask:
                    value = value & off_mask

                self.memory[address] = value


class Instruction:
    BITMASK_REGEX = re.compile(r'^mask = (?P<mask>[X10]{36})$')
    MEMSET_REGEX = re.compile(r'^mem\[(?P<address>\d+)\] = (?P<value>\d+)$')

    def __init__(self, raw_instruction):
        self.is_mask = False

        regex = Re()
        if regex.match(Instruction.BITMASK_REGEX, raw_instruction):
            m = regex.last_match
            mask = m.group('mask')

            self.is_mask = True
            self.on_mask = int(mask.replace('X', '0'), 2)
            self.off_mask = int(mask.replace('X', '1'), 2)
        elif regex.match(Instruction.MEMSET_REGEX, raw_instruction):
            m = regex.last_match
            self.address, self.value = (
                int(m.group('address')),
                int(m.group('value')),
            )
        else:
            raise Exception('Bad instruction: %s' % raw_instruction)


if __name__ == '__main__':
    main()
