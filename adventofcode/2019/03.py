# Python Standard Library Imports
import copy
import math
import re
from collections import defaultdict
from dataclasses import dataclass

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '03'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (865, 35038)
# TEST_EXPECTED_ANSWERS = (6, 30)
# TEST_EXPECTED_ANSWERS = (159, 610)  # 03b.test.in
TEST_EXPECTED_ANSWERS = (135, 410)  # 03c.test.in

DEBUGGING = False
DEBUGGING = True


def debug(s):
    if DEBUGGING:
        print(s)
    else:
        pass


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_coordinates=False,
        coordinate_delimeter=None,
        as_table=False,
        row_func=None,
        cell_func=None,
    )

    if TEST_MODE:
        # input_filename = f'{PROBLEM_NUM}.test.in'
        # input_filename = f'{PROBLEM_NUM}b.test.in'
        input_filename = f'{PROBLEM_NUM}c.test.in'
        expected_answers = TEST_EXPECTED_ANSWERS
    else:
        input_filename = f'{PROBLEM_NUM}.in'
        expected_answers = EXPECTED_ANSWERS

    solution = Solution(input_filename, input_config, expected_answers)

    solution.solve()
    solution.report()


class Solution(BaseSolution):
    def process_data(self):
        data = self.data

        self.wiring = Wiring(data)

    def solve1(self):
        (
            closest_intersection,
            closest_distance,
        ) = self.wiring.closest_intersection

        answer = closest_distance
        return answer

    def solve2(self):
        (
            shortest_wired_intersection,
            shortest_wired_intersection_steps,
        ) = self.wiring.shortest_wired_intersection

        answer = shortest_wired_intersection_steps
        return answer


class Wiring:
    DIRECTION_MAP = {
        'U': (0, 1),
        'D': (0, -1),
        'L': (-1, 0),
        'R': (1, 0),
    }

    def __init__(self, wires):
        self.wires = wires

        self._init_grid()

    def _init_grid(self):
        grid = defaultdict(set)
        grid_step_counts = defaultdict(int)

        def _mark_grid(x, y, wire_id, steps=0):
            grid[(x, y)].add(wire_id)
            grid_step_counts[(x, y)] += steps

        for wire_id, wire in enumerate(self.wires):
            x, y = 0, 0
            _mark_grid(x, y, wire_id)

            steps = 0

            for segment in wire.split(','):
                direction, magnitude = segment[0], int(segment[1:])
                dx, dy = self.DIRECTION_MAP[direction]

                for _ in range(magnitude):
                    steps += 1
                    x += dx
                    y += dy
                    _mark_grid(x, y, wire_id, steps)

        self.grid = grid
        self.grid_step_counts = grid_step_counts

    @property
    def intersections(self):
        coords = []
        for coord, wire_ids in self.grid.items():
            if coord == (0, 0) or len(wire_ids) == 1:
                # skip:
                # - origin intersections do not count
                # - this coordinate only has a single wire
                pass
            else:
                # intersection
                coords.append(coord)

        return coords

    @property
    def closest_intersection(self):
        intersections = self.intersections
        debug(f'Intersections: {intersections}')

        closest_intersection = None
        closest_distance = None

        for coord in intersections:
            x, y = coord
            distance = abs(x) + abs(y)
            if closest_intersection is None or distance < closest_distance:
                closest_intersection = coord
                closest_distance = distance

        return closest_intersection, closest_distance

    @property
    def shortest_wired_intersection(self):
        intersections = self.intersections

        shortest_wired_intersection = None
        shortest_wired_intersection_steps = None

        for coord in intersections:
            step_count = self.grid_step_counts[coord]
            if (
                shortest_wired_intersection is None
                or step_count < shortest_wired_intersection_steps
            ):
                shortest_wired_intersection = coord
                shortest_wired_intersection_steps = step_count

        return shortest_wired_intersection, shortest_wired_intersection_steps


if __name__ == '__main__':
    main()
