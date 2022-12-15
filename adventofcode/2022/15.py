# Python Standard Library Imports
import copy
import re
import typing as T
from dataclasses import dataclass
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


config.EXPECTED_ANSWERS = (4724228, 13622251246513)
config.TEST_CASES = {
    '': (26, 56000011),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data

        sensor_grid = SensorGrid(self.data)
        # sensor_grid.pretty_print()
        self.sensor_grid = sensor_grid

    def solve1(self):
        y = 10 if config.TEST_MODE else 2_000_000
        answer = self.sensor_grid.dead_spots(y)
        return answer

    def solve2(self):
        BEACON_RANGE_UPPER = 20 if config.TEST_MODE else 4_000_000
        beacon = self.sensor_grid.find_beacon(BEACON_RANGE_UPPER)
        answer = beacon.tuning_frequency
        return answer


@dataclass
class Coord:
    x: int
    y: int

    @cached_property
    def coords(self):
        return (self.x, self.y)


@dataclass
class Void(Coord):
    pass


@dataclass
class Beacon(Coord):
    @cached_property
    def tuning_frequency(self):
        return self.x * 4_000_000 + self.y


def manhattan(x1, x2, y1, y2):
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return dx + dy


@dataclass
class Sensor(Coord):
    beacon: 'Beacon'

    @cached_property
    def search_radius(self):
        return manhattan(self.x, self.beacon.x, self.y, self.beacon.y)

    def can_reach(self, x, y):
        return manhattan(x, self.x, y, self.y) <= self.search_radius

    def x_positions_on_y(self, y):
        r = self.search_radius
        positions = (
            x for x in range(self.x - r, self.x + r + 1) if self.can_reach(x, y)
        )
        return positions


class SensorGrid:
    REGEX = re.compile(
        r'^Sensor at x=(?P<sx>-?\d+), y=(?P<sy>-?\d+): closest beacon is at x=(?P<bx>-?\d+), y=(?P<by>-?\d+)$'
    )

    def __init__(self, data):
        grid = {}
        beacons = []
        sensors = []

        self.grid = grid
        self.beacons = beacons
        self.sensors = sensors

        for line in data:
            if RE.match(self.REGEX, line):
                keys = ['sx', 'sy', 'bx', 'by']
                (sx, sy, bx, by) = map(int, (RE.m.group(key) for key in keys))
                beacon = Beacon(bx, by)
                sensor = Sensor(sx, sy, beacon)

                beacons.append(beacon)
                sensors.append(sensor)

                grid[beacon.coords] = beacon
                grid[sensor.coords] = sensor
            else:
                raise Exception(f'Encountered bad data: {line}')

    def pretty_print(self):
        x_vals = [_.x for _ in (self.beacons + self.sensors)]
        y_vals = [_.y for _ in (self.beacons + self.sensors)]

        min_x = min(x_vals)
        max_x = max(x_vals)

        min_y = min(y_vals)
        max_y = max(y_vals)

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                content = self.grid.get((x, y))
                value = (
                    '.'
                    if content is None
                    else 'B'
                    if isinstance(content, Beacon)
                    else 'S'
                    if isinstance(content, Sensor)
                    else None
                )
                print(value, end='')
            print('')

    def dead_spots(self, y):
        count = 0

        for sensor in self.sensors:
            for x in sensor.x_positions_on_y(y):
                if self.grid.get((x, y)) is None:
                    self.grid[(x, y)] = Void(x, y)
                    count += 1
                else:
                    pass

        return count

    def find_beacon(self, upper):
        # beacon = self.find_beacon__naive(upper)
        beacon = self.find_beacon__fast(upper)
        return beacon

    def is_reachable_by_sensors(self, x, y):
        reachable = False
        for sensor in self.sensors:
            if sensor.can_reach(x, y):
                reachable = True
                break
        return reachable

    def find_beacon__naive(self, upper):
        start, end = (0, upper)

        for x in range(start, end + 1):
            for y in range(start, end + 1):
                reachable = self.is_reachable_by_sensors(x, y)
                if not reachable:
                    return Beacon(x, y)

        return None

    def find_beacon__fast(self, upper):
        # Reduce the search space compared to `find_beacon__naive()`
        # Look for the beacons from just beyond the reach of each sensor
        for sensor in self.sensors:
            r = sensor.search_radius
            for dx in range(r + 1 + 1):
                dy = r + 1 - dx

                for x in (sensor.x - dx, sensor.x + dx):
                    for y in (sensor.y - dy, sensor.y + dy):
                        if 0 <= x <= upper and 0 <= y <= upper:
                            reachable = self.is_reachable_by_sensors(x, y)
                            if not reachable:
                                return Beacon(x, y)

        return None


if __name__ == '__main__':
    main()
