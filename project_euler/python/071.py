"""http://projecteuler.net/problem=071

Ordered fractions

Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper fraction.
If we list the set of reduced proper fractions for d <= 8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that 2/5 is the fraction immediately to the left of 3/7.

By listing the set of reduced proper fractions for d <= 1,000,000 in ascending order of size, find the numerator of the fraction immediately to the left of 3/7.

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

EXPECTED_ANSWER = 428570

def solve1(marker, limit):
    """
    python 071.py
    Expected: 428570, Answer: 428570

    real30m14.628s
    user29m44.546s
    sys0m9.036s
    """
    best_so_far = -1
    best_n = None
    best_d = None
    best_so_far_key = None
    # precompute
    for d in xrange(2, limit + 1):
        print d
        n_upper = int(math.ceil(d * marker)) - 1
        n = n_upper
        hcf = gcd(n, d)
        if hcf == 1:
            value = n * 1.0 / d
            if best_so_far < value < marker:
                best_so_far = value
                best_n = n
                best_d = d
    # solve
    print '%s/%s' % (best_n, best_d,)
    answer = best_n
    return answer

def solve2(marker, limit):
    """Attempt at a more efficient solution

    The numerator of the reduced proper fraction
    immediately to the left of 3/7 will be the fraction
    with the greatest value -- largest numerator with smallest denominator
    """
    best_so_far = None
    # precompute
    for d in xrange(limit, 0, -1):
        n_upper = int(math.ceil(d * marker)) - 1
        n = max(1, n_upper)
        hcf = gcd(n, d)
        value = n * 1.0 / d
        if hcf == 1 and value < marker:
            print n, d
            best_so_far = n
            break
    # solve
    answer = best_so_far
    return answer

def solve(marker, limit):
    return solve1(marker, limit)

#answer = solve(3./7, 8)
answer = solve(3./7, 10**6)

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
