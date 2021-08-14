# coding=utf-8

# Python Standard Library Imports
import itertools
import math
import operator

# PE Solution Library Imports
from constants import *


def is_odd(n):
    """Determines whether `n` is odd
    """
    # odd = n % 2 == 1
    odd = bool(n & 1)
    return odd


def is_even(n):
    """Determines whether `n` is even
    """
    # even = n % 2 == 0
    even = not(n & 1)
    return even


def gcd_euclidean(a, b):
    """Efficiently finds the gcd of two integers

    Uses Euclidean algorithm

    http://en.wikipedia.org/wiki/Greatest_common_divisor
    http://en.wikipedia.org/wiki/Euclidean_algorithm
    """
    if a == 0:
        return b
    if b == 0:
        return a
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a


def gcd_modulo(a, b):
    while b:
        a, b = b, a % b
    return a


def gcd(a, b):
    return gcd_modulo(a, b)
    return result


def is_coprime(a, b):
    """Determines whether `a` and `b` are relatively prime to each other
    """
    result = gcd(a, b) == 1
    return result

def is_relatively_prime(a, b):
    return is_coprime(a, b)


PHI_MEMO = {}
def phi(n, memoize=False):
    """Euler's Totient function

    https://en.wikipedia.org/wiki/Euler's_totient_function

    Test cases:
    - 069
    """
    global PHI_MEMO

    if memoize and n in PHI_MEMO:
        result = PHI_MEMO[n]
    else:
        # result = phi_naive(n)
        # result = phi_eulers_product(n)
        result = phi_eulers_product_with_factorization(n, memoize=memoize)
        if memoize:
            PHI_MEMO[n] = result

    return result


def phi_naive(n):
    """Naive implementation of Euler's Totient function

    https://en.wikipedia.org/wiki/Euler's_totient_function

    Test cases:
    - 069 (basic)
    """
    # 1 is always relatively prime to `n`
    num_relative_primes = 1
    for k in range(2, n):
        if is_relatively_prime(n, k):
            num_relative_primes += 1

    return num_relative_primes


def phi_eulers_product(n):
    """Euler's Totient function using Euler's product formula

    https://en.wikipedia.org/wiki/Euler's_totient_function

    Euler's product formula states:

        φ(n) = n * Π(p|n) (1 - 1/p)

    Test cases:
    - 069
    """
    primes_up_to_n = generate_primes(n)
    # TODO: optimize
    primes_dividing_n = filter(lambda p: n % p == 0, primes_up_to_n)

    result = n * product_sequence(primes_dividing_n, lambda p: (1 - 1.0 / p))
    return result


def phi_eulers_product_with_factorization(n, memoize=False):
    """Euler's Totient function using Euler's product formula with factorization

    Test cases:
    - 069
    """
    global PHI_MEMO

    if memoize and n in PHI_MEMO:
        result = PHI_MEMO[n]
    else:
        if is_prime(n):
            distinct_factors = [n,]
        else:
            # TODO: optimize
            # distinct_factors = factor(n, distinct=True)
            distinct_factors = distinct_factors_memoized(n)

        result = n * product_sequence(distinct_factors, lambda p: (1 - 1.0 / p))
        if memoize:
            PHI_MEMO[n] = result

    return result


def reduce_fraction(numerator, denominator):
    """Reduces a fraction to its lowest terms
    """
    _gcd = gcd(numerator, denominator)
    reduced = (numerator / _gcd, denominator / _gcd,)
    return reduced


def power(x, n):
    """Computes x^n fast by using the squaring method

    https://en.wikipedia.org/wiki/Exponentiation_by_squaring

    Test cases:
    - 099
    """
    result = 1
    while n != 0:
        if is_odd(n):
            result *= x
            n -= 1
        x *= x
        n /= 2

    return result


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


