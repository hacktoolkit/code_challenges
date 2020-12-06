# Python Standard Library Imports
import time
from collections import namedtuple
from operator import mul

from utils import ingest


INPUT_FILE = '3.in'
EXPECTED_ANSWERS = (195, 3772314000, )

# INPUT_FILE = 'n.test.in'
# EXPECTED_ANSWERS = (None, None, )


def main():
    answers = (solve1(), solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Slope(namedtuple('Slope', 'x,y')):
    pass


def solve1():
    data = ingest(INPUT_FILE)
    hill = data

    m, n = (
        len(hill),  # "height" of hill, rows
        len(hill[0]),  # "width" of hill, columns
    )

    SLOPE = Slope(3, 1)

    num_trees_encountered = 0

    i, j = (0, 0)

    while i < m:
        if hill[i][j] == '#':
            num_trees_encountered += 1

        row = hill[i]

        i += SLOPE.y
        j = (j + SLOPE.x) % n

    answer = num_trees_encountered
    return answer


def solve2():
    data = ingest(INPUT_FILE)
    hill = data

    m, n = (
        len(hill),  # "height" of hill, rows
        len(hill[0]),  # "width" of hill, columns
    )

    slopes = [
        Slope(1, 1),
        Slope(3, 1),
        Slope(5, 1),
        Slope(7, 1),
        Slope(1, 2),
    ]

    def _count_trees(slope):
        num_trees_encountered = 0

        i, j = (0, 0)

        while i < m:
            if hill[i][j] == '#':
                num_trees_encountered += 1

            row = hill[i]

            i += slope.y
            j = (j + slope.x) % n

        return num_trees_encountered

    trees = [_count_trees(slope) for slope in slopes]

    answer = reduce(mul, trees, 1)
    return answer


if __name__ == '__main__':
    main()
