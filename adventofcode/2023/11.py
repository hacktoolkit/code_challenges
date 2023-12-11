# Python Standard Library Imports
from itertools import combinations

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (9418609, 593821230983)
config.TEST_CASES = {
    # '': (374, 1030),  # Expansion factor of 2; 10
    # '': (374, 8410),  # Expansion factor of 2; 100
    '': (374, 82000210),  # Expansion factor of 1M
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        self.cosmos = Cosmos(self.data)
        print(self.cosmos.pretty_unexpanded)

    def solve1(self):
        expansion_factor = 2
        answer = self.cosmos.sum_shortest_distances(
            expansion_factor=expansion_factor
        )
        return answer

    def solve2(self):
        # expansion_factor = 10
        # expansion_factor = 100
        expansion_factor = 10**6
        answer = self.cosmos.sum_shortest_distances(
            expansion_factor=expansion_factor
        )
        return answer


class Cosmos:
    def __init__(self, raw_data):
        self.unexpanded_cosmos: set = set()
        self.M = len(raw_data)
        self.N = len(raw_data[0])

        self.empty_rows = []
        self.empty_cols = []

        # ingest data into `unexpanded_cosmos: set` data structure
        # also check for empty rows
        for m in range(self.M):
            row_is_empty = True

            for n in range(self.N):
                value = raw_data[m][n]
                if value == '#':
                    row_is_empty = False
                    self.unexpanded_cosmos.add((m, n))

            if row_is_empty:
                self.empty_rows.append(m)

        # check for empty cols
        for n in range(self.N):
            col_is_empty = True

            for m in range(self.M):
                if (m, n) in self.unexpanded_cosmos:
                    col_is_empty = False
                    break

            if col_is_empty:
                self.empty_cols.append(n)

    def pretty_cosmos(self, cosmos, num_rows, num_cols):
        s = (
            '\n'.join(
                [
                    ''.join(
                        [
                            '#' if (m, n) in cosmos else '.'
                            for n in range(num_cols)
                        ]
                    )
                    for m in range(num_rows)
                ]
            )
            + '\n'
        )
        return s

    @property
    def pretty_unexpanded(self):
        return self.pretty_cosmos(self.unexpanded_cosmos, self.M, self.N)

    @property
    def pretty_expanded(self):
        return self.pretty_cosmos(self.expanded_cosmos, self.MM, self.NN)

    def expand_cosmos(self, expansion_factor=1):
        """Builds the data structure for the expanded cosmos"""

        self.expanded_cosmos: set = set()
        self.MM = self.M + len(self.empty_rows)
        self.NN = self.N + len(self.empty_cols)

        for galaxy in self.unexpanded_cosmos:
            (m, n) = galaxy
            mm = m + self.num_empty_rows_before(m) * (expansion_factor - 1)
            nn = n + self.num_empty_cols_before(n) * (expansion_factor - 1)

            self.expanded_cosmos.add((mm, nn))

    def num_empty_rows_before(self, m):
        num = len([row for row in self.empty_rows if row < m])
        return num

    def num_empty_cols_before(self, n):
        num = len([col for col in self.empty_cols if col < n])
        return num

    def manhattan_distance(self, g1, g2):
        m1, n1 = g1
        m2, n2 = g2
        dist = abs(m2 - m1) + abs(n2 - n1)
        return dist

    def sum_shortest_distances(self, expansion_factor=1):
        self.expand_cosmos(expansion_factor=expansion_factor)

        total_distance = 0
        for (g1, g2) in combinations(self.expanded_cosmos, 2):
            dist = self.manhattan_distance(g1, g2)
            total_distance += dist

        return total_distance


if __name__ == '__main__':
    main()
