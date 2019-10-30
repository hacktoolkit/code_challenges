"""
http://projecteuler.net/problem=357

Prime generating integers

Consider the divisors of 30: 1,2,3,5,6,10,15,30.
It can be seen that for every divisor d of 30, d+30/d is prime.

Find the sum of all positive integers n not exceeding 100 000 000 such that
for every divisor d of n, d+n/d is prime.

Solution by jontsai <hello@jontsai.com>
"""
from utils import *


class Solution(object):
    EXPECTED_ANSWER = 0
    TARGET = 10 ** 4

    def __init__(self):
        pass

    def is_prime_generating_integer(self, n):
        """Returns True if every divisor of `n` satisfies is_prime(d+30/d) is True
        """
        result = True

        divisors = get_divisors(n)

        for d in divisors:
            x = d + n / d
            if not is_prime(x):
                result = False
                break

        return result
    
    def solve(self):
        subtotal = 0

        for n in xrange(1, self.TARGET + 1):
            if self.is_prime_generating_integer(n):
                subtotal += 1

        answer = subtotal
        return answer


def main():
    solution = Solution()
    answer = solution.solve()

    print 'Expected: %s, Answer: %s' % (Solution.EXPECTED_ANSWER, answer)


if __name__ == '__main__':
    main()
