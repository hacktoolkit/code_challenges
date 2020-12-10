import copy
import re

from utils import ingest


INPUT_FILE = '8.in'
EXPECTED_ANSWERS = (2014, 2251, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)

    def solve1(self):
        instructions = [Instruction(instruction) for instruction in self.data]
        program = Program(instructions)
        normal_termination, accumulator = program.run()
        answer = accumulator
        return answer

    def solve2(self):
        answer = None

        for i in range(len(self.data)):
            instructions = [Instruction(instruction) for instruction in self.data]
            instruction = instructions[i]

            operation = instruction.operation

            if operation in ('nop', 'jmp', ):
                instruction.operation = 'nop' if operation == 'jmp' else 'jmp'

                program = Program(instructions)
                normal_termination, accumulator = program.run()

                if normal_termination:
                    answer = accumulator
                    break

        return answer


class Instruction:
    REGEXP = re.compile(r'^(?P<operation>(acc)|(jmp)|(nop)) (?P<sign>(\+)|(-))(?P<number>\d+)$')

    def __init__(self, instruction):
        self.instruction = instruction

        m = self.REGEXP.match(instruction)
        if m:
            operation, sign, number = (
                m.group('operation'),
                m.group('sign'),
                int(m.group('number')),
            )

            self.operation = operation
            self.number = number * (1 if sign == '+' else -1)
        else:
            raise Exception('Bad instruction %s:' % instruction)


class Program:
    def __init__(self, instructions):
        self.instructions = instructions

    def run(self):
        instructions = self.instructions
        accumulator = 0

        index = 0
        visited = [False] * len(instructions)

        prev_index = None

        normal_termination = True
        while index < len(instructions):
            if visited[index]:
                normal_termination = False
                break
            else:
                visited[index] = True

            instruction = instructions[index]
            operation, number = instruction.operation, instruction.number

            if operation == 'nop':
                index += 1
            elif operation == 'acc':
                accumulator += number
                index += 1
            elif operation == 'jmp':
                index += number

        return normal_termination, accumulator


if __name__ == '__main__':
    main()
