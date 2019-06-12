"""http://projecteuler.net/problem=493

Under The Rainbow

70 colored balls are placed in an urn, 10 for each of the seven rainbow colors.
What is the expected number of distinct colors in 20 randomly picked balls?
Give your answer with nine digits after the decimal point (a.bcdefghij).

Solution by jontsai <hello@jontsai.com>
"""
import itertools

from utils import *

EXPECTED_ANSWER = 0

#COLORS = [c for c in 'ROYGBIV']
#BALLS = list(itertools.chain.from_iterable([c * 10 for c in COLORS]))

# Ball 1: 1.0 possibility to be distinct color
# 

def solve(num_picks):
    answer = None

    total_balls = 70
    balls_picked = 1
    expected_num_distinct_colors = 1
    for k in xrange(balls_picked, num_picks):
        remaining_balls = total_balls - balls_picked
        remaining_balls_with_same_colors = (10 * expected_num_distinct_colors) - (balls_picked * expected_num_distinct_colors)
        p_pick_ball_same_color = 1.0 * remaining_balls_with_same_colors / remaining_balls
        p_pick_ball_diff_color = 1 - p_pick_ball_same_color
        expected_num_distinct_colors += p_pick_ball_diff_color

    answer = expected_num_distinct_colors
    return answer

def main():
    target = 20
    for x in xrange(1, target + 1):
        answer = solve(x)
        print x, answer

    print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)

if __name__ == '__main__':
    main()
