"""http://projecteuler.net/problem=073

Counting fractions in a range

Consider the fraction, n/d, where n and d are positive integers. If n<d and HCF(n,d)=1, it is called a reduced proper fraction.

If we list the set of reduced proper fractions for d <= 8 in ascending order of size, we get:

1/8, 1/7, 1/6, 1/5, 1/4, 2/7, 1/3, 3/8, 2/5, 3/7, 1/2, 4/7, 3/5, 5/8, 2/3, 5/7, 3/4, 4/5, 5/6, 6/7, 7/8

It can be seen that there are 3 fractions between 1/3 and 1/2.

How many fractions lie between 1/3 and 1/2 in the sorted set of reduced proper fractions for d <= 12,000?

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

EXPECTED_ANSWER = 7295372

def solve(lower, upper, limit):
    """
    $ time python 073.py 
    Expected: 7295372, Answer: 7295372

    real0m13.999s
    user0m13.606s
    sys0m0.134s
    """
    count = 0
    for d in xrange(2, limit + 1):
        #print d
        # optimization: don't test fractions below `lower` or above `upper`
        n_lower = int(math.floor(d * lower)) + 1
        n_upper = int(math.ceil(d * upper)) - 1
        n = n_lower
        for n in xrange(max(1, n_lower), n_upper + 1):
            hcf = gcd(n, d)
            if hcf != 1:
                continue
            else:
                value = n * 1.0 / d
                count += 1
    # solve
    answer = count
    return answer

#answer = solve(lower=1/3., upper=1/2., limit=8)
#answer = solve(lower=1/3., upper=1/2., limit=9)
answer = solve(lower=1/3., upper=1/2., limit=12000)

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