FIB_MEMO = [1, 1]
def fibonacci(n):
    """Get the `n`th Fibonacci number

    `n` is zero-based
    The sequence starts with [1, 1, ...]
    """
    if n < len(FIB_MEMO):
        answer = FIB_MEMO[n]
    else:
        answer = fibonacci(n - 1) + fibonacci(n - 2)
        FIB_MEMO.append(answer)
    return answer


def fib_up_to(n, repeat_1=False):
    """Fibonacci numbers up to `n` (inclusive)
    """
    k = 1
    while fibonacci(k) <= n:
        k += 1
    start = 0 if repeat_1 else 1
    end = k
    numbers = FIB_MEMO[start:end]
    return numbers


CUBE_ROOTS = { 1: 1, }
LARGEST_CUBE_GENERATED = 1
def generate_cubes(n):
    """Generate cubes for 1, ..., n

    Test cases:
    - 062
    """
    global CUBE_ROOTS
    global LARGEST_CUBE_GENERATED
    for z in range(len(CUBE_ROOTS) + 1, n + 1):
        CUBE_ROOTS[z**3] = z
    LARGEST_CUBE_GENERATED = max(LARGEST_CUBE_GENERATED, (n + 1) ** 3)
    return CUBE_ROOTS


GENERATE_CUBES_BATCH_SIZE = 100000
def get_perfect_cubic_root(n):
    """Gets the cubic root of a perfect cube
    """
    global CUBE_ROOTS
    global LARGEST_CUBE_GENERATED
    while LARGEST_CUBE_GENERATED < n:
        cubes = generate_cubes(len(CUBE_ROOTS) + GENERATE_CUBES_BATCH_SIZE)
    cubic_root = CUBE_ROOTS.get(n, None)
    return cubic_root


def is_perfect_cube(n):
    """Determines whether a number is a perfect cube

    Test cases:
    - 062
    """
    cubic_root = get_perfect_cubic_root(n)
    is_cube = cubic_root is not None
    return is_cube


def nth_root(number, n):
    """Gets the integral nth-root

    Test cases:
    - 063
    """
    nth_root = int(round(pow(number, 1.0 / n)))
    if nth_root ** n != number:
        nth_root = None
    return nth_root


def quadratic(a, b, c):
    """Solves the quadratic equation
    ax^2 + b + c = 0
    (-b + sqrt(b^2 - 4ac)) / 2a
    """
    x = (math.sqrt((b * b) - (4 * a * c)) - b) / (2 * a)
    return x


def triangle_number(n):
    """Get the nth triangle number

    1: 1 = 1
    2: 1 + 2 = 3
    3: 1 + 2 + 3 = 6
    4: 1 + 2 + 3 + 4 = 10

    Test cases:
    - 012
    """
    triangle = (n * (n + 1)) / 2
    return triangle


def is_triangle_num(n):
    """Determines if n is a triangle number

    The nth term of the sequence of triangle numbers is given by, tn = 0.5n(n+1)

    n^2 + n - 2tn = 0

    Tries to solve the quadratic formula:
    (-b + sqrt(b^2 - 4ac)) / 2a
    Where:
    a = 1
    b = 1
    c = -2(tn)

    This becomes (-1 + sqrt(1 - 4 * -2 * tn)) / 2

    Test cases:
    - 042
    - 045
    """
    x = quadratic(1, 1, -2 * n)
    is_triangle = int(x) == x # x is a whole number
    return is_triangle


def pentagon_number(n):
    """Get the nth pentagon number

    Pn = n * (3 * n - 1) / 2

    Test cases:
    - 044
    """
    pentagon = (n * (3 * n - 1)) / 2
    return pentagon


def is_pentagon_num(n):
    """Determines if n is a pentagon number

    Pn = n(3n - 1)/2

    Quadratic: 3n^2 - n - 2Pn = 0
    a = 3
    b = -1
    c = -2(Pn)

    Test cases:
    - 045
    """
    x = quadratic(3, -1, -2 * n)
    is_pentagon = int(x) == x # x is a whole number
    return is_pentagon


