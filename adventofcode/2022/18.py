# Python Standard Library Imports
import copy
import typing as T
from collections import (
    defaultdict,
    deque,
)
from dataclasses import (
    dataclass,
    field,
)
from functools import (
    cache,
    cached_property,
)

from utils import (
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (4310, 2466)
config.TEST_CASES = {
    '': (10, 10),
    'b': (64, 58),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        cubes = [Cube.from_raw(raw_coords) for raw_coords in data]
        self.droplet = Droplet(cubes)

    def solve1(self):
        (
            total_uncovered_surface_area,
            total_external_surface_area,
        ) = self.droplet.total_surface_area
        answer = total_uncovered_surface_area
        return answer

    def solve2(self):
        (
            total_uncovered_surface_area,
            total_external_surface_area,
        ) = self.droplet.total_surface_area
        answer = total_external_surface_area
        return answer


@dataclass
class Cube:
    x: int
    y: int
    z: int

    @classmethod
    def from_raw(cls, raw_coords):
        def _transform(x):
            return int(x.split())

        cube = cls(*map(int, raw_coords.split(',')))
        return cube

    @property
    def coords(self):
        return (self.x, self.y, self.z)

    @property
    def neighbor_coords(self):
        shifts = [
            (-1, 0, 0),
            (1, 0, 0),
            (0, -1, 0),
            (0, 1, 0),
            (0, 0, -1),
            (0, 0, 1),
        ]
        for (dx, dy, dz) in shifts:
            yield (self.x + dx, self.y + dy, self.z + dz)


class Droplet:
    def __init__(self, cubes):
        self.cubes = cubes
        self.spatial_map = set()

        self.external_air = set()
        self.enclosed_air = set()

        for cube in cubes:
            self.spatial_map.add(cube.coords)

        self.min_x = min((cube.x for cube in self.cubes))
        self.max_x = max((cube.x for cube in self.cubes))
        self.min_y = min((cube.y for cube in self.cubes))
        self.max_y = max((cube.y for cube in self.cubes))
        self.min_z = min((cube.z for cube in self.cubes))
        self.max_z = max((cube.z for cube in self.cubes))

    @cached_property
    def total_surface_area(self):
        total_uncovered_surface_area = 0
        total_external_surface_area = 0
        for cube in self.cubes:
            (
                uncovered_surface_area,
                external_surface_area,
            ) = self.cube_surface_area(cube)
            total_uncovered_surface_area += uncovered_surface_area
            total_external_surface_area += external_surface_area

        return total_uncovered_surface_area, total_external_surface_area

    def cube_surface_area(self, cube):
        uncovered_surface_area = 0
        external_surface_area = 0
        exposed = 0
        for x, y, z in cube.neighbor_coords:
            if (x, y, z) not in self.spatial_map:
                uncovered_surface_area += 1
                if not self.is_enclosed_air((x, y, z)):
                    external_surface_area += 1
            else:
                pass
        return uncovered_surface_area, external_surface_area

    def is_enclosed_air(self, coord):
        """Determines whether `coord` represents a pocket of enclosed air

        Expands neighbors of `coord` until we find
        """
        visited = set()
        Q = deque()

        Q.append(coord)

        while len(Q) > 0:
            coord2 = Q.popleft()

            if coord2 in self.enclosed_air:
                return True
            elif coord2 in self.external_air:
                return False
            elif len(visited) > len(self.cubes):
                self.external_air.add(coord2)
                return False
            else:
                for coord3 in Cube(*coord2).neighbor_coords:
                    # check previously undifferentiated air cubes
                    if (
                        coord3 not in self.spatial_map
                        and coord3 not in visited
                        and coord3 not in self.enclosed_air
                    ):
                        visited.add(coord3)
                        Q.append(coord3)

        self.enclosed_air.add(coord)
        return True


if __name__ == '__main__':
    main()
