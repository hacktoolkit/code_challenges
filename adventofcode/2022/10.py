from utils import (
    CRT,
    RE,
    BaseSolution,
    Font,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (12840, 'ZKJFBJFZ')
config.TEST_CASES = {
    '': (0, ''),
    'b': (13140, ''),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        self.cpu = CPU(self.data)
        self.cpu.run()

    def solve1(self):
        answer = sum(self.cpu.signals)
        return answer

    def solve2(self):
        debug(self.cpu.crt.render())
        answer = self.cpu.crt.read_characters()
        return answer


class CPU:
    MONITORS = {20, 60, 100, 140, 180, 220}
    CRT_WIDTH = 8

    def __init__(self, raw_instructions):
        self.raw_instructions = raw_instructions

        self.X = 1
        self.cycle = 0
        self.crt = CRT()

        self.signals = []

    def run(self):
        for i, instruction in enumerate(self.raw_instructions, 1):
            debug(i, self.cycle, self.X, instruction)
            parts = instruction.split()

            if parts[0] == 'noop':
                self.tick()
            elif parts[0] == 'addx':
                self.tick()
                self.tick()
                value = int(parts[1])
                self.X += value
            else:
                pass

    def tick(self):
        self.pre_tick()
        self.cycle += 1
        self.post_tick()

    def post_tick(self):
        # part 1
        if self.cycle in self.MONITORS:
            signal_strength = self.cycle * self.X
            debug('####', self.cycle, self.X, signal_strength)
            self.signals.append(signal_strength)

    def pre_tick(self):
        # part 2
        col = self.cycle % 40
        row = self.cycle // 40

        if self.X - 1 <= col <= self.X + 1:
            self.crt.pixel_on(row, col)
        else:
            pass


if __name__ == '__main__':
    main()
