# Python Standard Library Imports
from collections import defaultdict

from utils import (
    BaseSolution,
    config,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (2565, 2639)

config.INPUT_CONFIG.as_oneline = True


@solution
class Solution(BaseSolution):
    def process_data(self):
        self.directions = self.data
        self.delivery_map = DeliveryMap(self.directions)

    def solve1(self):
        self.delivery_map.run(1)
        answer = self.delivery_map.num_houses_visited
        return answer

    def solve2(self):
        self.delivery_map.run(2)
        answer = self.delivery_map.num_houses_visited
        return answer


class DeliveryMap:
    def __init__(self, directions):
        self.directions = directions

    def run(self, couriers):
        self.m = defaultdict(lambda: defaultdict(int))

        positions = [Position() for x in range(couriers)]

        for i, direction in enumerate(self.directions):
            position = positions[i % len(positions)]
            self.move(direction, position)

    def add_present(self, position):
        self.m[position.x][position.y] += 1

    def move(self, direction, position):
        # add present before move
        self.add_present(position)

        # do move
        position.move(direction)

        # add present after move
        self.add_present(position)

    @property
    def num_houses_visited(self):
        count = 0
        for k in self.m.keys():
            count += len(list(self.m[k].keys()))
        return count


class Position:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, direction):
        if direction == '^':
            self.y += 1
        elif direction == 'v':
            self.y -= 1
        elif direction == '>':
            self.x += 1
        elif direction == '<':
            self.x -= 1
        else:
            raise Exception('Unknown direction: %s' % direction)


if __name__ == '__main__':
    main()
