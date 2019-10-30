# coding=utf-8

"""
http://projecteuler.net/problem=069

Totient maximum

Euler's Totient function, φ(n) [sometimes called the phi function], is used to determine the number of numbers less than n which are relatively prime to n. For example, as 1, 2, 4, 5, 7, and 8, are all less than nine and relatively prime to nine, φ(9)=6.


n    Relatively Prime    φ(n)    n/φ(n)
2    1                   1       2
3    1,2                 2       1.5
4    1,3                 2       2
5    1,2,3,4             4       1.25
6    1,5                 2       3
7    1,2,3,4,5,6         6       1.1666...
8    1,3,5,7             4       2
9    1,2,4,5,7,8         6       1.5
10   1,3,7,9             4       2.5


It can be seen that n=6 produces a maximum n/φ(n) for n <= 10.

Find the value of n <= 1,000,000 for which n/φ(n) is a maximum.

Solution by jontsai <hello@jontsai.com>
"""
from collections import namedtuple

from utils import *


class Solution(object):
    TARGET = 10
    EXPECTED_ANSWER = 6

    # TARGET = 10**6
    # EXPECTED_ANSWER = 0

    def __init__(self):
        pass

    def solve(self):
        Result = namedtuple('Result', 'n phi_ratio')
        best_so_far = None

        for n in xrange(2, Solution.TARGET + 1):
            if n % 1000 == 0:
                print n
            phi_result = phi(n)
            phi_ratio =  n * 1.0 / phi_result

            #print n, phi_result, phi_ratio

            if best_so_far is None or phi_ratio > best_so_far.phi_ratio:
                best_so_far = Result(n, phi_ratio)

        answer = best_so_far.n
        return answer


def main():
    solution = Solution()
    answer = solution.solve()

    print 'Expected: %s, Answer: %s' % (Solution.EXPECTED_ANSWER, answer)


if __name__ == '__main__':
    main()
