from utils import ingest


INPUT_FILE = '11.in'
EXPECTED_ANSWERS = (2310, None, )

# INPUT_FILE = '11.test.in'
# EXPECTED_ANSWERS = (37, 26, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)
        self.seating_chart = SeatingChart(self.data)

    def solve1(self):
        seating_chart = self.seating_chart

        did_change = True

        while did_change:
            print(seating_chart.pretty())
            did_change = seating_chart.tick()

        answer = seating_chart.num_occupied_seats
        return answer

    def solve2(self):
        answer = None
        return answer


class SeatingChart:
    SENTINEL_EMPTY_OCCUPIED = '@'
    SENTINEL_OCCUPIED_EMPTY = '%'

    EMPTY_SYMBOLS = ['L', '@', '.', ]
    OCCUPIED_SYMBOLS = ['#', '%', ]

    SEAT_SYMBOLS = ['L', '@', '#', '%', ]

    def __init__(self, data):
        chart = [
            [seat for seat in row]
            for row in data
        ]
        self.chart = chart

        self.M = len(chart)
        self.N = len(chart[0])

        # check all rows have the same length
        assert(len(set([len(row) for row in chart]) ) == 1)


    @property
    def num_occupied_seats(self):
        count = 0
        for m in range(self.M):
            for n in range(self.N):
                if self.chart[m][n] == '#':
                    count += 1
        return count

    def tick(self):
        did_change = False

        for m in range(self.M):
            for n in range(self.N):
                status = self.chart[m][n]
                is_seat = status in self.SEAT_SYMBOLS
                is_empty = status in self.EMPTY_SYMBOLS

                neighbors = self.neighbors(m, n)
                num_empty_neighbors = sum([
                    1 if neighbor in self.EMPTY_SYMBOLS else 0
                    for neighbor
                    in neighbors
                ])
                num_occupied_neighbors = sum([
                    1 if neighbor in self.OCCUPIED_SYMBOLS else 0
                    for neighbor
                    in neighbors
                ])

                if is_seat:
                    if is_empty:
                        next_status = self.SENTINEL_EMPTY_OCCUPIED if num_occupied_neighbors == 0 else status
                    else:
                        next_status = self.SENTINEL_OCCUPIED_EMPTY if num_occupied_neighbors >= 4 else status
                else:
                    next_status = status

                if status != next_status:
                    self.chart[m][n] = next_status
                    did_change = True

        # replace sentinel values with actual
        for m in range(self.M):
            for n in range(self.N):
                status = self.chart[m][n]
                if status == self.SENTINEL_EMPTY_OCCUPIED:
                    self.chart[m][n] = self.OCCUPIED_SYMBOLS[0]
                elif status == self.SENTINEL_OCCUPIED_EMPTY:
                    self.chart[m][n] = self.EMPTY_SYMBOLS[0]
                else:
                    pass

        return did_change


    def neighbors(self, m, n):
        """Get all neighbors for cell at row m, col n
        """
        shifts = [
            (-1, -1),  # diagonally left above
            (-1, 0),  # immediately above
            (-1, 1),  # diagonally right above
            (0, -1),  # immediately left
            (0, 1),  # imediately right
            (1, -1),  # diagonally left below
            (1, 0),  # immediately below
            (1, 1),  # diagonally right below
        ]

        neighbors = []

        for a, b in shifts:
            i, j = m + a, n + b

            if 0 <= i < self.M and 0 <= j < self.N:
                neighbors.append(self.chart[i][j])

        return neighbors

    def pretty(self):
        pretty = '{}\n'.format(
            '\n'.join([''.join(row) for row in self.chart])
        )
        return pretty


if __name__ == '__main__':
    main()
