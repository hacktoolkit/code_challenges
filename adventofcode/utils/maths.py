# Python Standard Library Imports
import math
from functools import (
    lru_cache,
    reduce,
)
from operator import mul


def list_product(num_list):
    return reduce(mul, num_list, 1)


@lru_cache
def gcd(a, b):
    """Greatest common divisor

    https://en.wikipedia.org/wiki/Euclidean_algorithm
    """
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a


PRIMES = [2, 3]


def generate_primes(n):
    """Generates a list of prime numbers up to `n`"""
    global PRIMES

    k = PRIMES[-1] + 2
    while k <= n:
        primes_so_far = PRIMES[:]
        divisible = False

        for p in primes_so_far:
            if k % p == 0:
                divisible = True
                break

        if not divisible:
            PRIMES.append(k)

        k += 2

    return PRIMES


FACTORS_MEMO = {}


def factors_of(n):
    """Return of the factors of `n`

    Returns a list of numbers evenly dividing `n`, including 1 and itself
    """
    global FACTORS_MEMO

    if n in FACTORS_MEMO:
        factors = FACTORS_MEMO[n]
    else:
        factors = {1, n}
        for k in range(2, n // 2 + 1):
            if k in factors:
                # already a known number, does not need to be re-tested
                pass
            elif n % k == 0:
                if k in FACTORS_MEMO:
                    # a number we've already factored previously
                    # add those factors to speed things up
                    factors |= factors_of(k)
                else:
                    factors.add(k)
                    # when discovering a factor, also add factors of the quotient, to speed things up
                    quotient = n // k
                    factors |= factors_of(quotient)
            else:
                # not a factor, continue
                pass

        FACTORS_MEMO[n] = factors

    return factors


def lcm(num_list):
    """Finds the lcm of a list of numbers

    http://en.wikipedia.org/wiki/Least_common_multiple

    This algorithm uses a table
    http://en.wikipedia.org/wiki/Least_common_multiple#A_method_using_a_table

    We don't actually need the previous columns of the table, just the most recent,
    so an array is sufficient
    """
    largest_num = max(num_list)
    primes = generate_primes(largest_num)
    factors = []
    for prime in primes:
        divides = True
        while divides:
            divides = False
            for i in range(len(num_list)):
                n = num_list[i]
                if n % prime == 0:
                    n /= prime
                    num_list[i] = n
                    divides = True
            if divides:
                factors.append(prime)
    result = list_product(factors)
    return result


def gauss_sum(a, b):
    """Sums a sequence of integers from `a` to `b`

    - https://everything2.com/title/Gaussian+formula
    - https://en.wikipedia.org/wiki/Gaussian_function
    - https://en.wikipedia.org/wiki/Gauss_sum
    """
    return ((a + b) * (b - a + 1)) / 2
