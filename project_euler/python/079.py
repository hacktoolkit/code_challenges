"""http://projecteuler.net/problem=079

Passcode derivation

A common security method used for online banking is to ask the user for three random characters from a passcode. For example, if the passcode was 531278, they may ask for the 2nd, 3rd, and 5th characters; the expected reply would be: 317.
The text file, [keylog.txt](p079_keylog.txt), contains fifty successful login attempts.
Given that the three characters are always asked for in order, analyse the file so as to determine the shortest possible secret passcode of unknown length.

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

EXPECTED_ANSWER = 0

f = open('p079_keylog.txt', 'r')
passcodes = sorted(list(set([int(line.strip()) for line in f.readlines()])))
print passcodes
# [129, 160, 162, 168, 180, 289, 290, 316, 318, 319, 362, 368, 380, 389, 620, 629, 680, 689, 690, 710, 716, 718, 719, 720, 728, 729, 731, 736, 760, 762, 769, 790, 890]
print len(passcodes)
# 33
[362, 762, 620, 129, 289, 368, 380, 389, 710, 718, 719, 720, 728, 729, 319, 736, 760, 790, 160, 1680, 316, 716]
7690
6890
16290
73180
answer = None

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
