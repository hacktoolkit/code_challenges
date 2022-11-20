# Python Standard Library Imports
import copy
import math
import re
from collections import defaultdict
from dataclasses import dataclass

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '05'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (
    11194,
    4178,
)
TEST_EXPECTED_ANSWERS = (
    10,
    4,
)

DEBUGGING = False
DEBUGGING = True


def debug(s):
    if DEBUGGING:
        print(s)
    else:
        pass


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=False,
        row_func=None,
        cell_func=None,
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
        self.polymer = data[0]

    def solve1(self):
        # polymer = PolymerLab.react_naive(self.polymer)
        polymer = PolymerLab.react(self.polymer)

        debug(polymer)
        answer = len(polymer)
        return answer

    def solve2(self):
        variants = set()

        shortest_polymer = None
        shortest_length = None

        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        for letter in alphabet:
            print(f'Variant: {letter}/{letter.upper()} removed')
            variant = re.sub(rf'[{letter}{letter.upper()}]', '', self.polymer)
            if variant in variants:
                # already seen, skip
                pass
            else:
                variants.add(variant)

                polymer = PolymerLab.react(variant)
                l = len(polymer)
                print(f'Length: {l}')
                if shortest_polymer is None or l < shortest_length:
                    shortest_polymer = polymer
                    shortest_length = l
                    debug('Found shorter result')

        debug(shortest_polymer)
        answer = shortest_length
        return answer


class PolymerLab:
    @classmethod
    def react_naive(cls, polymer):
        did_change = True
        while did_change:
            did_change = False
            for i in range(len(polymer) - 1):
                a = polymer[i]
                b = polymer[i + 1]
                if a != b and a.lower() == b.lower():
                    # make it go poof
                    polymer = polymer[:i] + polymer[i + 2 :]
                    did_change = True
                    break

        return polymer

    @classmethod
    def react(cls, polymer):
        sequence = [c for c in polymer]

        did_change = True
        while did_change:
            did_change = False

            i = 0
            while i < len(sequence) - 1:
                while i < len(sequence) - 1 and sequence[i] is None:
                    i += 1

                j = i + 1
                while j < len(sequence) and sequence[j] is None:
                    j += 1

                if i < len(sequence) and j < len(sequence):
                    a = sequence[i]
                    b = sequence[j]
                    if a != b and a.lower() == b.lower():
                        # make it go poof
                        sequence[i] = None
                        sequence[j] = None
                        did_change = True
                        i = j + 1
                    else:
                        i += 1
                else:
                    i += 1

            sequence = list(filter(None, sequence))

        polymer = ''.join(sequence)
        return polymer


if __name__ == '__main__':
    main()
