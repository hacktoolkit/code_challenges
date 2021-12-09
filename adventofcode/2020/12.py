# Python Standard Library Imports
import re

from utils import (
    Re,
    ingest,
)


INPUT_FILE = '12.in'
EXPECTED_ANSWERS = (364, 39518, )

# INPUT_FILE = '12.test.in'
# EXPECTED_ANSWERS = (25, 286, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        data = ingest(INPUT_FILE)
        self.instructions = [Instruction(instruction) for instruction in data]

    def solve1(self):
        ship = Ship()
        for instruction in self.instructions:
            ship.move(instruction)
            print(ship.coords)

        answer = ship.manhattan_distance
        return answer

    def solve2(self):
        ship = Ship()
        for instruction in self.instructions:
            ship.waypoint_move(instruction)
            print(ship.coords, ship.waypoint)

        answer = ship.manhattan_distance
        return answer


class Ship:
    DIRECTION_MAP = {
        'N': (0, 1, ),
        'S': (0, -1, ),
        'E': (1, 0, ),
        'W': (-1, 0, ),
    }
    RIGHT_TURN_MAP = {
        'N': 'E',
        'E': 'S',
        'S': 'W',
        'W': 'N',
    }

    def __init__(self):
        self.x, self.y = (0, 0, )
        self.orientation = 'E'

        self.waypoint_x, self.waypoint_y = (10, 1, )

    @property
    def coords(self):
        return (self.x, self.y, )

    @property
    def waypoint(self):
        return (self.waypoint_x, self.waypoint_y, )

    @property
    def direction(self):
        return Ship.DIRECTION[self.orientation]

    @property
    def manhattan_distance(self):
        return abs(self.x) + abs(self.y)

    ##
    # Step 1

    def move(self, instruction):
        if instruction.delta_x:
            self.x += instruction.delta_x
        elif instruction.delta_y:
            self.y += instruction.delta_y
        elif instruction.turns:
            self.turn(instruction.turns)
        elif instruction.forward:
            x, y = Ship.DIRECTION_MAP.get(self.orientation)
            self.x += x * instruction.forward
            self.y += y * instruction.forward
        else:
            pass

    def turn(self, turns):
        turns = turns % 4
        for i in range(turns):
            self.turn_right()

    def turn_right(self):
        self.orientation = Ship.RIGHT_TURN_MAP[self.orientation]

    ##
    # Step 2

    def waypoint_move(self, instruction):
        if instruction.delta_x:
            self.waypoint_x += instruction.delta_x
        elif instruction.delta_y:
            self.waypoint_y += instruction.delta_y
        elif instruction.turns:
            self.rotate_waypoint(instruction.turns)
        elif instruction.forward:
            self.x += self.waypoint_x * instruction.forward
            self.y += self.waypoint_y * instruction.forward
        else:
            pass

    def rotate_waypoint(self, rotations):
        rotations = rotations % 4
        for i in range(rotations):
            self.rotate_waypoint_right()

    def rotate_waypoint_right(self):
        self.waypoint_x, self.waypoint_y = (
            self.waypoint_y,
            self.waypoint_x * -1,
        )


class Instruction:
    DIR_REGEX = r'^(?P<action>N|S|E|W|L|R|F)(?P<value>\d+)$'

    def __init__(self, instruction):
        self.delta_x = 0
        self.delta_y = 0
        self.turns = 0
        self.forward = 0

        regex = Re()
        if regex.match(Instruction.DIR_REGEX, instruction):
            m = regex.last_match
            action, value = (
                m.group('action'),
                int(m.group('value')),
            )

            if action in Ship.DIRECTION_MAP:
                x, y = Ship.DIRECTION_MAP[action]
                self.delta_x, self.delta_y = x * value, y * value
            elif action in ('R', 'L'):
                turn_multiplier = 1 if action == 'R' else -1
                if value % 90 == 0:
                    self.turns = turn_multiplier * (value // 90)
                else:
                    raise Exception('Bad turn angle: %s%s' % (action, value))
            elif action == 'F':
                self.forward = value
            else:
                raise Exception('Impossible case')
        else:
            raise Exception('Bad instruction: %s' % instruction)


if __name__ == '__main__':
    main()
