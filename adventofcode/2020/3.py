# Python Standard Library Imports
import time
from collections import namedtuple


def main():
    answer = solve()
    print(answer)


class Slope(namedtuple('Slope', 'x,y')):
    pass


def solve():
    with open('3.in', 'r') as f:
        hill = [line.strip() for line in f.readlines()]

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


if __name__ == '__main__':
    main()
