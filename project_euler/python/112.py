#!/usr/bin/env python3
"""http://projecteuler.net/problem=112

Bouncy numbers

Working from left-to-right if no digit is exceeded by the digit to its left it is called an increasing number; for example, 134468.

Similarly if no digit is exceeded by the digit to its right it is called a decreasing number; for example, 66420.

We shall call a positive integer that is neither increasing nor decreasing a "bouncy" number; for example, 155349.

Clearly there cannot be any bouncy numbers below one-hundred, but just over half of the numbers below one-thousand (525) are bouncy. In fact, the least number for which the proportion of bouncy numbers first reaches 50% is 538.

Surprisingly, bouncy numbers become more and more common and by the time we reach 21780 the proportion of bouncy numbers is equal to 90%.

Find the least number for which the proportion of bouncy numbers is exactly 99%.

Solution by jontsai <hello@jontsai.com>
"""
# PE Solution Library Imports
from utils import *


class Solution(object):
    # TARGET, EXPECTED_ANSWER = 0.5, 538
    # TARGET, EXPECTED_ANSWER = 0.9, 21780
    TARGET, EXPECTED_ANSWER = 0.99, 1587000

    def __init__(self):
        pass

    def solve(self):
        answer = None

        n = 1
        num_tested = 0
        num_bouncy = 0
        percentage_bouncy = 0
        while answer is None:
            num_tested += 1

            bouncy = self.is_bouncy(n)
            if bouncy:
                num_bouncy += 1
            else:
                pass

            percentage_bouncy = 1.0 * num_bouncy / num_tested

            #print(n, num_bouncy, num_tested, percentage_bouncy)

            if percentage_bouncy == self.TARGET:
                answer = n
            else:
                pass

            n += 1

        return answer

    def is_increasing(self, n):
        result = True

        prev_digit = None
        for d in digits(n):
            if prev_digit is None:
                pass
            elif d < prev_digit:
                result = False
                break

            prev_digit = d

        return result

    def is_decreasing(self, n):
        result = True

        prev_digit = None
        for d in digits(n):
            if prev_digit is None:
                pass
            elif d > prev_digit:
                result = False
                break

            prev_digit = d

        return result

    def is_bouncy(self, n):
        result = not(
            self.is_decreasing(n)
            or self.is_increasing(n)
        )
        return result


def main():
    solution = Solution()
    answer = solution.solve()

    print(f'Expected: {Solution.EXPECTED_ANSWER}, Answer: {answer}')


if __name__ == '__main__':
    main()
