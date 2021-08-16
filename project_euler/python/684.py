#!/usr/bin/env python3
"""
Solution by jontsai <hello@jontsai.com>
"""
# Python Standard Library Imports
from functools import lru_cache

# PE Solution Library Imports
from utils import *


class Solution(object):
    MODULUS = 1000000007
    EXPECTED_ANSWER = 0

    def __init__(self):
        pass

    def solve(self):
        answer = None

        # print(self.S(20))

        total = 0
        for i in range(2, 91):
            k = fibonacci(i)
            l = self.S(k)
            print(i, k, l)
            total += l
            total %= self.MODULUS

        answer = total

        return answer

    @lru_cache
    def s(self, n):
        answer = None
        k = 1
        while answer is None:
            s = sum_digits(k)
            if s == n:
                answer = k
                break
            else:
                k += 1

        return answer

    def S(self, k):
        total = 0
        for n in range(1, k + 1):
            total += self.s(n)

        return total



def main():
    solution = Solution()
    answer = solution.solve()

    print(f'Expected: {Solution.EXPECTED_ANSWER}, Answer: {answer}')


if __name__ == '__main__':
    main()
