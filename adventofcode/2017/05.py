# Python Standard Library Imports
import copy
from collections import defaultdict

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '05'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (
    360603,
    25347697,
)
TEST_EXPECTED_ANSWERS = (
    5,
    10,
)


def main():
    input_config = InputConfig(
        as_integers=True,
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
        data = self.data

    def solve1(self):
        jumpers = Jumpers(self.data)
        jumpers.run()
        answer = jumpers.steps
        return answer

    def solve2(self):
        jumpers = Jumpers(self.data)
        jumpers.run(is_part_2=True)
        answer = jumpers.steps
        return answer


class Jumpers:
    def __init__(self, jump_offsets):
        self.jump_offsets = copy.copy(jump_offsets)

        self.steps = 0
        self.index = 0

    def run(self, is_part_2=False):
        while 0 <= self.index < len(self.jump_offsets):
            jump_offset = self.jump_offsets[self.index]
            next_index = self.index + jump_offset

            if is_part_2:
                shift = -1 if jump_offset >= 3 else 1
            else:
                shift = 1

            self.jump_offsets[self.index] += shift

            # updates
            self.index = next_index
            self.steps += 1


if __name__ == '__main__':
    main()
