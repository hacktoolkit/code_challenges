# Python Standard Library Imports
import re

from utils import ingest


INPUT_FILE = '06.in'
EXPECTED_ANSWERS = (543903, 14687245, )

# INPUT_FILE = '06.test.in'
# EXPECTED_ANSWERS = (1000000 - (1000000 - 1000 - 4), 3001997, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        data = ingest(INPUT_FILE)
        self.instructions = [Instruction(instruction) for instruction in data]
        self.light_show = LightShow(self.instructions)

    def solve1(self):
        self.light_show.run()
        answer = self.light_show.num_lights_on
        return answer

    def solve2(self):
        self.light_show.run2()
        answer = self.light_show.total_brightness
        return answer


class Instruction:
    REGEXP = re.compile(r'^(?P<operation>(turn on)|(turn off)|(toggle)) (?P<x1>\d+),(?P<y1>\d+) through (?P<x2>\d+),(?P<y2>\d+)$')

    def __init__(self, instruction):
        self.instruction = instruction

        m = self.REGEXP.match(instruction)
        if m:
            self.operation, self.x1, self.y1, self.x2, self.y2 = (
                m.group('operation'),
                int(m.group('x1')),
                int(m.group('y1')),
                int(m.group('x2')),
                int(m.group('y2')),
            )


class LightShow:
    def __init__(self, instructions):
        self.instructions = instructions

        self.lights = [
            [False, ] * 1000
            for x
            in range(1000)
        ]

        self.lights2 = [
            [0, ] * 1000
            for x
            in range(1000)
        ]

    def run(self):
        lights = self.lights
        for instruction in self.instructions:
            operation, x1, y1, x2, y2 = (
                instruction.operation,
                instruction.x1,
                instruction.y1,
                instruction.x2,
                instruction.y2,
            )

            for i in range(x1, x2 + 1):
                for j in range(y1, y2 + 1):
                    if operation == 'turn on':
                        lights[i][j] = True
                    elif operation == 'turn off':
                        lights[i][j] = False
                    elif operation == 'toggle':
                        lights[i][j] = not(lights[i][j])
                    else:
                        raise Exception('Illegal operation: %s' % operation)

    @property
    def num_lights_on(self):
        lights = self.lights
        count = 0
        for i in range(1000):
            for j in range(1000):
                if lights[i][j]:
                    count += 1

        return count

    def run2(self):
        lights = self.lights2
        for instruction in self.instructions:
            operation, x1, y1, x2, y2 = (
                instruction.operation,
                instruction.x1,
                instruction.y1,
                instruction.x2,
                instruction.y2,
            )

            for i in range(x1, x2 + 1):
                for j in range(y1, y2 + 1):
                    if operation == 'turn on':
                        lights[i][j] += 1
                    elif operation == 'turn off':
                        lights[i][j] = max(0, lights[i][j] - 1)
                    elif operation == 'toggle':
                        lights[i][j] += 2
                    else:
                        raise Exception('Illegal operation: %s' % operation)

    @property
    def total_brightness(self):
        lights = self.lights2
        brightness = 0
        for i in range(1000):
            for j in range(1000):
                brightness += lights[i][j]

        return brightness


if __name__ == '__main__':
    main()
