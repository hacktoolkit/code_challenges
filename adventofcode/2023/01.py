# Python Standard Library Imports
import re
import typing as T

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (56506, 56017)
config.TEST_CASES = {
    # '': (142, 142),
    'b': (209, 281),
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

    def _convert_words_to_digits(
        self, raw_line: str, allow_overlaps: bool = True, direction: str = 'ltr'
    ):
        """Converts a line containing letters and numbers to a line with
        its number-words converted to digits

        The problem description is quite terrible because it is ambiguous
        whether overlaps are allowed or not.

        If someone made the assumption that overlaps were not allowed (like I did),
        then time would be wasted on an implemenetation that didn't allow
        overlaps.
        """
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
                reverse=direction == 'rtl',
            )

            if len(indexes) > 0:
                _, word = indexes[0]
                replacement = str(self.NUMBERS[word])
                if allow_overlaps:
                    # if overlaps are allowed,
                    # replace the number word with the number,
                    # plus the last letter of the word (for LTR)
                    replacement += word[-1]

                line = line.replace(word, replacement)
                did_replace = True
            else:
                did_replace = False

        return line


if __name__ == '__main__':
    main()
