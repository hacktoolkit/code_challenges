"""http://projecteuler.net/problem=148

Exploring Pascal's triangle

We can easily verify that none of the entries in the first seven rows of Pascal's triangle are divisible by 7:

1
1 1
1 2 1
1 3 3 1
1 4 6 4 1
1 5 10 10 5 1
1 6 15 20 15 6 1

However, if we check the first one hundred rows, we will find that only 2361 of the 5050 entries are not divisible by 7.

Find the number of entries which are not divisible by 7 in the first one billion (10^9) rows of Pascal's triangle.

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

EXPECTED_ANSWER = 0

def solve(target, divisor=7):
    # this method works pretty fast for 100 rows, but is too slow for 1B rows
    not_divisible_count = 0

    previous_row = []
    for row in xrange(target):
        next_row = []
        previous_row_length = row
        odd_row = is_odd(row + 1)
        # calculate midpoint, the number of items for half symmetry of this row of Pascal's triangle
        if odd_row:
            midpoint = int(row / 2) + 1
        else:
            midpoint = (row + 1) / 2
        for col in xrange(midpoint):
            # just build half of a triangle row
            if col == 0:
                value = 1
                next_row.append(1)
                if row == 0:
                    not_divisible_count += 1
                else:
                    not_divisible_count += 2
            elif col + 1 < midpoint:
                value = previous_row[col] + previous_row[col - 1]
                next_row.append(value)
                if value % divisor > 0:
                    not_divisible_count += 2
            elif col + 1 == midpoint:
                if odd_row:
                    value = previous_row[-1] + previous_row[-1]
                    if value % divisor > 0:
                        not_divisible_count += 1
                else:
                    value = previous_row[-1] + previous_row[-2]
                    if value % divisor > 0:
                        not_divisible_count += 2
                next_row.append(value)
            else:
                pass
        previous_row = next_row

    print previous_row
    return not_divisible_count

def solve2(target, divisor=7):
    # Observations:
    # - in row 8 (1, 7, 21, 35, 35, 21, 7, 1):
    #   - 6 values are divisible by 7
    #   - all (6) values but the ends (1 ... 1) are divisible by 7
    # - in row 9 (1, 8, 28, 56, 70, 56, 28, 8, 1):
    #   - 5 values are divisible by 7
    #   - 4 values (2 on each end) are not divisible by 7
    # - in row 10:
    #   - 4 values are divisible by 7
    #   - 6 values are not divisible by 7
    #
    # ...
    #
    # - in row 15 (1, 14, 91, ...):
    #   - just as in row 8, all values except for the ends are divisible by 7
    #   - subsequent rows will have one less divisible-by-7 per row
    not_divisible_count = 0
    
    for row in xrange(1, target + 1):
        num_values = row
        if row < 8:
            not_divisible_count += num_values
        else:
            level = (row - 1) % 7
            #print row, level
            num_divisible = num_values - 2 * (level + 1)
            not_divisible = num_values - num_divisible
            not_divisible_count += not_divisible

    return not_divisible_count

def main():
    divisor = 7

    target = 22
    #target = 10 ** 2
    #target = 10 ** 9

    for target in xrange(1, 23):
        answer = solve(target, divisor)
        print target, answer
        answer = solve2(target, divisor)
        print target, answer

    print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)

if __name__ == '__main__':
    main()
