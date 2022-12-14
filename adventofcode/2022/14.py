# Python Standard Library Imports
import functools
import typing as T
from dataclasses import dataclass

from utils import (
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    pairwise,
    solution,
)


config.EXPECTED_ANSWERS = (578, 24377)
config.TEST_CASES = {
    '': (24, 93),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data

        self.rock_formations = [
            [
                Coord(*map(int, raw_coords.split(',')))
                for raw_coords in line.split(' -> ')
            ]
            for line in data
        ]

    def solve1(self):
        cave = Cave(self.rock_formations)
        cave.pretty_print()
        answer = cave.pour_sand()
        cave.pretty_print()
        return answer

    def solve2(self):
        cave = Cave(self.rock_formations, has_floor=True)
        cave.pretty_print()
        answer = cave.pour_sand()
        cave.pretty_print()
        return answer


@functools.total_ordering
@dataclass
class Coord:
    x: int = 0
    y: int = 0

    def __str__(self):
        value = f'{self.__class__.__name__}: {self.coords}'
        return value

    @property
    def coords(self):
        return (self.x, self.y)

    def __lt__(self, other):
        if self.x < other.x:
            return True
        elif self.x == other.x:
            return self.y < other.y
        else:
            return False

    def __eq__(self, other):
        return self.coords == other.coords


class Rock(Coord):
    @classmethod
    def get_collection_from_formation(cls, rock_formation):
        rocks = []
        for c1, c2 in pairwise(rock_formation):
            c1, c2 = sorted([c1, c2])

            x1, y1 = c1.coords
            x2, y2 = c2.coords
            dx = x2 - x1
            dy = y2 - y1

            if dy > 0 and dx > 0:
                raise Exception('Not a straight line')
            elif dx > 0:
                coords = [(x, y1) for x in range(x1, x2 + 1)]
            elif dy > 0:
                coords = [(x1, y) for y in range(y1, y2 + 1)]
            else:
                raise Exception('A single point and not a line')

            rocks.extend([cls(*coord) for coord in coords])

        return rocks

    @property
    def symbol(self):
        return '#'


class Air(Coord):
    @property
    def symbol(self):
        return '.'


class Sand(Coord):
    @property
    def symbol(self):
        return 'o'

    def fall(self, cave):
        next_positions = (
            (self.x, self.y + 1),
            (self.x - 1, self.y + 1),
            (self.x + 1, self.y + 1),
        )

        try:
            self.x, self.y = next(
                (x, y)
                for (x, y) in next_positions
                if (
                    (x, y) not in cave.grid
                    and (
                        not cave.has_floor
                        or cave.has_floor
                        and y < cave.floor_y
                    )
                )
            )
        except StopIteration:
            # next() called on an empty iterator
            pass


class Origin(Coord):
    @property
    def symbol(self):
        return '+'


class Cave:
    SAND_ORIGIN = (500, 0)
    FLOOR_GAP = 2

    def __init__(self, rock_formations, has_floor=False):
        self.grid = {}
        self.min_x = None
        self.max_x = None
        self.max_y = 0

        self.init_rocks(rock_formations, has_floor=has_floor)

        origin = Origin(*self.SAND_ORIGIN)
        self.grid[origin.coords] = origin

        self.has_floor = has_floor
        self.floor_y = (
            (self.max_y + self.FLOOR_GAP) if has_floor else self.max_y
        )

    def init_rocks(self, rock_formations, has_floor=False):
        for rock_formation in rock_formations:
            rocks = Rock.get_collection_from_formation(rock_formation)
            for rock in rocks:
                _, y = rock.coords
                self.max_y = max(y, self.max_y)
                self.grid[rock.coords] = rock

        self.update_bounds()

        if has_floor:
            for x in range(self.min_x, self.max_x + 1):
                rock = Rock(x, self.max_y + self.FLOOR_GAP)
                self.grid[rock.coords] = rock

    def update_bounds(self):
        for (x, y) in self.grid:
            self.min_x = min(x, self.min_x) if self.min_x else x
            self.max_x = max(x, self.max_x) if self.max_x else x

    def pretty_print(self):
        for y in range(self.floor_y + 1):
            x_start = self.min_x - 2 if self.has_floor else self.min_x
            x_end = self.max_x + 2 if self.has_floor else self.max_x
            for x in range(x_start, x_end + 1):
                default_particle = (
                    Rock() if self.has_floor and y == self.floor_y else Air()
                )
                particle = self.grid.get((x, y), default_particle)
                print(particle.symbol, end='')
            print('')
        print('')

    def pour_sand(self):
        """Pours sand from ORIGIN

        Returns the number of sand particles that come to rest
        """
        sand_particles = 0

        while True:
            sand = Sand(*self.SAND_ORIGIN)
            while sand.y < self.floor_y:
                prev_y = sand.y
                sand.fall(self)
                if sand.y == prev_y:
                    # sand particle came to rest
                    self.grid[sand.coords] = sand
                    if self.has_floor and sand.y + 1 == self.floor_y:
                        rock = Rock(sand.x, self.floor_y)
                        self.grid[rock.coords] = rock
                        self.update_bounds()
                    sand_particles += 1
                    break
            else:
                # sand particles kept falling past lowest rock formation
                break

            if sand.coords == self.SAND_ORIGIN:
                break

        return sand_particles


if __name__ == '__main__':
    main()
