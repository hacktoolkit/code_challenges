# Python Standard Library Imports
import copy

from utils import ingest


INPUT_FILE = '02.in'
EXPECTED_ANSWERS = (4945026, 5296, )

# INPUT_FILE = '02.test.in'
# EXPECTED_ANSWERS = (3500, None, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)
        self.numbers = [int(x) for x in ','.join(self.data).split(',')]
        self.intcode_prog = IntcodeProg(self.numbers)


    def solve1(self):
        answer = self.intcode_prog.run(12, 2)
        return answer

    def solve2(self):
        TARGET = 19690720

        answer = None

        for noun in range(100):
            for verb in range(100):
                result = self.intcode_prog.run(noun, verb)
                if result == TARGET:
                    answer = 100 * noun + verb

        return answer


class IntcodeProg:
    def __init__(self, instructions):
        self.instructions = copy.copy(instructions)

    def run(self, noun, verb):
        instructions = copy.copy(self.instructions)

        instructions[1] = noun
        instructions[2] = verb

        pointer = 0
        while pointer < len(instructions):
            opcode, in1, in2, dest = (
                instructions[pointer],
                instructions[pointer + 1],
                instructions[pointer + 2],
                instructions[pointer + 3]
            )

            if opcode in (1, 2):
                val1, val2 = instructions[in1], instructions[in2]
                if opcode == 1:
                    instructions[dest] = val1 + val2
                else:
                    instructions[dest] = val1 * val2

            elif opcode == 99:
                break
            else:
                raise Exception('Unknown opcode: %s' % opcode)

            pointer += 4

        result = instructions[0]
        return result


if __name__ == '__main__':
    main()
