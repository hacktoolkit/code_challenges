"""http://projecteuler.net/problem=087

Prime power triples

The smallest number expressible as the sum of a prime square, prime cube, and prime fourth power is 28. In fact, there are exactly four numbers below fifty that can be expressed in such a way:

28 = 2^2 + 2^3 + 2^4
33 = 3^2 + 2^3 + 2^4
49 = 5^2 + 2^3 + 2^4
47 = 2^2 + 3^3 + 2^4

How many numbers below fifty million can be expressed as the sum of a prime square, prime cube, and prime fourth power?

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

EXPECTED_ANSWER = 1097343

def solve(limit):
    """
    $ time python 087.py
    Expected: 1097343, Answer: 1097343

    real0m0.798s
    user0m0.645s
    sys0m0.100s
    """
    # setup
    square_limit = int(pow(limit, 1. / 2))
    cube_limit = int(pow(limit, 1. / 3))
    fourth_limit = int(pow(limit, 1. / 4))
    primes = generate_primes(square_limit)

    square_primes = filter(lambda x: x <= square_limit, primes)
    cube_primes = filter(lambda x: x <= cube_limit, primes)
    fourth_primes = filter(lambda x: x <= fourth_limit, primes)
    #print square_primes, cube_primes, fourth_primes

    # test all valid prime power sum combinations
    values = set()
    for a in square_primes:
        a_value = a**2
        for b in cube_primes:
            b_value = b**3
            if a_value + b_value >= limit:
                break
            for c in fourth_primes:
                c_value = c**4
                value = a_value + b_value + c_value
                if value < limit:
                    #print value, a, b, c
                    values.add(value)
                else:
                    break

    answer = len(values)
    return answer

answer = solve(50 * 10**6)

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
