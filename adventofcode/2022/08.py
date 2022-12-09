# Python Standard Library Imports
import math
import typing as T
from collections import defaultdict
from enum import (
    Enum,
    auto,
)

from utils import (
    RE,
    BaseSolution,
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

    def solve1(self) -> int:
        num_visible = 0
        for i in range(self.M):
            for j in range(self.N):
                if self.is_visible(i, j):
                    num_visible += 1

        answer = num_visible
        return answer

    def solve2(self) -> int:
        best_scenic_score = None
        for i in range(self.M):
            for j in range(self.N):
                visible_trees = [
                    self.trees_visible[(i, j, direction)]
                    for direction in Direction
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

    def is_visible(self, i: int, j: int) -> bool:
        is_visible = any(
            [
                self.is_visible_from_direction(i, j, direction)
                for direction in Direction
            ]
        )
        return is_visible

    def is_visible_from_direction(
        self,
        i: int,
        j: int,
        direction: 'Direction',
    ) -> bool:
        h = self.trees[i][j]
        is_visible = True
        for m, n in direction.coords(i, j, self.M, self.N)():
            h2 = self.trees[m][n]
            self.trees_visible[(i, j, direction)] += 1
            if h2 >= h:
                is_visible = False
                break

        return is_visible


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

    def coords(self, i: int, j: int, M: int, N: int):
        mapping = {
            Direction.UP: lambda: ((m, j) for m in range(i - 1, -1, -1)),
            Direction.DOWN: lambda: ((m, j) for m in range(i + 1, M)),
            Direction.LEFT: lambda: ((i, n) for n in range(j - 1, -1, -1)),
            Direction.RIGHT: lambda: ((i, n) for n in range(j + 1, N)),
        }
        return mapping[self]


if __name__ == '__main__':
    main()
