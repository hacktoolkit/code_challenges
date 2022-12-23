# Python Standard Library Imports
import copy
import heapq
import math
import re
import typing as T
from collections import deque
from dataclasses import (
    dataclass,
    field,
)
from itertools import product

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (4052, 978)
config.TEST_CASES = {
    '': (25, 4),
    'b': (110, 20),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        self.grove = Grove(self.data)

    def solve1(self):
        grove = self.grove
        debug(grove.pretty_print())

        for i in range(10):
            did_move = grove.do_round()
            if not did_move:
                break
            if config.DEBUGGING:
                debug(grove.pretty_print())

        answer = grove.bounding_rect_free_space
        return answer

    def solve2(self):
        grove = self.grove
        did_move = True
        while did_move:
            did_move = grove.do_round()

        answer = grove.rounds + 1
        return answer


@dataclass
class Direction:
    label: str
    adj: T.Tuple[int, int]
    checks: list[T.Tuple[int, int]]


DIRECTIONS = [
    Direction('N', (-1, 0), [(-1, 0), (-1, -1), (-1, 1)]),
    Direction('S', (1, 0), [(1, 0), (1, -1), (1, 1)]),
    Direction('W', (0, -1), [(0, -1), (-1, -1), (1, -1)]),
    Direction('E', (0, 1), [(0, 1), (-1, 1), (1, 1)]),
]


class Grove:
    def __init__(self, data):
        self.grid = {}
        self.proposed = None
        self.elves = []

        self.directions = deque(DIRECTIONS)

        for i, row in enumerate(data):
            for j, cell in enumerate(row):
                if cell == '#':
                    elf = Elf(i, j)
                    self.elves.append(elf)
                    self.grid[elf.coords] = elf

        self.rounds = 0

    @property
    def bounding_rect(self):
        min_x, min_y = 0, 0
        max_x, max_y = 0, 0

        for (i, j) in self.grid:
            min_x = min(min_x, j)
            min_y = min(min_y, i)
            max_x = max(max_x, j)
            max_y = max(max_y, i)

        return min_x, min_y, max_x, max_y

    @property
    def bounding_rect_free_space(self):
        min_x, min_y, max_x, max_y = self.bounding_rect

        free_space = 0

        for i in range(min_y, max_y + 1):
            for j in range(min_x, max_x + 1):
                if (i, j) not in self.grid:
                    free_space += 1

        return free_space

    def do_round(self):
        did_move = False
        self.proposed = {}

        for elf in self.elves:
            if self.has_neighbor(elf):
                self.stage_move(elf)

        for coords, elf in self.proposed.items():
            if elf is not None:
                did_move = True
                del self.grid[elf.coords]
                elf.move_to(*coords)
                self.grid[coords] = elf

        self.directions.rotate(-1)
        if did_move:
            self.rounds += 1
        return did_move

    def has_neighbor(self, elf):
        adj = (-1, 0, 1)
        has_neighbor = False
        for dy, dx in product(adj, adj):
            if (dy, dx) != (0, 0):
                coord = elf.row + dy, elf.col + dx
                if coord in self.grid:
                    has_neighbor = True
                    break

        return has_neighbor

    def stage_move(self, elf):
        for direction in self.directions:
            is_eligible = True
            for dy, dx in direction.checks:
                i, j = elf.row + dy, elf.col + dx
                if (i, j) in self.grid:
                    is_eligible = False
                    break
            if is_eligible:
                dy, dx = direction.adj
                next_coord = (elf.row + dy, elf.col + dx)
                self.proposed[next_coord] = (
                    None if next_coord in self.proposed else elf
                )
                break

    def pretty_print(self):
        buf = []

        min_x, min_y, max_x, max_y = self.bounding_rect
        for i in range(min_y, max_y + 1):
            for j in range(min_x, max_x + 1):
                if (i, j) in self.grid:
                    buf.append('#')
                else:
                    buf.append('.')
            buf.append('\n')

        s = ''.join(buf)
        return s


@dataclass
class Elf:
    row: int
    col: int

    @property
    def coords(self):
        return (self.row, self.col)

    def move_to(self, row, col):
        self.row = row
        self.col = col


if __name__ == '__main__':
    main()
