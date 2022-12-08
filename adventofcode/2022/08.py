# Python Standard Library Imports
import math
from collections import defaultdict

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (1792, 334880)
config.TEST_CASES = {
    '': (21, 8),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        self.trees = [[int(d) for d in row] for row in data]
        self.M = len(self.trees)
        self.N = len(self.trees[0])

        self.trees_visible = defaultdict(int)

    def solve1(self):
        num_visible = 0
        for i in range(self.M):
            for j in range(self.N):
                if self.is_visible(i, j):
                    num_visible += 1

        answer = num_visible
        return answer

    def solve2(self):
        best_scenic_score = None
        for i in range(self.M):
            for j in range(self.N):
                visible_trees = [
                    self.trees_visible[(i, j, 'U')],
                    self.trees_visible[(i, j, 'L')],
                    self.trees_visible[(i, j, 'D')],
                    self.trees_visible[(i, j, 'R')],
                ]
                debug(f'visible_trees({i}, {j}): {visible_trees}')

                scenic_score = math.prod(visible_trees)
                if (
                    best_scenic_score is None
                    or scenic_score > best_scenic_score
                ):
                    best_scenic_score = scenic_score

        answer = best_scenic_score
        return answer

    def is_visible(self, i, j):
        is_visible = any(
            [
                self.is_visible_from_top(i, j),
                self.is_visible_from_left(i, j),
                self.is_visible_from_bottom(i, j),
                self.is_visible_from_right(i, j),
            ]
        )
        return is_visible

    def is_visible_from_top(self, i, j):
        h = self.trees[i][j]
        is_visible = True
        for m in range(i - 1, -1, -1):
            h2 = self.trees[m][j]
            self.trees_visible[(i, j, 'U')] += 1
            if h2 >= h:
                is_visible = False
                break

        return is_visible

    def is_visible_from_left(self, i, j):
        h = self.trees[i][j]
        is_visible = True
        for n in range(j - 1, -1, -1):
            h2 = self.trees[i][n]
            self.trees_visible[(i, j, 'L')] += 1
            if h2 >= h:
                is_visible = False
                break

        return is_visible

    def is_visible_from_bottom(self, i, j):
        h = self.trees[i][j]
        is_visible = True
        for m in range(i + 1, self.M):
            h2 = self.trees[m][j]
            self.trees_visible[(i, j, 'D')] += 1
            if h2 >= h:
                is_visible = False
                break

        return is_visible

    def is_visible_from_right(self, i, j):
        h = self.trees[i][j]
        is_visible = True
        for n in range(j + 1, self.N):
            h2 = self.trees[i][n]
            self.trees_visible[(i, j, 'R')] += 1
            if h2 >= h:
                is_visible = False
                break

        return is_visible


if __name__ == '__main__':
    main()
