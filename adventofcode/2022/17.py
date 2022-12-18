# Python Standard Library Imports
import copy
from collections import defaultdict
from dataclasses import (
    dataclass,
    field,
)
from functools import cached_property

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (3191, 1572093023267)
config.TEST_CASES = {
    '': (3068, 1514285714288),
}

config.INPUT_CONFIG.as_oneline = True


@solution
class Solution(BaseSolution):
    TARGET_1 = 2022
    TARGET_2 = 1_000_000_000_000

    def process_data(self):
        data = self.data
        self.chamber = Chamber(data)

    def solve1(self):
        chamber = self.chamber
        finalized_pieces = 0
        while finalized_pieces < self.TARGET_1:
            chamber.add_rock()
            finalized_pieces += 1

        answer = chamber.rock_height
        return answer

    def solve2(self):
        chamber = self.chamber
        finalized_pieces = self.TARGET_1
        fast_forward_height = 0

        while finalized_pieces < self.TARGET_2:
            chamber.add_rock()
            finalized_pieces += 1
            snapshot, previous_matching_snapshot = chamber.capture_snapshot(
                finalized_pieces
            )
            if previous_matching_snapshot is not None:
                # found repeat cycle
                # "fast-forward" using snapshot
                dy = (
                    snapshot.rock_height
                    - previous_matching_snapshot.rock_height
                )
                d_finalized_pieces = (
                    snapshot.finalized_pieces
                    - previous_matching_snapshot.finalized_pieces
                )
                steps = (
                    self.TARGET_2 - snapshot.finalized_pieces
                ) // d_finalized_pieces
                if steps > 0:
                    fast_forward_height = dy * steps
                    finalized_pieces += d_finalized_pieces * steps
                    print(
                        f'Fast-forward from {snapshot.finalized_pieces} (height: {snapshot.rock_height}) to {finalized_pieces} (height: {snapshot.rock_height + fast_forward_height}) pieces finalized (dy: {dy}; d_finalized_pieces: {d_finalized_pieces}; steps: {steps})'
                    )
                else:
                    pass
            else:
                pass

        answer = chamber.rock_height + fast_forward_height
        return answer


@dataclass
class Coord:
    x: int
    y: int

    @property
    def coords(self):
        return (self.x, self.y)

    def __copy__(self):
        return Coord(*self.coords)

    def __deepcopy__(self, memo):
        return copy.copy(self)


@dataclass
class Rock(Coord):
    x: int = 0
    y: int = 0
    matter: list[Coord] = field(default_factory=list)

    def __copy__(self):
        matter = copy.deepcopy(self.matter)
        return Rock(*self.coords, matter)

    @cached_property
    def rect(self):
        """Gets the bounding rectangle for this rock

        Returns a pair of `Coord` objects representing the bottom left and the top right.
        """
        max_x = max([coord.x for coord in self.matter])
        max_y = max([coord.y for coord in self.matter])
        return self.coords, Coord(max_x, max_y)

    @property
    def matter_coords(self):
        coords = {(self.x + coord.x, self.y + coord.y) for coord in self.matter}
        return coords

    def occupies_coord(self, x, y):
        return (x, y) in self.matter_coords


ROCKS = [
    # Anchor rocks to their bottom left rectangle
    # ..####
    Rock(x=2, y=0, matter=[Coord(0, 0), Coord(1, 0), Coord(2, 0), Coord(3, 0)]),
    # ...#.
    # ..###
    # ...#.
    Rock(
        x=2,
        y=0,
        matter=[
            Coord(1, 2),
            Coord(0, 1),
            Coord(1, 1),
            Coord(2, 1),
            Coord(1, 0),
        ],
    ),
    # ....#
    # ....#
    # ..###
    Rock(
        x=2,
        y=0,
        matter=[
            Coord(2, 2),
            Coord(2, 1),
            Coord(0, 0),
            Coord(1, 0),
            Coord(2, 0),
        ],
    ),
    # ..#
    # ..#
    # ..#
    # ..#
    Rock(
        x=2,
        y=0,
        matter=[
            Coord(0, 3),
            Coord(0, 2),
            Coord(0, 1),
            Coord(0, 0),
        ],
    ),
    # ..##
    # ..##
    Rock(x=2, y=0, matter=[Coord(0, 1), Coord(1, 1), Coord(0, 0), Coord(1, 0)]),
]


