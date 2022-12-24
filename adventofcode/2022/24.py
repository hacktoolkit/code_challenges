# Python Standard Library Imports
import operator
import typing as T
from collections import deque

from utils import (
    RE,
    BaseSolution,
    Graph,
    InputConfig,
    TriColor,
    Vertex,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (332, 942)
config.TEST_CASES = {
    '': (18, 54),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        self.valley = Valley(self.data)

    def solve1(self):
        valley = self.valley

        source, _ = SpaceTime.get_or_create((*Valley.START, 0))
        target, _ = SpaceTime.get_or_create((*Valley.END, None))
        print(f'Finding shortest path from {source} to {target}')
        path, distance = valley.bfs(source, target)
        t = distance - 1

        self.target, _ = SpaceTime.get_or_create((*Valley.END, t))

        answer = t
        return answer

    def solve2(self):
        valley = self.valley

        source2 = self.target
        target2, _ = SpaceTime.get_or_create((*Valley.START, None))
        print(f'Finding shortest path from {source2} to {target2}')
        path2, distance2 = valley.bfs(source2, target2)
        t2 = distance2 - 1
        print(t2)

        source3, _ = SpaceTime.get_or_create((*Valley.START, t2))
        target3, _ = SpaceTime.get_or_create((*Valley.END, None))
        print(f'Finding shortest path from {source3} to {target3}')
        path3, distance3 = valley.bfs(source3, target3)
        t3 = distance3 - 1

        answer = t3
        return answer


class Valley(Graph):
    START = (-1, 0)
    END = None

    def __init__(self, data):
        # skip the walls
        self.grid = {
            (i, j): cell
            for i, row in enumerate(data[1:-1])
            for j, cell in enumerate(row[1:-1])
        }
        self.M = len(data) - 2
        self.N = len(data[0]) - 2

        self.__class__.END = (self.M, self.N - 1)

    def is_valid(self, i, j, t):
        """Determines whether the cell `(i, j)` at time `t` is valid placeto stand in

        Not safe if:
        - Has a blizzard in cell at time `t`
        - Is a wall of the valley

        """
        is_valid = False

        if (i, j) in (Valley.START, Valley.END):
            # starting and ending cells are safe
            is_valid = True
        elif i < 0 or i >= self.M or j < 0 or j >= self.N:
            # walls and beyond
            is_valid = False
        else:
            # check whether cell at time `t` has a blizzard
            is_valid = not self.has_blizzard(i, j, t)
        return is_valid

    def has_blizzard(self, i, j, t):
        """Determines whether a cell at `(i, j)` and time `t` has a blizzard

        Implements wraparound logic for repeating blizzard
        """
        has_blizzard = (
            self.grid[(i - t) % self.M, j] == 'v'
            or self.grid[(i + t) % self.M, j] == '^'
            or self.grid[i, (j - t) % self.N] == '>'
            or self.grid[i, (j + t) % self.N] == '<'
        )
        return has_blizzard

    def neighbors_of(self, v, color=None):
        """Returns neighbors of `v` which have not been visited yet

        Utilizes `Vertex.get_or_create` to determine whether a vertex has been previously visited
        """
        directions = [
            (0, 0),  # wait in same spot
            (-1, 0),  # up
            (1, 0),  # down
            (0, -1),  # left
            (0, 1),  # right
        ]
        neighbors = []
        for d in directions:
            w, was_created = v.adj(*d)
            # debug(w, was_created, w.color)
            if w.color != TriColor.BLACK and self.is_valid(*w.label):
                neighbors.append((w, 1))

        debug(f'Neighbors of {v}: {neighbors}')
        return neighbors


class SpaceTime(Vertex):
    @property
    def coords(self):
        i, j, t = self.label
        return (i, j)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return str(self.label)

    def __eq__(self, other):
        if (self.coords == Valley.END and other.coords == Valley.END) or (
            self.coords == Valley.START and other.coords == Valley.START
        ):
            # start/end cells only need to compare the start/end coordinates, and not the timestamp
            is_equal = True
        else:
            # requires comparing all of (i, j, t)
            is_equal = self.label == other.label

        return is_equal

    def __hash__(self):
        return hash(self.label)

    def adj(self, dy, dx):
        """Calculates the next `SpaceTime` coordinate moving in `(dy, dx)`

        Advances the timestamp by 1
        """
        cell, was_created = SpaceTime.get_or_create(
            tuple(map(operator.add, self.label, (dy, dx, 1)))
        )
        return cell, was_created


if __name__ == '__main__':
    main()
