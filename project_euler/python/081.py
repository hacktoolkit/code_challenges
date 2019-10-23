"""
http://projecteuler.net/problem=081

Path sum: two ways

In the 5 by 5 matrix below, the minimal path sum from the top left to the bottom right, by **only moving to the right and down**, is indicated in bold red and is equal to 2427.

131 673 234 103  18
201  96 342 965 150
630 803 746 422 111
537 699 497 121 956
805 732 524  37 331

131 201 96 342 746 422 121 37 331

Find the minimal path sum, in matrix.txt (right click and 'Save Link/Target As...'), a 31K text file containing a 80 by 80 matrix, from the top left to the bottom right by only moving right and down.

Solution by jontsai <hello@jontsai.com>
"""
from utils import *


class Solution(object):
    EXPECTED_ANSWER = 427337


    # MATRIX_INPUT_FILE = 'p081_test_matrix.txt'
    # NUM_ROWS = 5
    # NUM_COLS = 5

    MATRIX_INPUT_FILE = 'p081_matrix.txt'
    NUM_ROWS = 80
    NUM_COLS = 80

    def __init__(self):
        self.matrix = self.get_matrix()

        self.memo = []
        for i in xrange(self.NUM_ROWS):
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
        for i in xrange(self.NUM_ROWS):
            for j in xrange(self.NUM_COLS):
                answer = self.min_path_sum2(i, j)
        return answer

    def min_path_sum2(self, i, j):
        matrix = self.matrix

        if self.memo[i][j] is not None:
            answer = self.memo[i][j]
        else:
            current_value = matrix[i][j]
            if i == 0 and j == 0:
                answer = current_value
            elif i == 0:
                answer = current_value + self.min_path_sum2(i, j - 1)
            elif j == 0:
                answer = current_value + self.min_path_sum2(i - 1, j)
            else:
                sub_problem = min(
                    self.min_path_sum2(i, j - 1),
                    self.min_path_sum2(i - 1, j)
                )
                answer = current_value + sub_problem
                self.memo[i][j] = answer
        return answer


def main():
    solution = Solution()
    answer = solution.solve()

    print 'Expected: %s, Answer: %s' % (Solution.EXPECTED_ANSWER, answer)


if __name__ == '__main__':
    main()
