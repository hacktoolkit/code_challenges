# Python Standard Library Imports
import functools
import json

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (4809, 22600)
config.TEST_CASES = {
    '': (13, 140),
}

config.INPUT_CONFIG.as_groups = True


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        self.pairs = [
            Pair(i, json.loads(g[0]), json.loads(g[1]))
            for i, g in enumerate(data, 1)
        ]

    def solve1(self):
        answer = sum([pair.num for pair in self.pairs if pair.is_in_order])
        return answer

    def solve2(self):
        divider_1 = Packet([[2]])
        divider_2 = Packet([[6]])
        packets = [
            _ for pair in self.pairs for _ in (pair.left, pair.right)
        ] + [
            divider_1,
            divider_2,
        ]
        sorted_packets = sorted(packets)

        i = sorted_packets.index(divider_1) + 1
        j = sorted_packets.index(divider_2) + 1
        debug(i, sorted_packets[i].data)
        debug(j, sorted_packets[j].data)

        answer = i * j
        return answer


class Pair:
    def __init__(self, num, left, right):
        self.num = num
        self.left = Packet(left)
        self.right = Packet(right)

    def __str__(self):
        return (
            f'Pair {self.num}:\n{self.left}\n{self.right}\n{self.is_in_order}'
        )

    @property
    def is_in_order(self):
        return self.left < self.right


def cmp(a, b):
    # https://docs.python.org/3.0/whatsnew/3.0.html#ordering-comparisons
    # return (a > b) - (a < b)
    return a.__cmp__(b)


@functools.total_ordering
class Packet:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return f'{self.data}'

    def __cmp__(self, other):
        left, right = self.data, other.data
        if isinstance(left, int) and isinstance(right, int):
            return left - right
        elif isinstance(left, list) and isinstance(right, list):
            # both lists
            for (a, b) in zip(left, right):
                result = cmp(Packet(a), Packet(b))
                if result != 0:
                    return result
            return len(left) - len(right)
        elif isinstance(left, list):
            return cmp(Packet(left), Packet([right]))
        elif isinstance(right, list):
            return cmp(Packet([left]), Packet(right))
        else:
            # impossible case
            raise Exception('Boom!')

    def __lt__(self, other):
        return cmp(self, other) < 0

    def __eq__(self, other):
        return self.data == other.data
        return cmp(self, other) == 0


if __name__ == '__main__':
    main()
