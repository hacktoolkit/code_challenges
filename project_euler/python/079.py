"""http://projecteuler.net/problem=079

Passcode derivation

A common security method used for online banking is to ask the user for three random characters from a passcode. For example, if the passcode was 531278, they may ask for the 2nd, 3rd, and 5th characters; the expected reply would be: 317.
The text file, [keylog.txt](p079_keylog.txt), contains fifty successful login attempts.
Given that the three characters are always asked for in order, analyse the file so as to determine the shortest possible secret passcode of unknown length.

Solution by jontsai <hello@jontsai.com>
"""
import itertools

from utils import *

EXPECTED_ANSWER = 73162890

def compress_passcode(passcode, lookahead=0):
    """Compresses a passcode by replacing repeated subsequences with just one occurence

    Note: This function is no longer relevant, as I initially interpreted the problem to mean that the three characters were in _consecutive_ order.
    """
    did_replace = True
    while did_replace:
        did_replace = False
        for i in xrange(lookahead, 0, -1):
            for j in xrange(len(passcode) - i - i):
                a_start = j
                a_end = j + i
                b_start = a_end
                b_end = b_start + i
                a, b = passcode[a_start:a_end], passcode[b_start:b_end]
                if a == b:
                    passcode = passcode[:a_end] + passcode[b_end:]
                    did_replace = True
                    break
                else:
                    pass
    return passcode

def get_login_sequences():
    f = open('p079_keylog.txt', 'r')
    logins = sorted(list(set([line.strip() for line in f.readlines()])))
    return logins

def solve_incorrectly():
    """
    Note: This function is no longer relevant, as I initially interpreted the problem to mean that the three characters were in _consecutive_ order.
    """
    logins = get_login_sequences()
    sequence_length = len(logins[0])
    best_so_far = None
    count = 0
    for permutation in itertools.permutations(sequences):
        count += 1
        print 'Checking permutation %s' % count
        passcode = ''.join(permutation)
        if best_so_far is None:
            best_so_far = passcode
            print 'Best so far: %s, %s' % (len(best_so_far), best_so_far,)
        compressed = compress_passcode(passcode, lookahead=sequence_length - 1)
        if len(compressed) < len(best_so_far):
            best_so_far = compressed
            print 'Best so far: %s, %s <- %s' % (len(best_so_far), best_so_far, passcode,)
    answer = best_so_far
    return answer

def solve():
    """
    $ time python 079.py
    [('7', 0), ('3', 1), ('1', 2), ('6', 3), ('2', 4), ('8', 5), ('9', 6), ('0', 7)]
    Expected: 73162890, Answer: 73162890

    real0m0.030s
    user0m0.015s
    sys0m0.011s
    """
    logins = get_login_sequences()
    # build a precedes table
    precedes = {}
    for login in logins:
        preceding_chars = set()
        for c in login:
            if c not in precedes:
                precedes[c] = set()
            precedes[c] = precedes[c].union(preceding_chars)
            preceding_chars.add(c)
    char_precedence_frequency = sorted([(k, len(precedes[k]),) for k in precedes.iterkeys()], key=lambda x: x[1])
    print char_precedence_frequency
    answer = ''.join([c[0] for c in char_precedence_frequency])
    return answer

answer = solve()

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
