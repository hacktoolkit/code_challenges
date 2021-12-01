# Third Party (PyPI) Imports
from utils import (
    BaseSolution,
    InputConfig,
    ingest,
)


EXPECTED_ANSWERS = (1521, 1543, )
TEST_EXPECTED_ANSWERS = (7, 5, )


def main():
    input_config = InputConfig(
        as_integers=True,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=False,
        cell_func=None
    )

    #solution = Solution('01.in', input_config, EXPECTED_ANSWERS)
    solution = Solution('01.test.in', input_config, TEST_EXPECTED_ANSWERS)

    solution.solve()
    solution.report()


class Solution(BaseSolution):
    def process_data(self):
        # data = self.data
        pass

    def solve1(self):
        answer = None

        num_increases = 0
        prev_value = None

        for value in self.data:
            if prev_value is None:
                pass
            else:
                if value > prev_value:
                    num_increases += 1
            prev_value = value

        answer = num_increases

        self.answer1 = answer
        return answer

    def solve2(self):
        answer = None

        window_size = 3
        num_increases = 0
        prev_subtotal = None

        for i in range(len(self.data) - window_size + 1):
            values = self.data[i:i + window_size]
            subtotal = sum(values)
            print(values, subtotal)


            if prev_subtotal is None:
                pass
            elif subtotal > prev_subtotal:
                num_increases += 1
            else:
                pass

            prev_subtotal = subtotal

        answer = num_increases

        self.answer2 = answer
        return answer


if __name__ == '__main__':
    main()
