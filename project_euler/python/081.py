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

EXPECTED_ANSWER = 427337

NUM_ROWS = 80
NUM_COLS = 80

def get_matrix():
    #matrix_file = 'test_matrix.txt'
    matrix_file = 'p081_matrix.txt'
    f = open(matrix_file, 'r')
    lines = f.readlines()
    matrix = []
    for line in lines:
        row = [int(x) for x in line.strip().split(',')]
        assert(len(row) == NUM_COLS)
        matrix.append(row)
    f.close()
    assert(len(matrix) == NUM_ROWS)
    return matrix

MEMO = []
for i in xrange(NUM_ROWS):
    MEMO.append([None] * 80)

def min_path_sum(matrix, i, j):
    if MEMO[i][j] is not None:
        answer = MEMO[i][j]
    else:
        current_value = matrix[i][j]
        if i == 0 and j == 0:
            answer = current_value
        elif i == 0:
            answer = current_value + min_path_sum(matrix, i, j - 1)
        elif j == 0:
            answer = current_value + min_path_sum(matrix, i - 1, j)
        else:
            sub_problem = min(
                min_path_sum(matrix, i, j - 1),
                min_path_sum(matrix, i - 1, j)
            )
            answer = current_value + sub_problem
        MEMO[i][j] = answer
    return answer

def solve():
    matrix = get_matrix()
    for i in xrange(NUM_ROWS):
        for j in xrange(NUM_COLS):
            answer = min_path_sum(matrix, i, j)
    return answer

answer = solve()

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
