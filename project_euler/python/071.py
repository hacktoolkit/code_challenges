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

#real30m14.628s
#user29m44.546s
#sys0m9.036s
EXPECTED_ANSWER = 428570

def solve(marker, limit):
    best_so_far = None
    best_so_far_key = None
    # precompute
    for d in xrange(1, limit):
        #print d
        # optimization: don't test fractions below `lower`
        n_upper = int(math.ceil(d * marker)) - 1
        n = max(1, n_upper)
        a, b = reduce(n, d)
        key = '%s/%s' % (a, b)
        value = a * 1.0 / b
        if value < marker:
            if best_so_far is None or value > best_so_far:
                best_so_far = value
                best_so_far_key = key
    # solve
    answer = best_so_far_key.split('/')[0]
    return answer

#answer = solve(3./7, 8)
answer = solve(3./7, 1000000)

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
