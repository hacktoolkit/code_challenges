# Python Standard Library Imports
from collections import defaultdict

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '08'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (274, 1012089, )
TEST_EXPECTED_ANSWERS = (26, 61229, )


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=False,
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

        self.searches = [Search(entry) for entry in self.data]

    def solve1(self):
        easy_digits = [
            digit
            for search in self.searches
            for s in search.seven_segs
            if (digit := s.digit) in (1, 4, 7, 8,)
        ]

        answer = len(easy_digits)
        return answer

    def solve2(self):
        answer = sum([search.number for search in self.searches])
        return answer


SIMPLE_SEGMENTS = {
    2: 1,
    3: 7,
    4: 4,
    7: 8,
}


NON_SIMPLE_SEGMENTS = {
    1: [],
    5: [2, 3, 5, ],
    6: [0, 6, 9,],
}


class Search:
    def __init__(self, entry):
        unique_signal_patterns_in, output_values_in = [_.strip() for _ in entry.split('|')]

        self.unique_signal_patterns = [
            (pattern := sorted(_.strip()))
            for _
            in unique_signal_patterns_in.split(' ')
        ]

        self.wire_map = {
            'a': None,
            'b': None,
            'c': None,
            'd': None,
            'e': None,
            'f': None,
            'g': None,
        }
        self.decode_wires()

        self.outputs = [_.strip() for _ in output_values_in.split(' ')]
        self.seven_segs = [
            SevenSegmentDisplay(self.remap(pattern))
            for pattern
            in self.outputs
        ]

    def decode_wires(self):
        """Figure out which wire is which!
        """
        buckets_by_num_segments = defaultdict(list)

        for pattern in self.unique_signal_patterns:
            buckets_by_num_segments[len(pattern)].append(pattern)

        ##
        # disambiguate wires with single patterns

        # 1, 7, 4, 8
        one = buckets_by_num_segments[2][0]
        seven = buckets_by_num_segments[3][0]
        four = buckets_by_num_segments[4][0]
        eight = buckets_by_num_segments[7][0]

        # wire 'a': '7' - '1'
        a = list(set(seven) - set(one))[0]
        self.wire_map['a'] = a

        # numbers with multiple candidates
        two_three_five = buckets_by_num_segments[5]
        zero_six_nine = buckets_by_num_segments[6]

        # wire 'd': intersection of '2', '3', '5', '4'
        d_set = set(four)
        for pattern in two_three_five:
            d_set = d_set & set(pattern)
        d = list(d_set)[0]
        self.wire_map['d'] = d

        # wire 'b': '4' - '1' - 'd'
        b = list(set(four) - set(one) - {d})[0]
        self.wire_map['b'] = b

        # '5': the only one out of '2', '3', '5' which contains 'b'
        five = None
        for pattern in two_three_five:
            if b in pattern:
                five = pattern
                break

        # wire 'g': '5' - '4' - 7'
        g = list(set(five) - set(four) - set(seven))[0]
        self.wire_map['g'] = g

        # wire 'f': '5' - 'a' - 'b' - 'd' - 'g'
        f = list(set(five) - {a, b, d, g})[0]
        self.wire_map['f'] = f

        # wire 'c': '1' - 'f'
        c = list(set(one) - {f})[0]
        self.wire_map['c'] = c

        # wire 'e': the only remaining wire
        # wire 'e': '2' - 'a' - 'c' - 'd' - 'g'
        e = list(set([c for c in 'abcdefg']) - {a, b, c, d, f, g,})[0]
        self.wire_map['e'] = e

        self.inverse_wire_map = { v: k for k, v in self.wire_map.items() }

    def remap(self, pattern):
        """Remaps a seven segment digit signal pattern to a canonical wiring pattern
        """
        mapped = ''.join([self.inverse_wire_map[w] for w in pattern])
        return mapped

    @property
    def number(self):
        digits = [str(s.digit) for s in self.seven_segs]
        num = int(''.join(digits))
        return num


class SevenSegmentDisplay:
    """

    https://en.wikipedia.org/wiki/Seven-segment_display

      0:      1:      2:      3:      4:
     aaaa    ....    aaaa    aaaa    ....
    b    c  .    c  .    c  .    c  b    c
    b    c  .    c  .    c  .    c  b    c
     ....    ....    dddd    dddd    dddd
    e    f  .    f  e    .  .    f  .    f
    e    f  .    f  e    .  .    f  .    f
     gggg    ....    gggg    gggg    ....

      5:      6:      7:      8:      9:
     aaaa    aaaa    aaaa    aaaa    aaaa
    b    .  b    .  .    c  b    c  b    c
    b    .  b    .  .    c  b    c  b    c
     dddd    dddd    ....    dddd    dddd
    .    f  e    f  .    f  e    f  .    f
    .    f  e    f  .    f  e    f  .    f
     gggg    gggg    ....    gggg    gggg

    """
    MAP = {
        'abcefg': 0,
        'cf': 1,
        'acdeg': 2,
        'acdfg': 3,
        'bcdf': 4,
        'abdfg': 5,
        'abdefg': 6,
        'acf': 7,
        'abcdefg': 8,
        'abcdfg': 9,
    }

    def __init__(self, pattern):
        self.pattern = pattern
        self.canonical_pattern = ''.join(sorted(pattern))

    @property
    def digit(self):
        num_segments = len(self.pattern)
        if num_segments in SIMPLE_SEGMENTS:
            digit = SIMPLE_SEGMENTS[num_segments]
        elif self.canonical_pattern in self.MAP:
            digit = self.MAP[self.canonical_pattern]
        else:
            digit = None
        return digit


if __name__ == '__main__':
    main()
