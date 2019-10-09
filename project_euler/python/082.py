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
from utils import *


EXPECTED_ANSWER = 0


def solve():
    answer = None
    return answer


def main():
    answer = solve()

    print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)


if __name__ == '__main__':
    main()
