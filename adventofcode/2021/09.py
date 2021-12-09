# Python Standard Library Imports
from collections import defaultdict

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '09'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (558, 882942, )
TEST_EXPECTED_ANSWERS = (15, 1134, )


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=True,
        row_func=lambda x: x[0],
        cell_func=lambda x: [int(d) for d in str(x)]
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
        self.height_map = HeightMap(data)

    def solve1(self):
        answer = self.height_map.risk_score
        return answer

    def solve2(self):
        basins = self.height_map.basins
        basin_sizes =[len(basin) for basin in basins]
        a, b, c = sorted(basin_sizes, reverse=True)[:3]
        answer = a * b * c
        return answer


class HeightMap:
    def __init__(self, table):
        self.table = table
        self.num_rows = len(table)
        self.num_cols = len(table[0])

    def __str__(self):
        buf = []
        for x in range(self.num_rows):
            buf.append(','.join([str(_) for _ in self.table[x]]))
            buf.append('\n')

        s = ''.join(buf)
        return s

    def is_valid_coord(self, x, y):
        is_valid = (
            0 <= x < self.num_rows
            and 0 <= y < self.num_cols
        )
        return is_valid

    def neighbor_coords(self, x, y):
        neighbor_shifts = [
            (0, 1,),
            (0, -1,),
            (-1, 0,),
            (1, 0,),
        ]

        coords = []
        for (dx, dy) in neighbor_shifts:
            a, b = (x + dx, y + dy)
            if self.is_valid_coord(a, b):
                coords.append((a, b))

        return coords

    @property
    def low_points(self):
        points = []

        for x in range(self.num_rows):
            for y in range(self.num_cols):
                value = self.table[x][y]
                is_low_point = True  # innocent until proven guilty

                neighbor_coords = self.neighbor_coords(x, y)
                for (a, b) in neighbor_coords:
                    neighbor = self.table[a][b]
                    if neighbor <= value:
                        is_low_point = False
                        break

                if is_low_point:
                    points.append((x, y))

        return points

    def risk_level(self, x, y):
        return 1 + self.table[x][y]

    @property
    def risk_score(self):
        score = sum([
            self.risk_level(x, y)
            for (x, y)
            in self.low_points
        ])
        return score

    @property
    def basins(self):
        basins = [
            self.find_basin(x, y)
            for x, y
            in self.low_points
        ]
        return basins

    def find_basin(self, x, y):
        visited = {
            (x, y): True,
        }

        to_visit = self.neighbor_coords(x, y)
        while len(to_visit) > 0:
            a, b = to_visit.pop()
            value = self.table[a][b]
            if value < 9:
                visited[(a,b)] = True
                neighbor_coords = self.neighbor_coords(a, b)
                for coord in neighbor_coords:
                    if coord not in visited:
                        to_visit.append(coord)
            else:
                visited[(a,b)] = False

        basin_coords = [
            coord
            for coord, in_basin
            in visited.items()
            if in_basin
        ]
        return basin_coords


if __name__ == '__main__':
    main()