def hexagon_number(n):
    """Get the nth hexagon number

    Hn=n(2n-1)

    Test cases:
    - 045
    """
    hexagon = n * (2 * n - 1)
    return hexagon


def is_hexagon_num(n):
    """Determines if n is a hexagon number

    Hn=n(2n-1)

    Quadratic: 2n^2 - n - Hn = 0
    a = 2
    b = -1
    c = -Hn

    Test cases:
    - 045
    """
    x = quadratic(2, -1, -n)
    is_hexagon = int(x) == x # x is a whole number
    return is_hexagon


DIGISUM_MEMO = [None] * 200
def digisum(a, b, carry):
    """A method for quickly computing the some of two integers and a carry bit

    Results are memoized for fast lookup
    """
    index = carry * 100 + a * 10 + b

    memoized_result = DIGISUM_MEMO[index]
    if memoized_result is None:
        # calculate value for first time
        result = a + b + carry
        DIGISUM_MEMO[index] = result
    else:
        # previously memoized
        result = memoized_result
    return result


def leading_digit(n):
    """Returns the leading digit of `n`
    """
    # str manipulation is slow
    #first_digit = int(str(n)[0])
    shifted = n / 10
    while shifted > 0:
        n = shifted
        shifted /= 10
    first_digit = n

    return first_digit


def trailing_digit(n):
    """Returns the trailing digit of `n`
    """
    last_digit = n % 10
    return last_digit


def reversed_int(n):
    """Returns an integer with the digits in `n` reversed
    """
    #reversed_n = _reversed_int_str(n)
    reversed_n = _reversed_int_fast(n)
    return reversed_n


def _reversed_int_str(n):
    """Returns an integer with the digits in `n` reversed

    It converts to string, and then back to integer.

    This is just a reference implementation, but in practice _reversed_int_fast should be used instead
    """
    digits_n_str = digits(n, string=True)
    reversed_n = int(''.join(digits_n_str[::-1]))
    return reversed_n


def _reversed_int_fast(n):
    """A faster implementation of reversed_int that keeps types as integers
    """
    reversed_n = n % 10
    while n > 0:
        n /= 10
        if n > 0:
            reversed_n *= 10
            reversed_n += n % 10

    return reversed_n


REVERSIBLE_MEMO = {}
def is_reversible(n):
    """Determines if n is a reversible number

    Reversible numbers:
    36 + 63 = 99
    409 + 904 = 1313

    Test cases:
    - 145
    """
    first_digit = leading_digit(n)
    last_digit = trailing_digit(n)
    n2 = reversed_int(n)

    if n in REVERSIBLE_MEMO:
        reversible = REVERSIBLE_MEMO[n]
    elif last_digit == 0:
        # the reversed number would have a leading 0, which is not allowed
        reversible = False
    elif n2 in REVERSIBLE_MEMO:
        reversible = REVERSIBLE_MEMO[n2]
    elif (is_even(first_digit) and is_even(last_digit)) or (is_odd(first_digit) and is_odd(last_digit)):
        # the first and last digit summed would be an even number
        reversible = False
    else:
        def _check_digits_slow():
            # slow method - sum, then check each digit
            _reversible = True

            reversed_sum = n + n2
            for digit in digits(reversed_sum):
                if is_even(digit):
                    _reversible = False
                    break
            return _reversible

        def _check_digits_fast():
            # fast method - sum from right to left, check as we go
            _reversible = True
            a = n
            b = n2

            carry = 0
            while a > 0 and b > 0:
                x = a % 10
                y = b % 10
                digit_sum = digisum(x, y, carry)
                digit = digit_sum % 10
                if is_even(digit):
                    _reversible = False
                    break
                # update for next iteration
                carry = digit_sum / 10
                a /= 10
                b /= 10
            return _reversible

        #reversible = _check_digits_slow()
        reversible = _check_digits_fast()

        # update memo for reverse(n)
        REVERSIBLE_MEMO[n2] = reversible

    # always update memo for `n`
    REVERSIBLE_MEMO[n] = reversible

    return reversible


