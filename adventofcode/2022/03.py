# Python Standard Library Imports
import typing as T

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '03'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (8233, 2821)
TEST_VARIANT = ''  # '', 'b', 'c', 'd', ...
TEST_EXPECTED_ANSWERS = {
    '': (157, 70),
    'b': (None, None),
    'c': (None, None),
}

DEBUGGING = False
# DEBUGGING = True


def debug(*args):
    if DEBUGGING:
        print(*args)
    else:
        pass


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_coordinates=False,
        coordinate_delimeter=None,
        as_table=False,
        row_func=None,
        cell_func=None,
    )

    if TEST_MODE:
        input_filename = f'{PROBLEM_NUM}{TEST_VARIANT}.test.in'
        expected_answers = TEST_EXPECTED_ANSWERS[TEST_VARIANT]
    else:
        input_filename = f'{PROBLEM_NUM}.in'
        expected_answers = EXPECTED_ANSWERS

    solution = Solution(input_filename, input_config, expected_answers)

    solution.solve()
    solution.report()


class Solution(BaseSolution):
    def process_data(self):
        data = self.data

    def solve1(self) -> int:
        p_total = 0
        for sack in self.data:
            l = len(sack) // 2
            c1 = sack[:l]
            c2 = sack[l:]
            common = next(iter(set(c1) & set(c2)))
            p = priority(common)
            debug(common, p)
            p_total += p

        answer = p_total
        return answer

    def solve2(self) -> int:
        p_total = 0
        i = 0
        while i < len(self.data):
            c1, c2, c3 = self.data[i], self.data[i + 1], self.data[i + 2]
            common = next(iter(set(c1) & set(c2) & set(c3)))
            p = priority(common)
            debug(common, p)

            p_total += p
            i += 3

        answer = p_total
        return answer


def priority(letter: str) -> int:
    if 'a' <= letter <= 'z':
        return ord(letter) - ord('a') + 1
    elif 'A' <= letter <= 'Z':
        return ord(letter) - ord('A') + 27
    else:
        raise Exception(f"C'est impossible! {letter}")


if __name__ == '__main__':
    main()
