# Third Party (PyPI) Imports
from utils import (
    BaseSolution,
    InputConfig,
    ingest,
)


PROBLEM_NUM = '01'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (1521, 1543, )
TEST_EXPECTED_ANSWERS = (7, 5, )


def main():
    input_config = InputConfig(
        as_integers=True,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=False,
        row_func=None,
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
        # data = self.data
        pass

    def solve1(self):
        num_increases = 0
        prev_value = None

        for value in self.data:
            if prev_value is None:
                pass
            elif value > prev_value:
                num_increases += 1
            else:
                pass

            prev_value = value

        answer = num_increases
        return answer

    def solve2(self):
        window_size = 3
        num_increases = 0
        prev_subtotal = None

        for i in range(len(self.data) - window_size + 1):
            values = self.data[i:i + window_size]
            subtotal = sum(values)
            # print(values, subtotal)

            if prev_subtotal is None:
                pass
            elif subtotal > prev_subtotal:
                num_increases += 1
            else:
                pass

            prev_subtotal = subtotal

        answer = num_increases
        return answer


if __name__ == '__main__':
    main()