def collatz_sequence(n):
    """Produces the Collatz sequence for a starting number, n

    n -> n/2 (n is even)
    n -> 3n + 1 (n is odd)
    Terminates when n is 1
    """
    sequence = [n,]
    while n > 1:
        if is_even(n):
            n = n / 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence


COLLATZ_LENGTH_MEMO = { 0 : 0, 1 : 1,}
def collatz_sequence_length(n):
    """Finds the length of the Collatz sequence for a starting number, n
    Does not need to actually calculate or return the sequence
    """
    if n in COLLATZ_LENGTH_MEMO:
        length = COLLATZ_LENGTH_MEMO[n]
    else:
        if is_even(n):
            length = 1 + collatz_sequence_length(n / 2)
        else:
            length = 1 + collatz_sequence_length(3 * n + 1)
        COLLATZ_LENGTH_MEMO[n] = length
    return length


def get_proper_divisors(n):
    """Get proper divisors of n
    Number less than n which divide evenly into n

    Test cases:
    - 021
    - 023
    """
    divisors = get_divisors(n)[:-1]
    return divisors


def sum_proper_divisors(n):
    """Get the sum of the proper divisors of n

    Test cases:
    - 021
    - 023
    """
    value = sum(get_proper_divisors(n))
    return value


def is_perfect_number(n):
    """A perfect number n is a number whose sum of its proper divisors is equal to n
    """
    perfectness = sum_proper_divisors(n) == n
    return perfectness


def is_abundant_number(n):
    """An abundant number n is a number whose sum of its proper divisors exceeds n

    Test cases:
    - 023
    """
    abundance = sum_proper_divisors(n) > n
    return abundance


def get_amicable_pair(n):
    """Get amicable pair for n, if one exists

    An amicable pair (a, b) is such that
    a = sum of proper divisors of n
    b = sum of proper divisors of a
    a = b

    Test cases:
    - 021
    """
    candidate = sum_proper_divisors(n)
    candidate_divisors_sum = sum_proper_divisors(candidate)
    if candidate_divisors_sum == n:
        pair = (n, candidate,)
    else:
        pair = None
    return pair


def get_divisors(n):
    """Get integer divisors of n

    Test cases:
    - 012
    - 179
    """
    divisors = []
    for k in range(1, int(math.sqrt(n)) + 1):
        if n % k == 0:
            quotient = n / k
            divisors.append(k)
            if k != quotient:
                divisors.append(quotient)
    divisors = sorted(divisors)
    return divisors


def get_prime_divisors(n):
    """Get prime numbers that divide evenly into `n`

    Test cases:
    - 069
    """
    primes = generate_primes(n)

    # prime_divisors = filter(lambda p: p <= n and n % p == 0, primes)

    # use a for loop instead of list comprehension in order to break early
    p = None
    prime_divisors = []
    for i in range(len(primes) + 1):
        p = primes[i]
        if n % p == 0:
            prime_divisors.append(p)
        if p * p > n:
            break

    if n in primes:
        prime_divisors.append(n)

    return prime_divisors


FACT_MEMO = [1, 1]
def factorial(n):
    """Computes n!
    """
    if n < len(FACT_MEMO):
        value = FACT_MEMO[n]
    else:
        value = n * factorial(n-1)
        FACT_MEMO.append(value)
    return value


PRIME_MEMO_TRIAL_DIVISION = []
def generate_primes_trial_division(n):
    """Generate prime numbers up to `n`

    Uses trial division
    """
    if len(PRIME_MEMO_TRIAL_DIVISION) and PRIME_MEMO_TRIAL_DIVISION[-1] > n:
        return
    for x in range(2, n + 1):
        if is_prime_trial_division(x):
            PRIME_MEMO_TRIAL_DIVISION.append(x)
        else:
            pass


