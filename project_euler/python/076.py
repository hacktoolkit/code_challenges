"""http://projecteuler.net/problem=076

Counting summations

It is possible to write five as a sum in exactly six different ways:
4 + 1
3 + 2
3 + 1 + 1
2 + 2 + 1
2 + 1 + 1 + 1
1 + 1 + 1 + 1 + 1

How many different ways can one hundred be written as a sum of at least two positive integers?

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

EXPECTED_ANSWER = 0

def count_summations(n):
    if n == 2:
        num_summations = 1
    else:
        num_summations = 1 + count_summations(n - 1)

def solve():
    n = 5
    a = 2
    b = 4
    while n < 101:
        c = a + b
        a = b
        b = c
        answer = c
        print n, answer
        n += 1
    return answer

answer = solve()

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
