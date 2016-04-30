"""http://projecteuler.net/problem=243

Resilience
 
A positive fraction whose numerator is less than its denominator is called a proper fraction.
For any denominator, d, there will be d-1 proper fractions; for example, with d = 12:
1/12 , 2/12 , 3/12 , 4/12 , 5/12 , 6/12 , 7/12 , 8/12 , 9/12 , 10/12 , 11/12 .

We shall call a fraction that cannot be cancelled down a resilient fraction.
Furthermore we shall define the resilience of a denominator, R(d), to be the ratio of its proper fractions that are resilient; for example, R(12) = 4/11.
In fact, d = 12 is the smallest denominator having a resilience R(d) < 4/10.

Find the smallest denominator d, having a resilience R(d) < 15499/94744.

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

EXPECTED_ANSWER = 0

def solve(limit):
    """
    Observations:

    1. For all prime numbers p, its resilience R(p) = 1
    2. The first and last fraction are always resilient.
    3. All fractions with a prime numerator that is not a factor of the denominator are resilient.
    """
    resilience = limit[0] * 1.0 / limit[1]
    d = limit[1]
    answer = None
    while answer is None:
        num_resilient = 0
        r = 0
        for n in xrange(1, d):
            if gcd(n, d) == 1:
                num_resilient += 1
                r = (num_resilient * 1.0) / (d - 1)
            if r >= resilience:
                break
        print d, r
        if r < resilience:
            answer = d
            break
        d += 1
    return answer

def main():
    answer = solve(limit=(15499,94744,))

    print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)

if __name__ == '__main__':
    main()
