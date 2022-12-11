# Python Standard Library Imports
import copy
import heapq
import math
import re
import typing as T
from collections import defaultdict
from dataclasses import dataclass

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (54752, 13606755504)
config.TEST_CASES = {
    '': (10605, 2713310158),
    # 'b': (None, None),
    # 'c': (None, None),
}

config.INPUT_CONFIG.as_integers = False
config.INPUT_CONFIG.as_comma_separated_integers = False
config.INPUT_CONFIG.as_json = False
config.INPUT_CONFIG.as_groups = True
config.INPUT_CONFIG.strip_lines = True
config.INPUT_CONFIG.as_oneline = False
config.INPUT_CONFIG.as_coordinates = False
config.INPUT_CONFIG.coordinate_delimeter = None
config.INPUT_CONFIG.as_table = False
config.INPUT_CONFIG.row_func = None
config.INPUT_CONFIG.cell_func = None


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data

    def solve1(self):
        monkeys = [Monkey.from_raw(_) for _ in self.data]
        game = Game(monkeys)
        game.run()

        m = iter(sorted(game.monkeys, reverse=True))
        m1, m2 = next(m), next(m)
        answer = m1.inspection_count * m2.inspection_count
        return answer

    def solve2(self):
        monkeys = [Monkey.from_raw(_) for _ in self.data]
        game = Game(monkeys)
        game.run(rounds=10000, is_part2=True)

        m = iter(sorted(game.monkeys, reverse=True))
        m1, m2 = next(m), next(m)
        answer = m1.inspection_count * m2.inspection_count
        return answer


class Game:
    def __init__(self, monkeys):
        self.monkeys = monkeys
        self.modulo = math.prod([m.divisor for m in self.monkeys])

    def run(self, rounds=20, is_part2=False):
        for _ in range(rounds):
            for i, monkey in enumerate(self.monkeys):
                while len(monkey.items) > 0:
                    item, other_monkey = monkey.inspect_item(
                        self.modulo, is_part2=is_part2
                    )
                    self.monkeys[other_monkey].receive_item(item)


@dataclass
class Monkey:
    items: list[int]
    operation: T.Callable
    divisor: int
    if_true: int
    if_false: int
    inspection_count: int = 0

    @classmethod
    def from_raw(cls, raw):
        monkey = Monkey(
            items=list(map(int, raw[1].split(': ')[1].split(', '))),
            operation=lambda old: eval(raw[2].split('new = ')[1]),
            divisor=int(raw[3].split('divisible by ')[1]),
            if_true=int(raw[4].split('throw to monkey ')[1]),
            if_false=int(raw[5].split('throw to monkey ')[1]),
        )
        return monkey

    def inspect_item(self, modulo, is_part2=False):
        self.inspection_count += 1
        item = self.items.pop(0)
        if is_part2:
            new_item = self.operation(item) % modulo
        else:
            new_item = (self.operation(item) % modulo) // 3
        other_monkey = (
            self.if_true if new_item % self.divisor == 0 else self.if_false
        )
        return new_item, other_monkey

    def receive_item(self, item):
        self.items.append(item)

    def __lt__(self, other):
        return self.inspection_count < other.inspection_count

    def __lte__(self, other):
        return self.inspection_count <= other.inspection_count


if __name__ == '__main__':
    main()
