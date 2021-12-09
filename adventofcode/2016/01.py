# Python Standard Library Imports
import re

from utils import (
    InputConfig,
    ingest,
)


INPUT_FILE = '01.in'
EXPECTED_ANSWERS = (271, 153, )

# INPUT_FILE = '01.test.in'
# EXPECTED_ANSWERS = (8, 4, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        data = ingest(INPUT_FILE, InputConfig(as_oneline=True))
        self.directions = [Direction(direction.strip()) for direction in data.split(',')]

    def solve1(self):
        grid = Grid()
        for direction in self.directions:
            grid.move(direction)
        answer = grid.manhattan_distance
        return answer

    def solve2(self):
        answer = None

        grid = Grid()

        for direction in self.directions:
            was_reached = grid.move(direction, crawl_mode=True)
            if was_reached:
                answer = grid.manhattan_distance
                break

        return answer


class Grid:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.orientation_x = 0
        self.orientation_y = 1
        self.visited = {
            '0.0': True,
        }

    def move(self, direction, crawl_mode=False):
        was_reached = None

        self.turn(direction.turn)
        if crawl_mode:
            was_reached = self.crawl(direction.distance)
        else:
            self.go(direction.distance)

        return was_reached

    def turn(self, turn):
        if turn == 'L':
            if self.orientation_x != 0:
                self.orientation_y = self.orientation_x
                self.orientation_x = 0
            elif self.orientation_y != 0:
                self.orientation_x = self.orientation_y * -1
                self.orientation_y = 0
        elif turn == 'R':
            if self.orientation_x != 0:
                self.orientation_y = self.orientation_x * -1
                self.orientation_x = 0
            elif self.orientation_y != 0:
                self.orientation_x = self.orientation_y
                self.orientation_y = 0

    def go(self, distance):
        self.x += distance * self.orientation_x
        self.y += distance * self.orientation_y

    def crawl(self, distance):
        reached = False
        for i in range(distance):
            self.x += self.orientation_x
            self.y += self.orientation_y
            xy = '{}.{}'.format(self.x, self.y)
            if xy in self.visited:
                reached = True
                break
            else:
                self.visited[xy] = True

        return reached

    @property
    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)


class Direction:
    REGEXP = re.compile(r'^(?P<turn>R|L)(?P<distance>\d+)$')

    def __init__(self, direction):
        m = self.REGEXP.match(direction)
        if m:
            self.turn, self.distance = (
                m.group('turn'),
                int(m.group('distance'))
            )
        else:
            raise Exception('Bad direction: %s' % direction)


if __name__ == '__main__':
    main()
