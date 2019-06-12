"""http://projecteuler.net/problem=146

Investigating a Prime Pattern 

The smallest positive integer n for which the numbers n^2+1, n^2+3, n^2+7, n^2+9, n^2+13, and n^2+27 are consecutive primes is 10. The sum of all such integers n below one-million is 1242490.

What is the sum of all such integers n below 150 million?

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

EXPECTED_ANSWER = 0

def solve(target):
    start = 10

    prime_addends = [1, 3, 7, 9, 13, 27,]

    total = 0

    # n * n must be even, otherwise the sums would not be prime
    # therefore, n must be even
    for n in xrange(start, target, 2):
        n_squared = n * n
        all_primes = True
        for addend in prime_addends:
            if not is_prime(n_squared + addend):
                all_primes = False
                break
            else:
                pass
        if all_primes:
            total += n
        else:
            pass

    answer = total
    #answer = None
    return answer

def main():
    target = 10**2
    #target = 150 * 10**6
    answer = solve(target)

    print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)

if __name__ == '__main__':
    main()
