# Python Standard Library Imports
import re

from utils import (
    RE,
    BaseSolution,
    config,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (46065, 14134)


@solution
class Solution(BaseSolution):
    def process_data(self):
        self.instructions = [
            Instruction(instruction) for instruction in self.data
        ]

    def solve1(self):
        logic_gates = LogicGates(self.instructions)
        logic_gates.run()
        answer = logic_gates.gates['a']

        self.answer1 = answer
        return answer

    def solve2(self):
        logic_gates = LogicGates(self.instructions)
        logic_gates.gates['b'] = self.answer1
        logic_gates.run()

        answer = logic_gates.gates['a']
        return answer


class Instruction:
    SIGNAL_REGEXP = re.compile(r'^(?P<w>(\d+)|([a-z]+)) -> (?P<wire>[a-z]+)$')
    AND_REGEXP = re.compile(
        r'^(?P<w1>(\d+)|([a-z]+)) AND (?P<w2>(\d+)|([a-z]+)) -> (?P<wire>[a-z]+)$'
    )
    OR_REGEXP = re.compile(
        r'^(?P<w1>(\d+)|([a-z]+)) OR (?P<w2>(\d+)|([a-z]+)) -> (?P<wire>[a-z]+)$'
    )
    LSHIFT_REGEXP = re.compile(
        r'^(?P<w>[a-z]+) LSHIFT (?P<value>\d+) -> (?P<wire>[a-z]+)$'
    )
    RSHIFT_REGEXP = re.compile(
        r'^(?P<w>[a-z]+) RSHIFT (?P<value>\d+) -> (?P<wire>[a-z]+)$'
    )
    NOT_REGEXP = re.compile(r'^NOT (?P<w>[a-z]+) -> (?P<wire>[a-z]+)$')

    def __init__(self, instruction):
        self.instruction = instruction

        if RE.match(self.SIGNAL_REGEXP, instruction):
            self.instruction_type = 'SIGNAL'

            self.w, self.wire = (
                RE.m.group('w'),
                RE.m.group('wire'),
            )
        elif RE.match(self.AND_REGEXP, instruction):
            self.instruction_type = 'AND'

            self.w1, self.w2, self.wire = (
                RE.m.group('w1'),
                RE.m.group('w2'),
                RE.m.group('wire'),
            )
        elif RE.match(self.OR_REGEXP, instruction):
            self.instruction_type = 'OR'

            self.w1, self.w2, self.wire = (
                RE.m.group('w1'),
                RE.m.group('w2'),
                RE.m.group('wire'),
            )
        elif RE.match(self.LSHIFT_REGEXP, instruction):
            self.instruction_type = 'LSHIFT'

            self.w, self.value, self.wire = (
                RE.m.group('w'),
                int(RE.m.group('value')),
                RE.m.group('wire'),
            )
        elif RE.match(self.RSHIFT_REGEXP, instruction):
            self.instruction_type = 'RSHIFT'

            self.w, self.value, self.wire = (
                RE.m.group('w'),
                int(RE.m.group('value')),
                RE.m.group('wire'),
            )
        elif RE.match(self.NOT_REGEXP, instruction):
            self.instruction_type = 'NOT'

            self.w, self.wire = (
                RE.m.group('w'),
                RE.m.group('wire'),
            )
        else:
            raise Exception('Bad instruction: %s' % instruction)


class LogicGates:
    def __init__(self, instructions):
        self.instructions = instructions

        self.gates = {}

        for instruction in instructions:
            wire = instruction.wire
            self.gates[wire] = instruction

    def run(self):
        was_updated = True

        while was_updated:
            was_updated = self.step()

    def step(self):
        was_updated = False

        for wire, value in self.gates.items():
            if isinstance(value, Instruction):
                instruction = value
                result = self.evaluate(instruction)
                if result is not None:
                    self.gates[wire] = result
                    was_updated = True
                    break

        return was_updated

    def evaluate(self, instruction):
        result = None

        instruction_type = instruction.instruction_type

        if instruction_type == 'SIGNAL':
            w = instruction.w

            v = self.gates[w] if w in self.gates else int(w)

            if type(v) == int:
                result = v
        elif instruction_type == 'AND':
            w1, w2 = instruction.w1, instruction.w2
            v1, v2 = (
                self.gates[w1] if w1 in self.gates else int(w1),
                self.gates[w2] if w2 in self.gates else int(w2),
            )

            if type(v1) == int and type(v2) == int:
                result = v1 & v2
        elif instruction_type == 'OR':
            w1, w2 = instruction.w1, instruction.w2
            v1, v2 = (
                self.gates[w1] if w1 in self.gates else int(w1),
                self.gates[w2] if w2 in self.gates else int(w2),
            )

            if type(v1) == int and type(v2) == int:
                result = v1 | v2
        elif instruction_type == 'LSHIFT':
            w, value = instruction.w, instruction.value
            v = self.gates[w]

            if type(v) == int:
                result = v << value
        elif instruction_type == 'RSHIFT':
            w, value = instruction.w, instruction.value
            v = self.gates[w]

            if type(v) == int:
                result = v >> value
        elif instruction_type == 'NOT':
            w = instruction.w
            v = self.gates[w]

            if type(v) == int:
                result = ~v

        return result


if __name__ == '__main__':
    main()
