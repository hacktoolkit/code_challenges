"""https://projecteuler.net/problem=625

Gcd sum

$G(N)=\sum_{j=1}^N\sum_{i=1}^j \text{gcd}(i,j)$. 
You are given: $G(10)=122$.

Find $G(10^{11})$. Give your answer modulo 998244353

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

EXPECTED_ANSWER = 0

MEMO = {}
def memoized_gcd(i, j):
    key = '_'.join([str(k) for k in sorted([i, j])])
    if key in MEMO:
        result = MEMO[key]
    else:
        result = gcd(i, j)
        MEMO[key] = result
    return result

def G(N):
    total = 0
    for j in xrange(1, N + 1):
        for i in xrange(1, j + 1):
            total += memoized_gcd(i, j)
    constant = 998244353
    total = total % constant
    return total

def solve(target):
    answer = None
    answer = G(target)
    return answer

def main():
    #target = 10
    target = 10**11
    answer = solve(target)

    print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)

if __name__ == '__main__':
    main()
