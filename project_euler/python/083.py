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
