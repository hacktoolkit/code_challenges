# Python Standard Library Imports
from collections import namedtuple
from operator import mul


def main():
    answer = solve()
    print(answer)


class Slope(namedtuple('Slope', 'x,y')):
    pass


def solve():
    # input = '3.test.in'
    input_file = '3.in'
    with open(input_file, 'r') as f:
        hill = [line.strip() for line in f.readlines()]

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
