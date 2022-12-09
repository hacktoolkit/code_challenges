# Python Standard Library Imports
import typing as T
from dataclasses import dataclass

from utils import (
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (6642, 2765)
config.TEST_CASES = {
    '': (13, 1),
    'b': (88, 36),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        self.moves = [Move.from_raw(raw_move) for raw_move in data]

    def solve1(self) -> int:
        rope = Rope(self.moves, knots=2)
        rope.run()

        answer = len(rope.T_visited)
        return answer

    def solve2(self) -> int:
        rope = Rope(self.moves, knots=10)
        rope.run()

        answer = len(rope.T_visited)
        return answer


@dataclass
class Move:
    direction: str
    distance: int

    @classmethod
    def from_raw(cls, raw_move):
        parts = raw_move.split()
        direction = parts[0]
        distance = int(parts[1])
        move = cls(direction, distance)
        return move

    @property
    def coords(self):
        COORDS = {
            'U': (0, 1),
            'D': (0, -1),
            'L': (-1, 0),
            'R': (1, 0),
        }
        return COORDS[self.direction]


class Rope:
    def __init__(self, moves, knots=2):
        self.moves = moves
        self.knots = knots

        self.H = (0, 0)
        self.K = [(0, 0) for _ in range(knots - 1)]

        self.T_visited = set()
        self.T_visited.add((0, 0))

    def run(self):
        for move in self.moves:
            self.do_move(move)

    def do_move(self, move):
        dx, dy = move.coords
        for i in range(move.distance):
            x, y = self.H
            self.H = (x + dx, y + dy)
            self.update_knots(dx, dy)

    def update_knots(self, dx, dy, knot=0):
        Ax, Ay = self.H if knot == 0 else self.K[knot - 1]
        Bx, By = self.K[knot]

        gap_x = Ax - Bx
        gap_y = Ay - By

        debug((dx, dy), (Ax, Ay), (Bx, By), (gap_x, gap_y))

        if abs(gap_x) <= 1 and abs(gap_y) <= 1:
            # B is currently touching A (either on top, touching, or 1 away)
            # no need to move
            pass
        else:
            # A is 2 spaces away, move B closer
            if gap_y == 0:
                dBx = dx
                dBy = 0
            elif gap_x == 0:
                dBx = 0
                dBy = dy
            elif abs(gap_x) == 1:
                dBx = gap_x
                dBy = dy
            elif abs(gap_y) == 1:
                dBx = dx
                dBy = gap_y
            elif abs(dx) == 1 and abs(dy) == 1:
                dBx, dBy = dx, dy
            else:
                raise Exception(
                    f'Impossible case. knot: {knot}; A: {(Ax, Ay)}; B: {(Bx, By)}; gap: {(gap_x, gap_y)}'
                )

            self.K[knot] = (Bx + dBx, By + dBy)

            if knot + 2 < self.knots:
                # a middle knot
                self.update_knots(dBx, dBy, knot=knot + 1)
            else:
                # the tail not
                self.T_visited.add(self.K[knot])


if __name__ == '__main__':
    main()
