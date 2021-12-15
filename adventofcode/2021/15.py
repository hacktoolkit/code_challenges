# Python Standard Library Imports
import copy
import heapq

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '15'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (415, 2864, )
TEST_EXPECTED_ANSWERS = (40, 315, )


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=True,
        row_func=lambda row: row[0],
        cell_func=lambda line: [int(d) for d in line]
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

        self.matrix = data
        self.matrix2 = self.build_tiled_matrix(data, 5)

    def build_tiled_matrix(self, matrix, n):
        # tile horizontally first
        horizontal = [
            [
                (v + k - 1) % 9 + 1
                for k in range(n)
                for v in row
            ]
            for row in matrix
        ]

        # tile vertically
        vertical = [
            [(v + k - 1) % 9 + 1 for v in row]
            for k in range(n)
            for row in horizontal
        ]

        return vertical

    def solve1(self):
        answer = self.shortest_path(self.matrix)
        return answer

    def solve2(self):
        answer = self.shortest_path(self.matrix2)
        return answer

    def shortest_path(self, matrix):
        """Calculates the shortest path to traverse matrix

        Starting from `(0, 0)`
        Ending at `(m, n)`

        Where:
        - `m = self.M - 1`
        - `n = self.N - 1`

        References:
        - https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Using_a_priority_queue
        - https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
        """
        M = len(matrix)
        N = len(matrix[0])

        INF = 10**9
        best_distances = [[INF] * N for _ in range(M)]

        pq = [(0, 0, 0, )]
        while pq:
            dist, i, j = heapq.heappop(pq)

            shifts = [
                (i - 1, j),  # above
                (i + 1, j),  # below
                (i, j - 1),  # left
                (i, j + 1),  # right
            ]

            for a, b in shifts:
                # only check valid neighbors
                if 0 <= a < M and 0 <= b < N:
                    alt_dist = dist + matrix[a][b]
                    if alt_dist < best_distances[a][b]:
                        # add to priority queue if `alt_dist` is better
                        best_distances[a][b] = alt_dist
                        heapq.heappush(pq, (alt_dist, a, b))

        shortest_path = best_distances[-1][-1]
        return shortest_path


if __name__ == '__main__':
    main()
