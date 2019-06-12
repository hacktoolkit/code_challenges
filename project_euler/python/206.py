"""http://projecteuler.net/problem=206

Concealed Square

Find the unique positive integer whose square has the form 1_2_3_4_5_6_7_8_9_0, where each "_" is a single digit.

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

EXPECTED_ANSWER = 1389019170

def pattern_match_factory(pattern):
    expected_digits = ''.join(pattern.split('_'))
    def pattern_matcher(n):
        """Determines whether `n` matches the `pattern`,
        e.g. 1_2_3_4_5_6_7_8_9_0
        """
        n_str = str(n)
        value = ''.join([c for c, i in zip(n_str, xrange(len(n_str))) if i % 2 == 0])
        #print 'expected digits', expected_digits,type(expected_digits), 'value', value, type(value)
        result = value == expected_digits
        return result
    return pattern_matcher


def _solve_brute_force1(pattern):
    """Brute force solution
    Very inefficient, takes approx 10 minutes
    """
    answer = None
    pattern_matcher = pattern_match_factory(pattern)

    # the answer lies somewhere between sqrt(min_square) and sqrt(max_square)
    min_square = int('0'.join(pattern.split('_')))
    max_square = int('9'.join(pattern.split('_')))

    lower = int(math.floor(math.sqrt(min_square)))
    upper = int(math.ceil(math.sqrt(max_square)))

    lower = lower - (lower % 10)
    upper = upper - (upper % 10)

    guess = lower
    while guess <= upper:
        square = guess * guess
        #print guess, upper, square
        if pattern_matcher(square):
            answer = guess
            break
        else:
            # optimizations
            # the first digit has to be 0, so advance by 10
            guess += 10

    return answer


def _solve_brute_force2(pattern):
    """Brute force solution

    Since the last 3 digits of the square are `9_0`, the number must end in 30 or 70

    Better than _solve_brute_force1 by factor of 5x (?)
    - 5x increase from only testing 2 numbers per 100, instead of 10 numbers per 100

    real	0m31.459s
    user	0m31.159s
    sys	0m0.023s
    """
    answer = None
    pattern_matcher = pattern_match_factory(pattern)

    # the answer lies somewhere between sqrt(min_square) and sqrt(max_square)
    min_square = int('0'.join(pattern.split('_')))
    max_square = int('9'.join(pattern.split('_')))

    lower = int(math.floor(math.sqrt(min_square)))
    upper = int(math.ceil(math.sqrt(max_square)))

    lower = lower - (lower % 100)
    upper = upper - (upper % 100)

    suffixes = [30, 70,]

    guess_prefix = lower

    while guess_prefix <= upper:
        for suffix in suffixes:
            guess = guess_prefix + suffix
            square = guess * guess
            #print guess, upper, square
            if pattern_matcher(square):
                answer = guess
                break

        # optimizations
        # the last two digits are fixed, so advance by 10
        guess_prefix += 100

    return answer


def _solve_efficiently(pattern):
    """Idea: like picking a lock, solve one level at a time, right to left

    Solve for sub-patterns gradually increasing digits:
    # 9_0
    # 8_9_0
    # 7_8_9_0
    """
    #indices = [x for x in xrange(len(pattern) + 1) if x % 2 == 1]
    #sub_patterns = [pattern[-i:] for i in indices]
    #print sub_patterns
    pass


def solve():
    answer = None
    pattern = '1_2_3_4_5_6_7_8_9_0'

    #answer = _solve_brute_force1(pattern)
    answer = _solve_brute_force2(pattern)
    #answer = _solve_efficiently(pattern)

    return answer


def main():
    answer = solve()
    print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)


if __name__ == '__main__':
    main()
