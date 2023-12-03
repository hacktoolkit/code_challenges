# Python Standard Library Imports
import copy
import heapq
import math
import re
import typing as T
from collections import (
    defaultdict,
    deque,
)
from dataclasses import (
    dataclass,
    field,
)
from functools import (
    cache,
    lru_cache,
)
from itertools import (
    combinations,
    permutations,
    product,
)
from operator import (
    add,
    mul,
)

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (56506, None)
config.TEST_CASES = {
    # '': (142, 142),
    'b': (209, 281),
    # 'c': (None, None),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        self.doc = CalibrationDoc(self.data)

    def solve1(self):
        answer = sum(self.doc.calibration_values)
        return answer

    def solve2(self):
        answer = sum(self.doc.calibration_values_with_word_digits)
        return answer


class CalibrationDoc:
    NUMBERS = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
    }

    def __init__(self, data):
        self.data = data

    @property
    def calibration_values(self):
        return self.extract_calibration_values()

    @property
    def calibration_values_with_word_digits(self):
        return self.extract_calibration_values(word_digits=True)

    def extract_calibration_values(self, word_digits=False):
        values = [
            self._extract_value(line, word_digits=word_digits)
            for line in self.data
        ]
        return values

    def _extract_value(self, raw_line, word_digits=False):
        line = (
            self._convert_words_to_digits(raw_line) if word_digits else raw_line
        )
        digits = [c for c in line if c.isdigit()] or [0]
        value = int(str(digits[0]) + str(digits[-1]))
        return value

    def _convert_words_to_digits(self, raw_line):
        line = raw_line

        did_replace = True

        while did_replace:
            # replacements happen left to right
            indexes = sorted(
                [
                    (index, word)
                    for word, digit in self.NUMBERS.items()
                    if (index := line.find(word)) >= 0
                ],
                key=lambda x: x[0],
            )

            if len(indexes) > 0:
                _, word = indexes[0]
                line = line.replace(word, str(self.NUMBERS[word]))
                did_replace = True
            else:
                did_replace = False

        print(raw_line, line)

        return line


if __name__ == '__main__':
    main()
