# Python Standard Library Imports
import copy
from collections import defaultdict

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '25'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (471, None, )
TEST_EXPECTED_ANSWERS = (58, None, )


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
        self.sea_cucumbers = SeaCucumbers(data)

    def solve1(self):
        sea_cucumbers = self.sea_cucumbers

        did_move = True
        while did_move:
            did_move = sea_cucumbers.step()

        answer = sea_cucumbers.step_count
        return answer

    def solve2(self):
        #
        # TODO: FILL THIS IN
        #
        answer = None
        return answer


class SeaCucumbers:
    def __init__(self, raw_input):
        self.grid = [
            [
                cucumber if cucumber in ['v', '>', ] else None
                for cucumber
                in row
            ]
            for row in raw_input
        ]

        self.M = len(self.grid)
        self.N = len(self.grid[0])

        self.did_move = True
        self.step_count = 0

    def __str__(self):
        buf = []
        for row in self.grid:
            buf.append(''.join([
                cucumber or '.'
                for cucumber
                in row
            ]))
            buf.append('\n')
        s = ''.join(buf)
        return s

    def step(self):
        east_did_move = self.east_facing_move()
        south_did_move = self.south_facing_move()
        did_move = east_did_move or south_did_move
        self.did_move = did_move
        self.step_count += 1

        return did_move

    def east_facing_move(self):
        did_move = False
        new_grid = copy.deepcopy(self.grid)
        for m, row in enumerate(self.grid):
            for n, cucumber in enumerate(row):
                n2 = (n + 1) % self.N
                if cucumber == '>':
                    if self.grid[m][n2] is None:
                        new_grid[m][n] = None
                        new_grid[m][n2] = cucumber
                        did_move = True
                    else:
                        pass
                else:
                    pass
        self.grid = new_grid
        return did_move

    def south_facing_move(self):
        did_move = False
        new_grid = copy.deepcopy(self.grid)
        for m, row in enumerate(self.grid):
            m2 = (m + 1) % self.M
            for n, cucumber in enumerate(row):
                if cucumber == 'v':
                    if self.grid[m2][n] is None:
                        new_grid[m][n] = None
                        new_grid[m2][n] = cucumber
                        did_move = True
                    else:
                        pass
                else:
                    pass
        self.grid = new_grid
        return did_move


if __name__ == '__main__':
    main()
