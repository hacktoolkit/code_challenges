#!/usr/bin/env python3
"""http://projecteuler.net/problem=074

Digit factorial chains

The number 145 is well known for the property that the sum of the factorial of its digits is equal to 145:

1! + 4! + 5! = 1 + 24 + 120 = 145

Perhaps less well known is 169, in that it produces the longest chain of numbers that link back to 169; it turns out that there are only three such loops that exist:

169 -> 363601 -> 1454 -> 169
871 -> 45361 -> 871
872 -> 45362 -> 872

It is not difficult to prove that EVERY starting number will eventually get stuck in a loop. For example,

69 -> 363600 -> 1454 -> 169 -> 363601 (-> 1454)
78 -> 45360 -> 871 -> 45361 (-> 871)
540 -> 145 (-> 145)

Starting with 69 produces a chain of five non-repeating terms, but the longest non-repeating chain with a starting number below one million is sixty terms.

How many chains, with a starting number below one million, contain exactly sixty non-repeating terms?

Solution by jontsai <hello@jontsai.com>
"""
# Python Standard Library Imports
from functools import lru_cache

# PE Solution Library Imports
from utils import *


class Solution(object):
    EXPECTED_ANSWER = 402

    def __init__(self):
        pass

    def solve(self):
        answer = None
        print(self.digit_factorial_chain_length(69))

        count = 0
        for n in range(10**6):
            if n % 1000 == 0:
                print(n)

            chain_length = self.digit_factorial_chain_length(n)
            if chain_length == 60:
                count += 1

        answer = count

        return answer

    @lru_cache
    def digit_factorial_sum(self, n):
        """Gets the sum of the factorial of each digit of `n`
        """
        df_sum =  sum([factorial(digit) for digit in digits(n)])
        return df_sum

    @lru_cache
    def digit_factorial_chain_length(self, n):
        chain_length = 0

        seen = {}
        df_sum = n
        while df_sum not in seen:
            seen[df_sum] = True
            chain_length += 1
            df_sum = self.digit_factorial_sum(df_sum)

        return chain_length


def main():
    solution = Solution()
    answer = solution.solve()

    print(f'Expected: {Solution.EXPECTED_ANSWER}, Answer: {answer}')


if __name__ == '__main__':
    main()
