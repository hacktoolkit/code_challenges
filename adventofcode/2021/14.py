# Python Standard Library Imports
import itertools
from collections import defaultdict

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '14'

TEST_MODE = False
TEST_MODE = True

EXPECTED_ANSWERS = (3213, None, )
TEST_EXPECTED_ANSWERS = (1588, 2188189693529, )



def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=True,
        as_oneline=False,
        as_table=False,
        row_func=None,
        cell_func=None
    )

    if TEST_MODE:
        input_filename = f'{PROBLEM_NUM}.test.in'
        expected_answers = TEST_EXPECTED_ANSWERS
    else:
        input_filename = f'{PROBLEM_NUM}.in'
        expected_answers = EXPECTED_ANSWERS

    solution = Solution(input_filename, input_config, expected_answers)

    solution.solve()
    solution.report()


class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        raw_polymer, raw_rules = data

        self.polymer = raw_polymer[0]
        self.rules = dict([
            raw_rule.split(' -> ')
            for raw_rule
            in raw_rules
        ])

        self.step_n = 0

    def solve1(self):
        for _ in range(10):
            self.step()

        counts = defaultdict(int)
        for c in self.polymer:
            counts[c] += 1

        answer = max(list(counts.values())) - min(list(counts.values()))
        return answer

    def solve2(self):
        for _ in range(30):
            self.step()

        counts = defaultdict(int)
        for c in self.polymer:
            counts[c] += 1

        answer = max(list(counts.values())) - min(list(counts.values()))
        return answer

    def step(self):
        polymer = self.polymer
        rules = self.rules

        def mod_pair(pair):
            if pair in rules:
                result = pair[0] + rules[pair] + pair[1]
            else:
                result = pair
            return result

        new_pairs = [mod_pair(''.join(pair)) for pair in pairwise(polymer)]
        new_polymer = self.merge_pairs(new_pairs)

        self.polymer = new_polymer
        self.step_n += 1

    def merge_pairs(self, pairs):
        l = len(pairs)
        buf = []
        for i, pair in enumerate(pairs):
            if i == 0:
                buf.append(pair)
            else:
                buf.append(pair[1:])
        new_polymer = ''.join(buf)
        return new_polymer


if __name__ == '__main__':
    main()
