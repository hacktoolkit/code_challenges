from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '05'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (6113, 20373, )
TEST_EXPECTED_ANSWERS = (5, 12, )


def main():
    input_config = InputConfig(
        as_integers=False,
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

        # test
        v = VentLine('1,1 -> 3,3', diagonals=True)
        print(v)
        v2 = VentLine('9,7 -> 7,9', diagonals=True)
        print(v2)

    def solve1(self):
        h = HydrothermalVents(self.data)

        print(h)

        answer = h.num_points_at_least_2
        return answer

    def solve2(self):
        h = HydrothermalVents(self.data, diagonals=True)

        print(h)

        answer = h.num_points_at_least_2
        return answer


class HydrothermalVents:
    def __init__(self, raw_vent_lines, diagonals=False):
        self.diagonals = diagonals

        self.vent_lines = [
            VentLine(raw_vent_line, diagonals=diagonals)
            for raw_vent_line
            in raw_vent_lines
        ]

        max_size = 0
        for vent in self.vent_lines:
            max_size = max(
                max_size,
                vent.point1.x,
                vent.point1.y,
                vent.point2.x,
                vent.point2.y
            )
        self.grid_size = max_size + 1

        grid = [
            [0 for j in range(self.grid_size)]
            for i in range(self.grid_size)
        ]
        self.grid = grid


        self._fill_grid()

    def __str__(self):
        buf = []
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                val = self.grid[i][j]
                str_val = str(val) if val > 0 else '.'
                buf.append(str_val)
            buf.append('\n')

        s = ''.join(buf)
        return s

    def _fill_grid(self):
        for vent_line in self.vent_lines:
            for point in vent_line.points:
                self.grid[point.x][point.y] += 1

    @property
    def num_points_at_least_2(self):
        count = 0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] >= 2:
                    count += 1
        return count


class VentLine:
    def __init__(self, raw, diagonals=False):
        self.diagonals = diagonals
        self.point1, self.point2 = [
            Point(*[int(x) for x in raw_point.split(',')])
            for raw_point
            in raw.split(' -> ')
        ]

    def __str__(self):
        buf = []
        for point in self.points:
            buf.append(str(point))
        s = ', '.join(buf)
        return s

    @property
    def is_horizontal(self):
        return self.point1.x == self.point2.x

    @property
    def is_vertical(self):
        return self.point1.y == self.point2.y

    @property
    def points(self):
        points = []
        if self.is_horizontal:
            a, b = sorted([self.point1, self.point2], key=lambda point: point.y)
            for j in range(a.y, b.y + 1):
                points.append(Point(self.point1.x, j))
        elif self.is_vertical:
            a, b = sorted([self.point1, self.point2], key=lambda point: point.x)
            for i in range(a.x, b.x + 1):
                points.append(Point(i, self.point1.y))
        elif self.diagonals:
            x1, y1 = self.point1.x, self.point1.y
            x2, y2 = self.point2.x, self.point2.y

            x_step = 1 if x2 > x1 else -1
            y_step = 1 if y2 > y1 else -1

            cur_x = x1
            cur_y = y1

            while (
                (x_step == 1 and cur_x <= x2)
                or (x_step == -1 and cur_x >= x2)
            ):
                points.append(Point(cur_x, cur_y))
                cur_x += x_step
                cur_y += y_step

        return points


class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f'({self.x},{self.y})'


if __name__ == '__main__':
    main()
