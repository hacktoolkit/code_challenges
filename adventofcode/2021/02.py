# Third Party (PyPI) Imports
from utils import (
    BaseSolution,
    InputConfig,
    ingest,
)


EXPECTED_ANSWERS = (None, None, )
TEST_EXPECTED_ANSWERS = (None, None, )


def main():
    input_config = InputConfig(
        as_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=False,
        cell_func=None
    )

    #solution = Solution('02.in', input_config, EXPECTED_ANSWERS)
    solution = Solution('02.test.in', input_config, TEST_EXPECTED_ANSWERS)

    solution.solve()
    solution.report()


class Solution(BaseSolution):
    def process_data(self):
        # data = self.data
        pass

    def solve1(self):
        #
        # TODO: FILL THIS IN
        #
        answer = None
        return answer

    def solve2(self):
        #
        # TODO: FILL THIS IN
        #
        answer = None
        return answer


if __name__ == '__main__':
    main()
