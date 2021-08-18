#!/usr/bin/env python3
"""
http://projecteuler.net/problem=083

Path sum: four ways

NOTE: This problem is a significantly more challenging version of Problem 81.
In the 5 by 5 matrix below, the minimal path sum from the top left to the bottom right, by moving left, right, up, and down, is indicated in bold red and is equal to 2297.

131 673 234 103  18
201  96 342 965 150
630 803 746 422 111
537 699 497 121 956
805 732 524  37 331

Minimal Path: 131 201 96 342 234 103 18 150 111 422 121 37 331

Find the minimal path sum, in matrix.txt (right click and 'Save Link/Target As...'), a 31K text file containing a 80 by 80 matrix, from the top left to the bottom right by moving left, right, up, and down.

Solution by jontsai <hello@jontsai.com>
"""
# Python Standard Library Imports
import copy
import resource
import sys

# PE Solution Library Imports
from utils import *


class Solution(object):
    EXPECTED_ANSWER = 2297
    MATRIX_INPUT_FILE = 'p081_test_matrix.txt'
    NUM_ROWS = 5
    NUM_COLS = 5

    # EXPECTED_ANSWER = 0
    # MATRIX_INPUT_FILE = 'p081_matrix.txt'
    # NUM_ROWS = 80
    # NUM_COLS = 80

    def __init__(self):
        self.matrix = self.get_matrix()

        self.memo = []
        for i in range(self.NUM_ROWS):
            self.memo.append([None] * self.NUM_COLS)

    def get_matrix(self):
        f = open(self.MATRIX_INPUT_FILE, 'r')
        lines = f.readlines()
        matrix = []
        for line in lines:
            row = [int(x) for x in line.strip().split(',')]
            assert(len(row) == self.NUM_COLS)
            matrix.append(row)
            f.close()
        assert(len(matrix) == self.NUM_ROWS)
        return matrix

    def solve(self):
        answer = self.min_path_sum(self.NUM_ROWS - 1, self.NUM_COLS - 1)
        return answer

    def min_path_sum(self, i, j, visited=None):
        if visited is None:
            visited = {}

        def _path_key(a, b):
            key = f'{a},{b}'
            return key

        visited[_path_key(i, j)] = True

        paths = []

        def _try_path(i2, j2):
            if _path_key(i2, j2) in visited:
                # already visited node, skip
                pass
            else:
                path = self.min_path_sum(i2, j2, visited=copy.copy(visited))
                if path is None:
                    # reached a dead end
                    pass
                else:
                    paths.append(path)

        node_value = self.matrix[i][j]

        if i == 0 and j == 0:
            mps = node_value
        else:
            if i > 0:  # above
                _try_path(i - 1, j)

            if i + 1 < self.NUM_ROWS:  # below
                _try_path(i + 1, j)

            if j > 0:  # left
                _try_path(i, j - 1)

            if j + 1 < self.NUM_COLS:  # right
                _try_path(i, j + 1)

            if len(paths) == 0:
                # reached a dead end
                mps = None
            else:
                mps = node_value + min(paths)

        return mps


def main():
    # https://stackoverflow.com/a/16248113/865091
    # resource.setrlimit(resource.RLIMIT_STACK, (2**29,-1))
    # sys.setrecursionlimit(10**6)

    solution = Solution()
    answer = solution.solve()

    print(f'Expected: {Solution.EXPECTED_ANSWER}, Answer: {answer}')


if __name__ == '__main__':
    main()
