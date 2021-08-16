#!/usr/bin/env python3
"""https://projecteuler.net/problem=700

Eulercoin

Leonhard Euler was born on 15 April 1707.

Consider the sequence 1504170715041707n mod 4503599627370517.

An element of this sequence is defined to be an Eulercoin if it is strictly smaller than all previously found Eulercoins.

For example, the first term is 1504170715041707 which is the first Eulercoin.  The second term is 3008341430083414 which is greater than 1504170715041707 so is not an Eulercoin.  However, the third term is 8912517754604 which is small enough to be a new Eulercoin.

The sum of the first 2 Eulercoins is therefore 1513083232796311.

Find the sum of all Eulercoins.

Solution by jontsai <hello@jontsai.com>
"""
# PE Solution Library Imports
from lib.modular import modular_multiply
from utils import *


class Solution(object):
    EXPECTED_ANSWER = 0

    BASE = 1504170715041707
    MODULUS = 4503599627370517

    def __init__(self):
        self.EULERCOINS_COUNT = 0
        self.EULERCOINS_TOTAL = 0
        self.SMALLEST_EULERCOIN = None
        self.PREV_RESULT = None

    def solve(self):
        answer = None

        n = 1
        did_repeat = False
        for n in range(1, self.MODULUS + 1):
            v = self.s(n)
            # print(n, v)
            was_updated = self.update_eulercoin(v)
            if was_updated:
                print(n, v)

        answer = self.EULERCOINS_TOTAL

        return answer

    def s(self, n):
        """Calculates `1504170715041707n mod 4503599627370517` for `n`

        Assumes that we are doing so sequentially, so optimizes by adding to the previously stored result
        """
        if n == 1:
            result = self.BASE
        else:
            result = (self.PREV_RESULT + self.BASE) % self.MODULUS

        self.PREV_RESULT = result

        return result

    def update_eulercoin(self, v):
        if self.SMALLEST_EULERCOIN is None or v < self.SMALLEST_EULERCOIN:
            self.SMALLEST_EULERCOIN = min(
                self.SMALLEST_EULERCOIN or v,
                v
            )
            self.EULERCOINS_COUNT += 1
            self.EULERCOINS_TOTAL += v

            was_updated = True
        else:
            was_updated = False

        return was_updated


def main():
    solution = Solution()
    answer = solution.solve()

    print(f'Expected: {Solution.EXPECTED_ANSWER}, Answer: {answer}')


if __name__ == '__main__':
    main()