class Chamber:
    WIDTH = 7
    DROP_HEIGHT = 3
    SNAPSHOT_HEIGHT = 30

    def __init__(self, jet_pattern):
        self.jet_pattern = jet_pattern
        self.grid = {}

        self.rock_index = 0
        self.jet_index = 0

        self.top = 0
        self.active_rock = None

        self.snapshots = {}

    @property
    def rock_height(self):
        max_y = max([0] + [y for x, y in self.grid.keys()])
        if self.active_rock:
            max_y = max(
                [max_y] + [y for (x, y) in self.active_rock.matter_coords]
            )
        return max_y + 1

    @property
    def next_rock(self):
        rock = copy.copy(ROCKS[self.rock_index])
        self.rock_index = (self.rock_index + 1) % len(ROCKS)

        rock.y = self.top + self.DROP_HEIGHT
        self.active_rock = rock

        return rock

    @property
    def next_jet_direction(self):
        jet_direction = self.jet_pattern[self.jet_index]
        self.jet_index = (self.jet_index + 1) % len(self.jet_pattern)
        return jet_direction

    def add_rock(self):
        debug(f'Add rock. Top: {self.top}')
        rock = self.next_rock

        # drop rock until it hits bottom
        did_drop = True
        while did_drop:
            _ = self.move_rock_in_jet_direction(rock)
            did_drop = self.move_rock_down(rock)

        self.finalize_rock(rock)

    def has_collision(self, rock):
        has_collision = False
        for x, y in rock.matter_coords:
            if (
                (x < 0 or x >= self.WIDTH)
                or (self.grid.get((x, y)) is not None)
                or y < 0
            ):
                debug(f'Collision at {(x,y)}')
                has_collision = True
                break
        return has_collision

    def move_rock(self, rock, dx, dy):
        did_move = True
        rock.x += dx
        rock.y += dy
        if self.has_collision(rock):
            # undo the move
            rock.x -= dx
            rock.y -= dy
            did_move = False

        if config.DEBUGGING:
            debug(self.pretty_print())
        return did_move

    def move_rock_left(self, rock):
        debug('Move left')
        return self.move_rock(rock, -1, 0)

    def move_rock_right(self, rock):
        debug('Move right')
        return self.move_rock(rock, 1, 0)

    def move_rock_down(self, rock):
        debug('Move down')
        return self.move_rock(rock, 0, -1)

    def move_rock_in_jet_direction(self, rock):
        jet_direction = self.next_jet_direction

        if jet_direction == '<':
            self.move_rock_left(rock)
        elif jet_direction == '>':
            self.move_rock_right(rock)
        else:
            raise Exception('Bad jet direction')

    def finalize_rock(self, rock):
        self.active_rock = None
        max_y = None
        for x, y in rock.matter_coords:
            max_y = y + 1 if max_y is None else max(y + 1, max_y)
            self.grid[(x, y)] = '#'
        self.top = max(max_y, self.top)
        if config.DEBUGGING:
            debug(self.pretty_print())

    def pretty_print(self, n_lines=None) -> str:
        buf = []
        j_start = self.rock_height
        j_end = (self.rock_height - n_lines) if n_lines is not None else 0
        for j in range(j_start + 1, j_end - 1, -1):
            for i in range(self.WIDTH + 2):
                x = i - 1
                y = j - 1
                if i in (0, self.WIDTH + 1):
                    c = '+' if j == 0 else '|'
                elif j == 0:
                    c = '-'
                elif self.active_rock and self.active_rock.occupies_coord(x, y):
                    c = '@'
                else:
                    c = self.grid.get((x, y), '.')
                buf.append(c)
            buf.append('\n')
        buf.append('\n')
        s = ''.join(buf)
        return s

    def chamber_scan(self) -> str:
        """Returns a cross section of the scan of the top `n_lines`

        Used to detect if a cycle has happened
        """
        s = self.pretty_print(n_lines=self.SNAPSHOT_HEIGHT)
        scan = '\n'.join(s.split('\n'))
        return scan

    def capture_snapshot(self, finalized_pieces):
        snapshot = Snapshot(
            self.rock_index,
            self.jet_index,
            self.chamber_scan(),
            finalized_pieces,
            self.rock_height,
        )
        prev_snapshot = self.snapshots.get(snapshot)
        self.snapshots[snapshot] = snapshot
        return snapshot, prev_snapshot


@dataclass
class Snapshot:
    rock_index: int
    jet_index: int
    chamber_scan: str
    finalized_pieces: int
    rock_height: int

    @property
    def signature(self):
        return frozenset([self.rock_index, self.jet_index, self.chamber_scan])

    def __eq__(self, other):
        return self.signature == other.signature

    def __hash__(self):
        return hash(self.signature)


if __name__ == '__main__':
    main()
