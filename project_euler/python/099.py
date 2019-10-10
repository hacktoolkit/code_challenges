"""
http://projecteuler.net/problem=099

Largest exponential

Comparing two numbers written in index form like 2^11 and 3^7 is not difficult, as any calculator would confirm that 2^11 = 2048 < 3^7 = 2187.

However, confirming that 632382^518061 > 519432^525806 would be much more difficult, as both numbers contain over three million digits.

Using base_exp.txt (right click and 'Save Link/Target As...'), a 22K text file containing one thousand lines with a base/exponent pair on each line, determine which line number has the greatest numerical value.

NOTE: The first two lines in the file represent the numbers in the example given above.

Solution by jontsai <hello@jontsai.com>
"""
from utils import *


EXPECTED_ANSWER = 0


def solve():
    pairs = []
    with open('base_exp.txt', 'r') as f:
        for line in f.readlines():
            base, exp = [int(x) for x in line.strip().split(',')]
            pair = (base, exp,)
            pairs.append(pair)

    largest_value = None
    largest_value_line = None

    current_line = 1
    for base, exp in pairs:
        print base, exp
        value = power(base, exp)
        if largest_value is None or value > largest_value:
            largest_value = value
            largest_value_line = current_line

        current_line += 1

    answer = largest_value_line
    return answer


def main():
    answer = solve()

    print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)


if __name__ == '__main__':
    main()
