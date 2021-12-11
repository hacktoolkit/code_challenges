from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '11'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (1683, 788, )
TEST_EXPECTED_ANSWERS = (1656, 195, )


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=True,
        row_func=lambda row: row[0],
        cell_func=lambda cell: [int(d) for d in str(cell)]
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
        self.octopi = Octopi(data)

    def solve1(self):
        o = self.octopi

        for i in range(100):
            o.tick()

        answer = o.total_num_flashes
        return answer

    def solve2(self):
        o = self.octopi

        while True:
            o.tick()
            if o.current_num_flashes == o.count:
                break

        answer = o.num_steps
        return answer


class Octopi:
    def __init__(self, table):
        self.table = table
        self.num_rows = len(table)
        self.num_cols = len(table[0])

        self.count = self.num_rows * self.num_cols

        self.current_num_flashes = 0
        self.total_num_flashes = 0
        self.num_steps = 0

    def __str__(self):
        buf = []
        for row in self.table:
            buf.append(''.join([str(d) for d in row]))
            buf.append('\n')
        s = ''.join(buf)
        return s

    def tick(self):
        table = self.table

        # reset flashed map each tick
        self.flashed = set()

        for x in range(self.num_rows):
            for y in range(self.num_cols):
                table[x][y] += 1

        for x in range(self.num_rows):
            for y in range(self.num_cols):
                if table[x][y] > 9:
                    self.flash(x, y)

        for x in range(self.num_rows):
            for y in range(self.num_cols):
                if table[x][y] > 9:
                    table[x][y] = 0

        num_flashes = len(self.flashed)
        self.current_num_flashes = num_flashes
        self.total_num_flashes += num_flashes
        self.num_steps += 1

    def flash(self, x, y):
        table = self.table

        coord = (x,y)
        if coord in self.flashed:
            pass
        else:
            self.flashed.add(coord)
            neighbors = self.get_neighbors(x, y)
            for a, b in neighbors:
                table[a][b] += 1
                if table[a][b] > 9:
                    self.flash(a, b)

    def get_neighbors(self, x, y):
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
        cells = []
        for dx, dy in shifts:
            a = x + dx
            b = y + dy

            coord = (a, b)

            if 0 <= a < self.num_rows and 0 <= b < self.num_cols:
                cells.append(coord)

        return cells


if __name__ == '__main__':
    main()
