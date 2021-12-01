"""
http://projecteuler.net/problem=082

Path sum: three ways

NOTE: This problem is a more challenging version of Problem 81.
The minimal path sum in the 5 by 5 matrix below, by starting in any cell in the left column and finishing in any cell in the right column, and only moving up, down, and right, is indicated in red and bold; the sum is equal to 994.

131 673 234 103  18
201  96 342 965 150
630 803 746 422 111
537 699 497 121 956
805 732 524  37 331

Minimal Path: 201 96 342 234 103 18

Find the minimal path sum, in matrix.txt (right click and 'Save Link/Target As...'), a 31K text file containing a 80 by 80 matrix, from the left column to the right column.

Solution by jontsai <hello@jontsai.com>
"""

# Python Standard Library Imports
import copy
from collections import namedtuple

# PE Solution Library Imports
from utils import *


class Move(namedtuple('Move', 'row col')):
    pass


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
            assert prev_move in (MOVE_RIGHT, MOVE_UP, MOVE_DOWN,)

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


class Solution(object):
    # EXPECTED_ANSWER = 994
    # MATRIX_INPUT_FILE = 'p081_test_matrix.txt'
    # NUM_ROWS = 5
    # NUM_COLS = 5

    EXPECTED_ANSWER = 0
    MATRIX_INPUT_FILE = 'p081_matrix.txt'
    NUM_ROWS = 80
    NUM_COLS = 80

    def __init__(self):
        self.matrix = self.get_matrix()

        self.memo = []
        for i in range(self.NUM_ROWS):
            self.memo.append([None] * 80)

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
        positions = []

        for m in range(self.NUM_ROWS):
            n = 0
            position = Position(self.matrix, m, n)
            positions.append(position)

        best_result_so_far = None

        # DFS using a stack
        while len(positions) > 0:
            print(len(positions), best_result_so_far.cumulative_sum if best_result_so_far else 0)
            position = positions.pop()

            if position.is_finished:
                if best_result_so_far is None:
                    best_result_so_far = position
                elif position.cumulative_sum < best_result_so_far.cumulative_sum:
                    # a new best
                    best_result_so_far = position
            else:
                # position is not in finished state, progress it
                if best_result_so_far is not None and position.cumulative_sum >= best_result_so_far.cumulative_sum:
                    # already found a better result, prune this path
                    pass
                else:
                    next_positions = position.get_next_positions()
                    positions += next_positions

        answer = best_result_so_far.cumulative_sum
        return answer


def main():
    solution = Solution()
    answer = solution.solve()

    print('Expected: %s, Answer: %s' % (Solution.EXPECTED_ANSWER, answer))


if __name__ == '__main__':
    main()
