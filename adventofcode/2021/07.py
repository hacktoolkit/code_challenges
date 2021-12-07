# Python Standard Library Imports
from collections import defaultdict

from utils import (
    BaseSolution,
    InputConfig,
    gauss_sum,
)


PROBLEM_NUM = '07'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (343468, 96086265, )
TEST_EXPECTED_ANSWERS = (37, 168, )


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=True,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=False,
        cell_func=None
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
        positions = self.data

        solutions = defaultdict(int)
        for i in range(len(positions)):
            for position in positions:
                solutions[i] += abs(position - i)

        answer = min(solutions.values())
        return answer

    def solve2(self):
        positions = self.data

        solutions = defaultdict(int)
        for i in range(len(positions)):
            for position in positions:
                steps = abs(position - i)
                # solutions[i] += sum([x for x in range(1, steps + 1)])
                solutions[i] += int(gauss_sum(1, steps))

        answer = min(solutions.values())
        return answer


if __name__ == '__main__':
    main()
