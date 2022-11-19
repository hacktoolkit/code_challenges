# Python Standard Library Imports
import copy
import math
import re
from collections import defaultdict

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '06'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (
    5042,
    1086,
)
TEST_EXPECTED_ANSWERS = (
    5,
    4,
)


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=False,
        row_func=None,
        cell_func=None,
    )

    if TEST_MODE:
        input_filename = f'{PROBLEM_NUM}.test.in'
        expected_answers = TEST_EXPECTED_ANSWERS
    else:
        input_filename = f'{PROBLEM_NUM}.in'
        expected_answers = EXPECTED_ANSWERS

    solution = Solution(input_filename, input_config, expected_answers)

    solution.solve()
    solution.report()


class Solution(BaseSolution):
    def process_data(self):
        data = self.data[0]
        self.numbers = [int(n) for n in re.split(r'\s', data)]

    def solve1(self):
        memory = Memory(self.numbers)
        cycles, loop_size = memory.reallocate()
        self.loop_size = loop_size

        answer = cycles
        return answer

    def solve2(self):
        answer = self.loop_size
        return answer


class Memory:
    def __init__(self, banks):
        self.banks = copy.copy(banks)

    def reallocate(self):
        seen = {}
        detected_cycle = False
        cycles = 0
        loop_size = None

        while not detected_cycle:
            snapshot = tuple(self.banks)
            if snapshot in seen:
                detected_cycle = True
                loop_size = cycles - seen[snapshot]
            else:
                seen[snapshot] = cycles
                self.reallocate_step()
                cycles += 1

        return cycles, loop_size

    def reallocate_step(self):
        max_so_far = None
        max_index = None

        # find the memory block with the largest value to reallocate
        for i, value in enumerate(self.banks):
            if max_so_far is None or value > max_so_far:
                max_so_far = value
                max_index = i
            else:
                pass

        # determine reallocation scheme
        value = self.banks[max_index]
        target_redistribution_amount = math.ceil(value / len(self.banks))

        # reallocate
        self.banks[max_index] = 0
        for offset in range(1, len(self.banks) + 1):
            index = (max_index + offset) % len(self.banks)

            redistribution_amount = min(target_redistribution_amount, value)
            self.banks[index] += redistribution_amount
            value -= redistribution_amount
            if value == 0:
                break


if __name__ == '__main__':
    main()