def is_prime_trial_division(n):
    """Determines whether `n` is a prime number

    Prerequisite: generate_primes_trial_division(math.sqrt(n))  called
    """
    primeness = True
    limit = math.sqrt(n)
    for prime in PRIME_MEMO_TRIAL_DIVISION:
        if prime > limit:
            break
        elif n % prime == 0:
            primeness = False
    # n must be prime if no divisors found yet
    if primeness:
        PRIME_MEMO_TRIAL_DIVISION.append(n)
    return primeness


# seed with basic primes
PRIMES = [2, 3]
PRIME_MEMO = { 2 : True, 3 : True }
PRIMES_BATCH_SIZE = 10000000 # look at 10M numbers at a time
PRIMES_GENERATED_UP_TO = 0
def generate_primes(n):
    """Generates a list of prime numbers
    Uses the sieve of Eratosthenes

    Optimizations:
    - after 2, all other primes must be odd
    - use range instead of range to save on memory
    - extend PRIME_MEMO by a constant factor, in batches

    Test cases:
    - 007
    - 010
    - 037
    - 041
    """
    global PRIMES
    global PRIME_MEMO
    global PRIMES_GENERATED_UP_TO
    PRIMES_GENERATED_UP_TO = max(PRIMES_GENERATED_UP_TO, n)
    greatest_prime_so_far = PRIMES[-1]
    lower = greatest_prime_so_far + 2
    upper = min(lower + PRIMES_BATCH_SIZE, n)
    while lower <= upper <= n:
        # generate the next batch of numbers to sieve
        # always increment by 2, since primes cannot be even
        num_range = range(lower, upper + 1, 2)
        local_memo = dict(zip(num_range, [True] * len(num_range)))

        # mark off the composite numbers, sieve style
        for k in PRIMES:
            # k is a prime number
            # mark every kth number following k as composite
            for x in range(k + k, upper + 1, k):
                if x in local_memo:
                    # just delete instead of marking False to save memory
                    del local_memo[x]

        # make a copy of keys, since we are modifying the underlying dict
        for k in sorted(local_memo.keys()):
            if k in local_memo:
                # k is a prime
                for x in range(k + k, upper + 1, k):
                    if x in local_memo:
                        del local_memo[x]
            else:
                # k is already marked as composite, do nothing
                pass

        lower = min(upper + 2, n + 1)
        upper = min(upper + PRIMES_BATCH_SIZE, n + 1)

        PRIME_MEMO.update(local_memo)
        for k in sorted(local_memo.keys()):
            PRIMES.append(k)

    return PRIMES


def is_prime(n):
    """Determines whether n is a prime number

    Requires generate_primes(n) called before

    Test cases:
    - 007
    - 010
    - 037
    - 041
    """
    global PRIME_MEMO
    global PRIMES_GENERATED_UP_TO
    if not PRIME_MEMO or PRIMES_GENERATED_UP_TO < n:
        primes = generate_primes(n)
    else:
        primes = PRIMES
    primeness = n in primes
    return primeness


def primality(n):
    """A basic primality test

    http://en.wikipedia.org/wiki/Primality_test
    """
    if n < 0:
        primeness = False
    elif n <= 3:
        if n <= 1:
            primeness = False
        else:
            primeness = True
    elif not(n % 2) or not(n % 3):
        primeness = False
    else:
        primeness = True
        for i in range(5, int(n ** 0.5) + 1, 6):
            if not n % i or not n % (i + 2):
                primeness = False
                break
    return primeness


def possibly_prime(n):
    """Determines whether n is possibly a prime number

    Cannot be even
    Not divible by 3 (sum of digits cannot be divisible by 3)
    """
    possible = not is_even(n) and n % 3 > 0
    return possible


def get_truncations(s, dir='all'):
    """Get truncations

    `dir` direction of truncation

    E.g. 'asdf' => ['sdf', 'df', 'f'] (ltr)
         'asdf' => ['asd', 'as', 'a'] (rtl)
    """
    truncations = []
    for i in range(1, len(s)):
        if dir in ('ltr', 'all',):
            truncations.append(s[i:])
        if dir in ('rtl', 'all',):
            truncations.append(s[:-i])
    return truncations


