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

EXPECTED_ANSWER = 0

def solve(lower, upper, limit):
    memo = {}
    memo2 = {}
    count = 0
    for d in xrange(1, limit + 1):
        #print d
        # optimization: don't test fractions below `lower` or above `upper`
        n_lower = int(math.floor(d * lower)) + 1
        n_upper = int(math.ceil(d * upper)) - 1
        n = max(1, n_lower)
        for n in xrange(max(1, n_lower), n_upper + 1):
            key = '%s/%s' % (n, d)
            a, b = reduce(n, d)
            key2 = '%s/%s' % (a, b)
            if key2 not in memo2:
                memo2[key2] = True
            if key in memo:
                break
            else:
                value = n * 1.0 / d
                for k in xrange(1, limit / d + 1):
                    # mark all expanded fractions
                    key = '%s/%s' % (n * k, d * k)
                    memo[key] = value
                count += 1
    # solve
    #sorted_fractions = sorted(memo.items(), key=lambda x: x[1])
    #print sorted_fractions
    #answer = count
    print count
    answer = len(memo2)
    return answer

#answer = solve(lower=1/3., upper=1/2., limit=8)
#answer = solve(lower=1/3., upper=1/2., limit=9)
answer = solve(lower=1/3., upper=1/2., limit=12000)

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
