"""http://projecteuler.net/problem=145

How many reversible numbers are there below one-billion?

Some positive integers n have the property that the sum [ n + reverse(n) ] consists entirely of odd (decimal) digits. For instance, 36 + 63 = 99 and 409 + 904 = 1313. We will call such numbers reversible; so 36, 63, 409, and 904 are reversible. Leading zeroes are not allowed in either n or reverse(n).

There are 120 reversible numbers below one-thousand.

How many reversible numbers are there below one-billion (10^9)?

Solution by jontsai <hello@jontsai.com>
"""
from utils import *


EXPECTED_ANSWER = 0


def solve():
    global EXPECTED_ANSWER

    # LIMIT = 10**2
    # EXPECTED_ANSWER = 20

    # LIMIT = 10**3
    # EXPECTED_ANSWER = 120

    # LIMIT = 10**4
    # EXPECTED_ANSWER = 720 # 6x previous

    # LIMIT = 10**5
    # EXPECTED_ANSWER = 720 # 1x previous

    # LIMIT = 10**6
    # EXPECTED_ANSWER = 18720 # 26x previous
    
    # LIMIT = 10**7
    # EXPECTED_ANSWER = 68720 # no relationship to previous

    # LIMIT = 10**8
    # EXPECTED_ANSWER = 608720 # no relationship to previous

    # TODO:
    LIMIT = 10**9
    EXPECTED_ANSWER = 0 # ???

    # re-initialize the global `REVERSIBLE_MEMO` to be a fixed array for faster lookups
    global REVERSIBLE_MEMO
    REVERSIBLE_MEMO = [None] * LIMIT

    reversible_count = 0

    for n in xrange(1, LIMIT + 1):
        if n % 10**6 == 0:
            # print progress
            print n
        if is_reversible(n):
            reversible_count += 1

    answer = reversible_count

    return answer


def main():
    answer = solve()

    print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)


if __name__ == '__main__':
    main()
