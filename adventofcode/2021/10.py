# Python Standard Library Imports
from collections import defaultdict

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '10'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (319329, 3515583998, )
TEST_EXPECTED_ANSWERS = (26397, 288957, )


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
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
        self.command = Program(data)

    def solve1(self):
        answer = self.command.syntax_error_score
        return answer

    def solve2(self):
        answer = self.command.autocomplete_score
        return answer


class Program:
    OPENINGS = {
        '(': ')',
        '[': ']',
        '{': '}',
        '<': '>',
    }

    CLOSINGS = {
        ')': '(',
        ']': '[',
        '}': '{',
        '>': '<',
    }

    SYNTAX_ERROR_POINTS = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137,
    }

    COMPLETION_POINTS = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4,
    }

    def __init__(self, lines):
        self.lines = lines

        self._analyze()

    def _analyze(self):
        corrupt_chars = []
        incomplete_lines = []

        for line in self.lines:
            c = self.analyze_line(line)
            if c is None:
                incomplete_lines.append(line)
            else:
                corrupt_chars.append(c)

        self.incomplete_lines = incomplete_lines
        self.corrupt_chars = corrupt_chars

    @property
    def syntax_error_score(self):
        score = sum([
            self.SYNTAX_ERROR_POINTS[c]
            for c
            in self.corrupt_chars
        ])
        return score

    @property
    def autocomplete_score(self):
        completion_strings = [
            self.complete_line(line)
            for line
            in self.incomplete_lines
        ]
        scores = sorted([
            self.completion_string_score(completion_chars)
            for completion_chars
            in completion_strings
        ])
        score_index = (len(scores) - 1) // 2
        score = scores[score_index]

        return score

    def analyze_line(self, line):
        """Returns the first illegal character in a line, if any
        """
        illegal_char = None

        stack = []
        for c in line:
            if c in self.OPENINGS:
                stack.append(c)
            elif c in self.CLOSINGS:
                expected_pair = self.CLOSINGS[c]
                prev = stack[-1]

                if prev == expected_pair:
                    stack.pop(-1)
                else:
                    illegal_char = c
                    break

        return illegal_char

    def complete_line(self, incomplete_line):
        """
        """
        stack = []
        for c in incomplete_line:
            if c in self.OPENINGS:
                stack.append(c)
            elif c in self.CLOSINGS:
                expected_pair = self.CLOSINGS[c]
                prev = stack[-1]

                if prev == expected_pair:
                    stack.pop(-1)

        completion_chars = []
        while len(stack) > 0:
            c = stack.pop(-1)
            closing = self.OPENINGS[c]
            completion_chars.append(closing)

        return completion_chars

    def completion_string_score(self, completion_chars):
        total = 0
        for c in completion_chars:
            total *= 5
            total += self.COMPLETION_POINTS[c]
        return total


if __name__ == '__main__':
    main()
