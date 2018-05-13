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

EXPECTED_ANSWER = 190569291

MEMO = {
    0 : 0,
    1 : 0,
    2 : 1,
}

# TODO: BROKEN. how to fix?
def count_summations(n):
    """Count the number of ways to write `n` as a sum of two or more positive integers

    Written another way, the first 7 expansions are:
    1: None
    2: 1  - [                                                                                                                                                          1+1]
    3: 2  - [                                                                                                                                            2+1           1+1+1]
    4: 4  - [                                                                                                  3+1                           2+2         2+1+1         1+1+1+1]
    5: 6  - [                                                        4+1                             3+2       3+1+1                         2+2+1       2+1+1+1       1+1+1+1+1]
    6: 10 - [                        5+1                     4+2     4+1+1           3+3             3+2+1     3+1+1+1             2+2+2     2+2+1+1     2+1+1+1+1     1+1+1+1+1+1]
    7: 14 - [        6+1       5+2   5+1+1       4+3         4+2+1   4+1+1+1         3+3+1   3+2+2   3+2+1+1   3+1+1+1+1           2+2+2+1   2+2+1+1+1   2+1+1+1+1+1   1+1+1+1+1+1+1+1]
    8: 21 - [7+1 6+2 6+1+1 5+3 5+2+1 5+1+1+1 4+4 4+3+1 4+2+2 4+2+1+1 4+1+1+1+1 3+3+2 3+3+1+1 3+2+2+1 3+2+1+1+1 3+1+1+1+1+1 2+2+2+2 2+2+2+1+1 2+2+1+1+1+1 2+1+1+1+1+1+1 1+1+1+1+1+1+1+1+1]


    """
    if n in MEMO:
        num_ways = MEMO[n]
    else:
        num_ways = (
            # +1 to every way to write (n - 1)
            count_summations(n - 1)
            # (n-1) + 1
            + 1
        )

        # groupings for 1's
        for x in xrange(2, n + 1):
            if x == 2 and n > 4 and (n & (n - 1) == 0):
                # n is a power of 2 greater than 4
                num_groupings = (n / x)
            else:
                num_groupings = (n / x) - 1
            num_ways += num_groupings

        MEMO[n] = num_ways
    return num_ways


COINS = list(xrange(1, 100,))
COINS.reverse()

COIN_SUMS_MEMO = {}
def coin_sums(amount, coin_index):
    key = '%s:%s' % (amount, coin_index,)

    if key in COIN_SUMS_MEMO:
        num_ways = COIN_SUMS_MEMO[key]
    elif amount == 0:
        num_ways = 1
    else:
        coin = COINS[coin_index]
        num_ways = 0
        if coin <= amount:
            num_ways += coin_sums(amount - coin, coin_index)
        if coin_index + 1 < len(COINS):
            num_ways += coin_sums(amount, coin_index + 1)

        COIN_SUMS_MEMO[key] = num_ways
    return num_ways

def solve():
    answer = None
    for x in xrange(101):
        # TODO: this method is broken
        #answer = count_summations(x)

        # this problem is just adapted from Problem 031 - Coin Sums
        # modifying the inputs to solve!
        answer = coin_sums(100, 0)
        print x, answer
    return answer

answer = solve()

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
