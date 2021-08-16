#!/usr/bin/env python3
"""https://projecteuler.net/problem=745

Sum of Squares


For a positive integer, n, define g(n) to be the maximum perfect square that divides n.

For example, g(18) = 9, g(19) = 1.


Also define

S(N) = \sum_{n=1}^N g(n)


For example, S(10) = 24 and S(100) = 767.


Find S(10^{14}). Give your answer modulo 1,000,000,007.

Solution by jontsai <hello@jontsai.com>
"""

# Python Standard Library Imports
import math

# PE Solution Library Imports
from lib.search import binary_search
from utils import *


def main():
    solution = Solution()
    answer = solution.solve()

    # print(g(18) == 9)
    # print(g(19) == 1)

    print(f'Expected: {Solution.EXPECTED_ANSWER}, Answer: {answer}')


class Solution(object):
    MODULUS = 1000000007

    # PREV_GUESS = None
    # TARGET, EXPECTED_ANSWER = 10, 24

    PREV_GUESS = None
    TARGET, EXPECTED_ANSWER = 100, 767

    # PREV_GUESS = None
    # TARGET, EXPECTED_ANSWER = 10**14, 0


    def __init__(self):
        self.SQUARES = [
            n**2
            for n
            in range(
                1,
                int(math.ceil(math.sqrt(self.TARGET))) + 1
            )
        ]

        self.SQUARES_SET = set(self.SQUARES)

    def solve(self):
        answer = self.S(self.TARGET)
        return answer

    def g(self, n):
        """Maximum perfect square that divides n
        """
        divisor = None

        if n in self.SQUARES_SET:
            divisor = n
        else:
            initial_guess = Solution.PREV_GUESS

            index = binary_search(
                self.SQUARES,
                n,
                exact=False,
                ascending=True,
                initial_guess=initial_guess
            )

            while index >= 0:
                square = self.SQUARES[index]
                if n % square == 0:
                    divisor = square
                    Solution.PREV_GUESS = index
                    break
                index -= 1

        return divisor

    def S(self, N):
        total = 0
        for n in range(N, 0, -1):
            if n % 1000 == 0:
                print(n)

            total += self.g(n)
            total = total % self.MODULUS

        return total


if __name__ == '__main__':
    main()
