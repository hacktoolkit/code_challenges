"""http://projecteuler.net/problem=063

Powerful digit counts

The 5-digit number, 16807=7^5, is also a fifth power. Similarly, the 9-digit number, 134217728=8^9, is a ninth power.

How many n-digit positive integers exist which are also an nth power?

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

EXPECTED_ANSWER = 49

def solve():
    n = 1
    count = 0
    last_n = 0
    while True:
        if n - last_n > 1:
            break
        k = 1
        nth_power = k ** n
        num_digits = log_num_digits(nth_power)
        if num_digits > n:
            break

        while True:
            nth_power = k ** n
            num_digits = log_num_digits(nth_power)

            if num_digits < n:
                pass
            elif num_digits == n:
                last_n = n
                count += 1
                #print k, n, nth_power
            elif num_digits > n:
                n += 1
                break
            else:
                pass
            k += 1
            if k > 9:
                n += 1
                break

    answer = count
    return answer

answer = solve()

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
