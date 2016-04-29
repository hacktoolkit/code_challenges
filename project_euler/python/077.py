"""http://projecteuler.net/problem=077

Prime summations

It is possible to write ten as the sum of primes in exactly five different ways:

7 + 3
5 + 5
5 + 3 + 2
3 + 3 + 2 + 2
2 + 2 + 2 + 2 + 2

What is the first value which can be written as the sum of primes in over five thousand different ways?

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

EXPECTED_ANSWER = 71

primes = generate_primes(100)

def prime_sums(value, prime_index):
    if value == 0:
        ways = 1
    elif value < 0:
        ways = 0
    else:
        prime = primes[prime_index]
        ways = 0
        if prime <= value:
            ways += prime_sums(value - prime, prime_index)
        if prime_index + 1 < len(primes):
            ways += prime_sums(value, prime_index + 1)
    return ways

def solve(threshold):
    """
    $ time python 077.py
    Expected: 71, Answer: 71

    real0m3.966s
    user0m3.755s
    sys0m0.087s
    """
    answer = None
    n = 2
    while answer is None:
        num_ways = prime_sums(n, 0)
        #print n, num_ways
        if num_ways > threshold:
            answer = n
        n += 1
    return answer

answer = solve(5000)

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
