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
from utils import *

EXPECTED_ANSWER = 0

memo = {
    145 : 1,
    # 169
    169 : 3,
    363601 : 3,
    1454 : 3,
    # 871
    871 : 2,
    45361 : 2,
    # 871
    872 : 2,
    45362 : 2,
    # generic
    0 : 2,
    1 : 1,
    2 : 1,
}

def digit_factorial_equivalent(n):
    """Removes 0 digits and sorts remaining digits in ascending order
    """
    _digits = sorted(filter(lambda x: x, digits(n)))
    n1 = int(''.join([str(digit) for digit in _digits]))
    return n1

def digit_factorial_sum(n):
    """Gets the sum of the factorial of each digit of `n`
    """
    df_sum =  sum([factorial(digit) for digit in digits(n)])
    return df_sum

def get_digit_factorial_chain_length(n):
    n1 = digit_factorial_equivalent(n)
    if n in memo:
        chain_length = memo[n]
    elif n1 in memo:
        chain_length = memo[n1]
    else:
        seen = {
            n: True,
        }
        df_chain = [n]
        df_sum = digit_factorial_sum(n)
        while df_sum not in seen:
            df_chain.append(df_sum)
            seen[df_sum] = True
            df_sum = digit_factorial_sum(df_sum)
        chain_length = len(df_chain)
        for i in xrange(chain_length):
            x = df_chain[i]
            memo[x] = chain_length - i
            if x == df_sum:
                break
        if n1 != n and df_sum != n:
            memo[n1] = chain_length
    return chain_length

def solve(limit, num_terms):
    count = 0
    for n in xrange(1, limit):
        chain_length = get_digit_factorial_chain_length(n)
        if chain_length == num_terms:
            count += 1
    answer = count
    return answer

answer = solve(10**6, 60)

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
