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

EXPECTED_ANSWER = 0

def reduce(n, d):
    _gcd = gcd(n, d)
    a, b = (n / _gcd, d / _gcd)
    return a, b

def solve(marker, limit, lower=0):
    memo = {}
    best_so_far = {}
    # precompute
    for d in xrange(1, limit):
        #print d
        # optimization: don't test fractions below `lower`
        n = max(1, int(d * (marker + lower) / 2))
        while n < d:
            if n / marker > d:
                # optimization: don't test fractions larger than `marker`
                break
            a, b = reduce(n, d)
            key = '%s/%s' % (a, b)
            n += 1
            if key in memo:
                # optimization: already computed the reduced version of this fraction
                continue
            else:
                value = a / (b * 1.0)
                # if value < lower:
                # memoize
                best_so_far[key] = value
                memo[key] = value
                # pruning
                if len(best_so_far) > 1:
                    sorted_fractions = sorted(best_so_far.items(), key=lambda x: x[1])
                    lower = sorted_fractions[-2][1]
                    best_so_far = dict(sorted_fractions[-2:])
                    n = max(1, n, int(d * (marker + lower) / 2))
    # solve
    sorted_fractions = sorted(best_so_far.items(), key=lambda x: x[1])
    #print sorted_fractions
    answer = sorted_fractions[-2][0].split('/')[0]
    return answer

#answer = solve(3/7., 8, lower=2/5.)
answer = solve(3/7., 1000000, lower=2/5.)

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
