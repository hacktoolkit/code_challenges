# Python Standard Library Imports
from collections import defaultdict
from enum import Enum

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '03'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (
    438,
    266330,
)
TEST_EXPECTED_ANSWERS = (
    31,
    None,
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
        self.n = self.data[0]

    def solve1(self):
        spiral = Spiral()
        d_layer, d_side, side = spiral.manhattan(self.n)
        answer = d_layer + abs(d_side)
        return answer

    def solve2(self):
        spiral = Spiral2()
        answer = spiral.build_grid(self.n)
        return answer


class Side(Enum):
    EAST = 1
    NORTH = 2
    WEST = 3
    SOUTH = 4


class Spiral:
    def calc_square_position(self, square_num):
        layer = 1

        while True:
            side_length = (layer - 1) * 2 + 1
            size = side_length**2
            if size >= square_num:
                break

            layer += 1

        return layer, side_length, size

    def manhattan(self, square_num):
        layer, side_length, size = self.calc_square_position(square_num)

        # calculate number of layers to traverse from outer-most layer to inner-most layer
        d_layer = layer - 1

        # calculate distance along side from square to center of a side
        c2 = size
        c1 = c2 - (side_length - 1)
        side = Side.SOUTH

        while not (c1 <= square_num <= c2):
            c2 = c1
            c1 = c2 - (side_length - 1)
            side = Side(side.value - 1)

        mid = (c2 + c1) // 2
        d_side = square_num - mid

        return d_layer, d_side, side


class Spiral2(Spiral):
    def __init__(self):
        self.square_num = 1
        self.grid = {}

    def build_grid(self, n):
        # grid coordinates represented by a Cartesian plane
        x = 0
        y = 0
        # seed value of 1 in center of grid
        value = 1

        # stop when the first value written exceeds `n`
        while value < n:
            self.grid[(x, y)] = value
            self.square_num += 1
            x, y = self.get_coords(self.square_num)
            value = self.calculate_value_at(x, y)

        return value

    def get_coords(self, square_num):
        d_layer, d_side, side = self.manhattan(square_num)

        if side == Side.EAST:
            x = d_layer
            y = d_side
        elif side == Side.WEST:
            x = -d_layer
            y = -d_side
        elif side == Side.NORTH:
            y = d_layer
            x = -d_side
        elif side == Side.SOUTH:
            y = -d_layer
            x = d_side

        return x, y

    def calculate_value_at(self, x, y):
        # the value of a cell is the sum of the value of all its neighbors
        shifts = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        neighbors = [(x + dx, y + dy) for dx, dy in shifts]
        total = sum([self.grid.get(cell, 0) for cell in neighbors])
        return total


if __name__ == '__main__':
    main()
