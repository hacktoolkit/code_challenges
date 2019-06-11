"""http://projecteuler.net/problem=145

How many reversible numbers are there below one-billion?

Some positive integers n have the property that the sum [ n + reverse(n) ] consists entirely of odd (decimal) digits. For instance, 36 + 63 = 99 and 409 + 904 = 1313. We will call such numbers reversible; so 36, 63, 409, and 904 are reversible. Leading zeroes are not allowed in either n or reverse(n).

There are 120 reversible numbers below one-thousand.

How many reversible numbers are there below one-billion (10^9)?

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

#LIMIT = 10**3
#EXPECTED_ANSWER = 120

#LIMIT = 10**4
#EXPECTED_ANSWER = 720 # 6x previous

#LIMIT = 10**5
#EXPECTED_ANSWER = 720 # 1x previous

#LIMIT = 10**6
#EXPECTED_ANSWER = 18720 # 18x previous

#LIMIT = 10**7
#EXPECTED_ANSWER = 68720 # 3x previous

# TODO:
LIMIT = 10**9
EXPECTED_ANSWER = 0

reversible_count = 0

reversible_dict = {}

for n in xrange(1, LIMIT + 1):
    if n % 10**6 == 0:
        # print progress
        print n
    if is_reversible(n):
        reversible_count += 1

answer = reversible_count

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
