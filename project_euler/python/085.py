"""http://projecteuler.net/problem=085

Counting rectangles

By counting carefully it can be seen that a rectangular grid measuring 3 by 2 contains eighteen rectangles:

- 6 1x1
- 4 1x2
- 2 1x3
- 3 2x1
- 2 2x2
- 1 3x2

Although there exists no rectangular grid that contains exactly two million rectangles, find the area of the grid with the nearest solution.

Solution by jontsai <hello@jontsai.com>
"""
import math

from utils import *

EXPECTED_ANSWER = 0

MEMO = {}

def get_subrectangles(m, n):
    m, n = (max(m, n), min(m, n))
    num_rectangles = 0
    if m <= 0 or n <= 0:
        num_rectangles = 0
    elif m == 1:
        num_rectangles = sum([math.ceil(n / (n - j)) for j in xrange(n)])
    elif n == 1:
        num_rectangles = sum([math.ciel(m / (m - i)) for i in xrange(m)])
    else:
        # number of subrectangles in (m * n) =
        #   number of unique unit rectangles in this level: m + n - 1
        #   number of row-wise: m
        #   number of col-wise: n
        #
        parts = (
            # number of subrectangles in smaller problem: get_subrectangles(m - 1, n - 1)
            get_subrectangles(m - 1, n - 1),
            # number of unique unit rectangles in this level: m + n - 1
            m + n - 1,
            # number of new subrectangles formed by (m * (n - j)) for j = [0, n)
            m * sum([math.ceil(n / (n - j)) for j in xrange(n)]),
            # number of new subrectangles formed by (n * (m - i)) for i = [0, m)
            sum([math.ciel(m / (m - i)) for i in xrange(m)]),
            # number of new subrectangles sized (m - 1, n - 1): 3
            3,
        )
        num_rectangles = sum(parts)
    return num_rectangles

def solve():
    for i in xrange(3):
        for j in xrange(3):
            answer = get_subrectangles(i, j)
            print i, j, answer
    return answer

answer = solve()

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