def is_truncatable_prime(n):
    """A truncatable prime is a prime number that, when continuously removing digits from the left to right or right to left, the subsequent numbers are also prime

    23 is the lowest truncatable prime that has an even digit

    Test cases:
    - 037
    """
    truncatable = False
    if is_prime(n) and (n == 23 or (n > 23 and not has_even_digits(n))):
        truncations = [int(truncation) for truncation in get_truncations(str(n))]
        if truncations:
            truncatable = True
            for truncation in truncations:
                if not is_prime(truncation):
                    truncatable = False
                    break
                else:
                    pass
    else:
        pass
    return truncatable


def factor(n, distinct=False):
    """Get the factors of `n`

    E.g. numbers that evenly divide `n`

    Returns the prime factorization of n

    Test cases:
    - 003
    - 047
    - 069
    """
    limit = int(math.sqrt(n))
    primes = filter(lambda p: p <= n, generate_primes(limit))
    divisors = []
    reduced = n

    prev_prime = None
    for prime in primes[::-1]:
        while reduced % prime == 0:
            reduced /= prime
            if distinct:
                # set sentinel value
                if prime != prev_prime:
                    divisors.append(prime)
                    prev_prime = prime
            else:
                divisors.append(prime)

    if reduced != 1:
        divisors.append(reduced)

    return divisors


DISTINCT_FACTORS_MEMO = {}
def distinct_factors_memoized(n):
    """
    """
    global DISTINCT_FACTORS_MEMO

    if n in DISTINCT_FACTORS_MEMO:
        divisors = DISTINCT_FACTORS_MEMO[n]
    else:
        divisors = []

        limit = int(math.sqrt(n))
        primes = filter(lambda p: p <= n, generate_primes(limit))

        reduced = n

        for prime in primes[::-1]:
            is_divisible = reduced % prime == 0

            if is_divisible:
                divisors.append(prime)

                while is_divisible:
                    reduced /= prime
                    is_divisible = reduced % prime == 0

                if reduced in DISTINCT_FACTORS_MEMO:
                    divisors += DISTINCT_FACTORS_MEMO[reduced]
                    break

        DISTINCT_FACTORS_MEMO[n] = divisors

    return divisors


def is_palindromic(n):
    """Determines whether a number or a string is palindromic

    Test cases:
    - 036
    """
    palindromic = str(n) == str(n)[::-1]
    return palindromic


def is_lychrel_number(n, iterations=50):
    """Determines if a number is a Lychrel number within `iterations`
    """
    _summation = n
    found_palindrome = False
    count = 0
    while not found_palindrome and count < iterations:
        reversed_digits = int(''.join(reversed(digits(_summation, string=True))))
        _summation += reversed_digits
        if is_palindromic(str(_summation)):
            found_palindrome = True
            break
        else:
            count += 1
    is_lychrel = not(found_palindrome)
    return is_lychrel


def range_sum(lower, upper):
    """Find the sum of a range of numbers
    """
    # sum(range(lower, upper + 1))
    total = (upper + lower) * (upper - lower + 1) / 2
    return total


def list_product(num_list):
    """Multiplies all of the numbers in a list
    """
    product = 1
    for x in num_list:
        product *= x
    return product


def count_digits(n):
    """Counts the number of digits in `n`

    Test cases:
    - 057
    """
    if n == 0:
        return 1

    num_digits = 0
    while n > 0:
        num_digits += 1
        n /= 10
    return num_digits


def log_num_digits(n):
    """Gets the number of digits in `n`

    Utilizes log base 10

    Test cases:
    - 063
    """
    if n / 10 == 0:
        num_digits = 1
    else:
        num_digits = int(math.ceil(math.log(n, 10)))
    return num_digits


def digits(n, string=False):
    """Get the digits of a number as a list of numbers

    `string` if True, return a list of strings
    """
    if string:
        list_of_digits = [digit for digit in str(n)]
    else:
        list_of_digits = [int(digit) for digit in str(n)]
    return list_of_digits


