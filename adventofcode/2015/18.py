from utils import ingest


STEPS = 100
INPUT_FILE = '18.in'
EXPECTED_ANSWERS = (821, 886, )

# STEPS = 5
# INPUT_FILE = '18.test.in'
# EXPECTED_ANSWERS = (5, 17, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        data = ingest(INPUT_FILE)
        self.data = data

    def solve1(self):
        board = Board(self.data)
        print(board.pretty())

        for i in range(STEPS):
            board.tick()
            print(board.pretty())

        answer = board.num_on

        self.answer1 = answer
        return answer

    def solve2(self):
        board = Board(self.data, corners_stuck=True)
        print(board.pretty())

        for i in range(STEPS):
            board.tick()
            print(board.pretty())

        answer = board.num_on

        self.answer2 = answer
        return answer


class Board:
    SENTINEL_OFF_ON = '@'
    SENTINEL_ON_OFF = '%'

    OFF_SYMBOLS = ['.', '@', ]
    ON_SYMBOLS = ['#', '%', ]

    def __init__(self, data, corners_stuck=False):
        board = [
            [slot for slot in row]
            for row in data
        ]
        self.board = board

        M, N = (len(board), len(board[0]), )
        self.M, self.N = (M, N, )

        # check all rows have the same length
        assert(len(set([len(row) for row in board]) ) == 1)

        self.corners_stuck = corners_stuck
        if corners_stuck:
            self.corner_positions = [
                (0, 0, ),
                (0, N - 1, ),
                (M - 1, 0, ),
                (M -1, N - 1, ),
            ]
            for a, b in self.corner_positions:
                board[a][b] = '#'

    @property
    def num_on(self):
        count = 0
        for m in range(self.M):
            for n in range(self.N):
                if self.board[m][n] == '#':
                    count += 1
        return count

    def tick(self):
        """Performs 1 tick in this adapted Game of Life

        https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
        """
        did_change = False

        for m in range(self.M):
            for n in range(self.N):
                if self.corners_stuck and (m, n, ) in self.corner_positions:
                    continue

                status = self.board[m][n]
                is_on = status in self.ON_SYMBOLS

                neighbors = self.neighbors(m, n)
                num_off_neighbors = sum([
                    1 if neighbor in self.OFF_SYMBOLS else 0
                    for neighbor
                    in neighbors
                ])
                num_on_neighbors = sum([
                    1 if neighbor in self.ON_SYMBOLS else 0
                    for neighbor
                    in neighbors
                ])

                if is_on:
                    next_status = self.SENTINEL_ON_OFF if num_on_neighbors not in (2, 3) else status
                else:
                    next_status = self.SENTINEL_OFF_ON if num_on_neighbors == 3 else status

                if status != next_status:
                    self.board[m][n] = next_status
                    did_change = True

        # replace sentinel values with actual
        for m in range(self.M):
            for n in range(self.N):
                status = self.board[m][n]
                if status == self.SENTINEL_OFF_ON:
                    self.board[m][n] = self.ON_SYMBOLS[0]
                elif status == self.SENTINEL_ON_OFF:
                    self.board[m][n] = self.OFF_SYMBOLS[0]
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
                neighbor = self.board[i][j]
                neighbors.append(neighbor)

        return neighbors

    def pretty(self):
        pretty = '{}\n'.format(
            '\n'.join([''.join(row) for row in self.board])
        )
        return pretty


if __name__ == '__main__':
    main()
