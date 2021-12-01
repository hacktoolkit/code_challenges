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


class Move(namedtuple('Move', 'row col')):
    pass


MOVE_LEFT = Move(0, -1)
MOVE_RIGHT = Move(0, 1)
MOVE_UP = Move(-1, 0)
MOVE_DOWN = Move(1, 0)


class Position(object):
    def __init__(self, matrix, m, n):
        self.matrix = matrix
        self.moves = []
        self.m = m
        self.n = n
        self.cumulative_sum = matrix[m][n]

    def clone(self):
        """Returns a clone of this `Position`
        """
        cloned_position = Position(self.matrix, self.m, self.n)
        cloned_position.moves = copy.copy(self.moves)
        cloned_position.cumulative_sum = self.cumulative_sum
        return cloned_position

    @property
    def is_finished(self):
        return self.is_at_last_column

    @property
    def is_at_first_column(self):
        assert self.n >= 0
        return self.n == 0

    @property
    def is_at_last_column(self):
        assert self.n >= 0
        return self.n + 1 == Solution.NUM_COLS

    @property
    def is_at_top_row(self):
        assert self.m >= 0
        return self.m == 0

    @property
    def is_at_bottom_row(self):
        assert self.m >= 0
        return self.m + 1 == Solution.NUM_ROWS

    def get_next_positions(self):
        """Returns a list of subsequent `Position`s after applying all eligible moves
            """
        moves = self.get_eligible_moves()

        next_positions = []

        for move in moves:
            position = self.clone()
            position.do_move(move)
            next_positions.append(position)

        return next_positions

    def do_move(self, move):
        """Applies `move` to this `Position`
        """
        self.m += move.row
        self.n += move.col
        self.moves.append(move)
        self.cumulative_sum += self.matrix[self.m][self.n]

    def get_eligible_moves(self):
        """Returns a list of `Move`s that are eligible from this current position
        """
        moves = []
        if self.is_at_first_column:
            moves.append(MOVE_RIGHT)

        elif self.is_at_last_column:
            # no more eligible moves
            pass

        elif len(self.moves) > 0:
            # RIGHT is always an eligble move before last column
            moves.append(MOVE_RIGHT)

            # check UP and DOWN eligibility based on previous move
            prev_move = self.moves[-1]
            assert prev_move in (MOVE_LEFT, MOVE_RIGHT, MOVE_UP, MOVE_DOWN,)

            if prev_move == MOVE_RIGHT:
                if not self.is_at_top_row:
                    moves.append(MOVE_UP)

                if not self.is_at_bottom_row:
                    moves.append(MOVE_DOWN)

            elif prev_move == MOVE_UP and not self.is_at_top_row:
                moves.append(MOVE_UP)

            elif prev_move == MOVE_DOWN and not self.is_at_bottom_row:
                moves.append(MOVE_DOWN)

            else:
                pass

        else:
            raise Exception('Illegal state -- empty moves but not in starting column')

        return moves


class SolutionNaive(object):
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

    # solution = SolutionNaive()
    solution = Solution()
    answer = solution.solve()

    print(f'Expected: {Solution.EXPECTED_ANSWER}, Answer: {answer}')


if __name__ == '__main__':
    main()
