"""
http://projecteuler.net/problem=179

Consecutive positive divisors

Find the number of integers 1 < n < 10^7, for which n and n + 1 have the same number of positive divisors. For example, 14 has the positive divisors 1, 2, 7, 14 while 15 has 1, 3, 5, 15.

Solution by jontsai <hello@jontsai.com>
"""
from utils import *


class Solution(object):
    TARGET = 16
    EXPECTED_ANSWER = 2

    # TARGET = 10**7
    # EXPECTED_ANSWER = 0

    def __init__(self):
        pass

    def solve(self):
        count = 0
        prev_num_divisors = None

        for n in xrange(2, Solution.TARGET):
            if n % 1000 == 0:
                print n
            divisors = get_divisors(n)
            num_divisors = len(divisors)
            if prev_num_divisors is not None and prev_num_divisors == num_divisors:
                count += 1
            prev_num_divisors = num_divisors

        answer = count
        return answer


def main():
    solution = Solution()
    answer = solution.solve()

    print 'Expected: %s, Answer: %s' % (Solution.EXPECTED_ANSWER, answer)


if __name__ == '__main__':
    main()
