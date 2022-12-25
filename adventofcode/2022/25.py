# Python Standard Library Imports
from functools import cache

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = ('20=022=21--=2--12=-2', None)
config.TEST_CASES = {
    '': ('2=-1=0', None),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data

    def solve1(self):
        decimals = [Snafu.to_decimal(snafu) for snafu in self.data]
        debug(decimals)

        total = sum(decimals)
        print(total)

        answer = Snafu.from_decimal(total)
        return answer

    def solve2(self):
        answer = None
        return answer


class Snafu:
    DIGITS = {
        '2': 2,
        '1': 1,
        '0': 0,
        '-': -1,
        '=': -2,
    }

    @classmethod
    @cache
    def to_decimal(cls, snafu_value):
        total = 0
        for i, snafu_digit in enumerate(reversed(snafu_value)):
            total += 5**i * cls.DIGITS[snafu_digit]

        return total

    @classmethod
    @cache
    def from_decimal(cls, value):
        # guess-and-check the number of snafu digits
        guess = ['2']
        while cls.to_decimal(''.join(guess)) < value:
            guess.append('2')

        # reduce the guess to fit the `value`
        for i, guess_digit in enumerate(guess):
            correct_digit = guess_digit
            for snafu_digit in Snafu.DIGITS:
                snafu_digits = guess[:i] + [snafu_digit] + guess[i + 1 :]
                if cls.to_decimal(''.join(snafu_digits)) >= value:
                    correct_digit = snafu_digit
                else:
                    break

            guess[i] = correct_digit

        snafu = ''.join(guess)
        return snafu


if __name__ == '__main__':
    main()
