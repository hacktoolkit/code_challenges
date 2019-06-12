"""
http://projecteuler.net/problem=078

Coin partitions

Let p(n) represent the number of different ways in which n coins can be separated into piles. For example, five coins can be separated into piles in exactly seven different ways, so p(5)=7.


OOOOO

OOOO   O

OOO   OO

OOO   O   O

OO   OO   O

OO   O   O   O

O   O   O   O   O


Find the least value of n for which p(n) is divisible by one million.


Solution by jontsai <hello@jontsai.com>
"""
from utils import *


EXPECTED_ANSWER = 0


def solve():
    answer = None
    return answer


def main():
    answer = solve()

    print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)


if __name__ == '__main__':
    main()
