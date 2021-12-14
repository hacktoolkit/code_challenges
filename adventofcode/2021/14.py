# Python Standard Library Imports
import time
from collections import (
    Counter,
    defaultdict,
)

from utils import (
    BaseSolution,
    InputConfig,
    pairwise,
)


PROBLEM_NUM = '14'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (3213, 3711743744429, )
TEST_EXPECTED_ANSWERS = (1588, 2188189693529, )


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

        self.original_polymer = raw_polymer[0]
        self.polymer = self.original_polymer
        self.rules = dict([
            raw_rule.split(' -> ')
            for raw_rule
            in raw_rules
        ])

    def reset(self):
        self.step_n = 0
        self.polymer = self.original_polymer

    def solve1(self):
        self.reset()
        for _ in range(10):
            self.step()

        counts = Counter(self.polymer)
        values = counts.values()
        answer = max(values) - min(values)
        return answer

    def solve2(self):
        self.reset()
        answer = self.fast_step(40)
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
        buf = []
        for i, pair in enumerate(pairs):
            if i == 0:
                buf.append(pair)
            else:
                buf.append(pair[1:])
        new_polymer = ''.join(buf)
        return new_polymer

    def iter_pairs(self, s):
        for pair in pairwise(s):
            yield ''.join(pair)

    def fast_step(self, n):
        polymer = self.polymer
        rules = self.rules

        pairs_count = Counter(self.iter_pairs(polymer))

        for _ in range(n):
            next_pairs_count = defaultdict(int)
            for pair, count in pairs_count.items():
                if pair not in rules:
                    next_pairs_count[pair] = count
                else:
                    a, b = pair[0], pair[1]
                    c = rules[pair]
                    next_pairs_count[a + c] += count
                    next_pairs_count[c + b] += count

            pairs_count = next_pairs_count

        counts = defaultdict(int)
        for pair, count in pairs_count.items():
            # sufficient to just track the first letter of each pair
            # to prevent double-counting of the middle characters
            counts[pair[0]] += count

        # adds on the last character
        counts[self.polymer[-1]] += 1

        values = counts.values()
        result = max(values) - min(values)
        return result


if __name__ == '__main__':
    main()
