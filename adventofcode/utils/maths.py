# Python Standard Library Imports
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


PRIMES = [2, 3,]


def generate_primes(n):
    """Generates a list of prime numbers up to `n`
    """
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
