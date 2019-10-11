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
from collections import namedtuple

from utils import *


EXPECTED_ANSWER = 2772


def count_rectangles(m, n):
    """Returns the number of sub-rectangles in a rectangular grid of size m x n
    """
    def _place_subrectangles(mm, nn):
        """Returns the number of ways an mm x nn sub-rectangle can be placed within the larger m x n rectagle
        """
        num_placements = 0

        # TODO: use maths to make more efficient
        for i in xrange(m + 1):
            for j in xrange(n + 1):
                if i - mm >= 0 and j - nn >= 0:
                    num_placements += 1
        return num_placements

    num_rectangles = 0

    for i in xrange(m, 0, -1):
        for j in xrange(n, 0, -1):
            num_rectangles += _place_subrectangles(i, j)

    return num_rectangles


def solve():
    target = 2 * 10**6

    memo = {}

    best_so_far = None

    Result = namedtuple('result', 'm n num_rectangles delta')


    # 1x2000 grid will already exceed 2M sub-rectangles
    for i in xrange(2001):
        for j in xrange(2001):
            m, n = (min(i, j), max(i, j),)

            key = '%sx%s' % (m, n,)
            if key in memo:
                num_rectangles = memo[key]
            else:
                num_rectangles = count_rectangles(m, n)
                memo[key] = num_rectangles

            delta = abs(target - num_rectangles)
            result = Result(m, n, num_rectangles, delta)
            print result

            if best_so_far is None or delta < best_so_far.delta:
                best_so_far = result

            if num_rectangles > target:
                break

        # TODO: optimize this loop by breaking earlier

    print best_so_far
    answer = best_so_far.m * best_so_far.n
    return answer


def main():
    answer = solve()

    print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)


if __name__ == '__main__':
    main()