def str_to_digits(s):
    """Get a list of digits from a numeric string or numeric list
    """
    digits = [int(digit) for digit in s]
    return digits


def sum_digits(n):
    """Find the sum of the digits of n

    Test cases:
    - 056
    """
    digits_n = digits(n)
    result = sum(digits_n)
    return result


def has_even_digits(n):
    even_digits = filter(is_even, digits(n))
    has_even = len(even_digits) > 0
    return has_even


def number_to_words(n):
    words = ''
    # thousands
    if n >= 1000:
        quotient = n / 1000
        words += NUM_WORDS[quotient] + ' ' + NUM_WORDS[1000]
        n -= quotient * 1000

    # hundredths
    if n >= 100:
        quotient = n / 100
        words += NUM_WORDS[quotient] + ' ' + NUM_WORDS[100]
        n -= quotient * 100
        if n > 0:
            words += ' and '

    # tens
    if n >= 20:
        quotient = n / 10
        words += NUM_WORDS[quotient * 10]
        n -= quotient * 10
        if n > 0:
            words += '-'
    elif n >= 10:
        words += NUM_WORDS[n]
        n -= n

    # ones
    if n > 0:
        words += NUM_WORDS[n]
    return words


def letter_score(letter):
    """Gets the value of a letter

    E.g. A = 1, B = 2, C = 3, ..., Z = 26
    """
    letter = letter.upper()
    score = ord(letter) - ord('A') + 1
    return score


def word_score(word):
    """Computes the sum of the alphabetical value of each character

    Test cases:
    - 042
    """
    letter_scores = [letter_score(letter) for letter in word]
    score = sum(letter_scores)
    return score


def word_number(word):
    """Converts a word to a number
    """
    pass


def is_pandigital(n):
    """An n-digit number is pandigital if it makes use of all the digits 1 to n exactly once

    E.g. 2143 is a 4-digit pandigital (and is also a prime)

    Test cases:
    - 038
    - 041
    """
    digits_n = digits(n)
    pandigitalness = len(digits_n) == max(digits_n) == len(set(digits_n)) and min(digits_n) == 1
    return pandigitalness


def rotations(s):
    """Get all the rotations of a string
    E.g.
    'abc' => ['abc', 'bca', 'cba']
    """
    all_rotations = []
    for i in range(len(s)):
        rotation = s[i:] + s[:i]
        all_rotations.append(rotation)
    return all_rotations


def is_circular_prime(n):
    """Determines if n is a circular prime

    It is a circular prime if all rotations of n are also prime

    E.g. 197 => 197, 971, 719

    Test cases:
    - 035
    """
    rotations_of_n = [int(rotation) for rotation in rotations(str(n))]
    circular_primeness = is_prime(n) and len(filter(is_prime, rotations_of_n)) == len(rotations_of_n)
    return circular_primeness


# DEPRECATED in favor of using itertools.permutations
def permutations_deprecated(s):
    """Get all the permutations of a string, i.e. anagrams

    E.g.
    'abc' => ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
    """
    if len(s) == 0:
        all_permutations = []
    elif len(s) == 1:
        all_permutations = [s]
    else:
        all_permutations = []
        string = ''.join(sorted([c for c in s]))
        for i in range(len(string)):
            c = string[i]
            substring = string[:i] + string[i + 1:]
            sub_permutations = [c + sub_permutation for sub_permutation in permutations(substring)]
            all_permutations += sub_permutations
    return list(set(all_permutations))


def permutations(s):
    for p in itertools.permutations(s):
        yield ''.join(p)


def numeric_permutations(n):
    """Find the permutations of a number n

    Test cases:
    - 049
    - 062
    """
    n_str = str(n)
    n_str_len = len(n_str)

    permutations_of_n = sorted(set([
        int(permutation)
        for permutation
        in permutations(n_str)
        # filter out numbers with leading zeroes
        if len(str(int(permutation))) == n_str_len
    ]))

    # for p in permutations(n_str):
    #     p_int = int(p)
    #     if len(str(p_int)) == n_str_len:
    #         yield int(p)

    return permutations_of_n


