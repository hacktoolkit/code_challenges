"""http://projecteuler.net/problem=079

Passcode derivation

A common security method used for online banking is to ask the user for three random characters from a passcode. For example, if the passcode was 531278, they may ask for the 2nd, 3rd, and 5th characters; the expected reply would be: 317.
The text file, [keylog.txt](p079_keylog.txt), contains fifty successful login attempts.
Given that the three characters are always asked for in order, analyse the file so as to determine the shortest possible secret passcode of unknown length.

Solution by jontsai <hello@jontsai.com>
"""
import itertools

from utils import *

EXPECTED_ANSWER = 0

def compress_passcode(passcode, lookahead=0):
    """Compresses a passcode by replacing repeated subsequences with just one occurence
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

def solve():
    f = open('p079_keylog.txt', 'r')
    sequences = sorted(list(set([line.strip() for line in f.readlines()])))
    sequence_length = len(sequences[0])
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

answer = solve()

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