def prime_permutations(n):
    """Find all permutations of the digits of the numbers in n that are primes

    Test cases:
    - 049
    """
    permutations_of_n = numeric_permutations(n)
    prime_permutations_of_n = filter(is_prime, permutations_of_n)
    return prime_permutations_of_n


def summation(series, f):
    """Calculations the summation of a `series` with function `f`

    aka "Capital-sigma notation"

    Σ(f(n)) = f(k0) + f(k1) + f(k2) + ... + f(kn)

    https://en.wikipedia.org/wiki/Summation#Capital-sigma_notation
    https://en.wikipedia.org/wiki/Arithmetic_function#Notation
    """
    values = (f(value) for value in series)
    result = sum(values)
    return result


def product_sequence(series, f):
    """Calculates the product sequence of a `series` of numbers

    aka "Capital-pi notation"

    Π(f(n)) = f(k0) * f(k1) * f(k2) * ... * f(kn)

    https://en.wikipedia.org/wiki/Arithmetic_function#Notation
    """
    values = (f(value) for value in series)
    result = reduce(operator.mul, values)
    return result


def arithmetic_series_subset(num_list):
    """Given a list of numbers in increasing order, return the subset of numbers that are in an arithmetic series

    An arithmetic series must have at least 3 items

    Returns the first subset found, not necessarily the longest subset

    Test cases:
    - 049
    """
    if len(num_list) < 3:
        subset = []
    else:
        subset = []
        for i in range(len(num_list)):
            # find the difference between every pair
            for j in range(i + 1, len(num_list)):
                n1 = num_list[i]
                n2 = num_list[j]
                difference = n2 - n1
                n3 = n2 + difference
                if n3 in num_list:
                    subset = [n1, n2, n3]
                    break
    return subset


ROMAN_NUMERALS = {
    # core Roman numerals
    1000 : 'M',
    500  : 'D',
    100  : 'C',
    50   : 'L',
    10   : 'X',
    5    : 'V',
    1    : 'I',
    # special cases
    900  : 'CM',
    400  : 'CD',
    90   : 'XC',
    40   : 'XL',
    9    : 'IX',
    4    : 'IV',
}

ROMAN_VALUES = sorted(ROMAN_NUMERALS.keys(), reverse=True)

ROMAN_NUMERAL_VALUES = dict([(roman_numeral, value,) for (value, roman_numeral,) in ROMAN_NUMERALS.items()])


def roman(n):
    """Find the Roman numeral string representing `n`

    Algorithm depends on a pre-constructed list of roman values in descending order

    Greedy, so will find the optimal string
    """
    roman_str = ''
    index = 0
    while n > 0 and index < len(ROMAN_VALUES):
        roman_value = ROMAN_VALUES[index]
        roman_numeral = ROMAN_NUMERALS[roman_value]
        if roman_value <= n:
            n -= roman_value
            roman_str += roman_numeral
        else:
            index += 1
    return roman_str


def roman_value(roman_str):
    """Given a Roman numeral string, find its value
    """
    index = 0
    total = 0
    while index < len(roman_str):
        numeral = roman_str[index]
        value = ROMAN_NUMERAL_VALUES.get(numeral, 0)
        if index + 1 < len(roman_str):
            # determine whether the next two form a subtractive pair
            next_numeral = roman_str[index + 1]
            next_value = ROMAN_NUMERAL_VALUES.get(next_numeral, 0)
            if next_value > value:
                # look at the subtractive pair
                numeral = roman_str[index:index + 2]
                value = ROMAN_NUMERAL_VALUES.get(numeral, 0)
                total += value
                index += 2
            else:
                # not a subtractive pair
                total += value
                index += 1
        else:
            # last numeral
            total += value
            index += 1
    return total
