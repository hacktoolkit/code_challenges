# Python Standard Library Imports
import copy
import itertools
import json
import math
from functools import reduce

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '18'

TEST_MODE = False
TEST_MODE = True

EXPECTED_ANSWERS = (4008, 4667, )
TEST_EXPECTED_ANSWERS = (4140, 3993, )


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
        self.test()

        data = self.data
        self.pairs = [json.loads(pair) for pair in self.data]

    def test(self):
        print('Running tests...')
        SnailfishNumber([9, [14, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]]])
        self.test_magnitude()
        self.test_sum()
        self.test_addition_pairwise()
        print('All tests passed!')

    def test_magnitude(self):
        test_cases = [
            ([[1,2],[[3,4],5]], 143),
            ([[[[0,7],4],[[7,8],[6,0]]],[8,1]], 1384),
            ([[[[1,1],[2,2]],[3,3]],[4,4]], 445),
            ([[[[3,0],[5,3]],[4,4]],[5,5]], 791),
            ([[[[5,0],[7,4]],[5,5]],[6,6]], 1137),
            ([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]], 3488),
        ]
        tests_run = 0
        for sfn, magnitude in test_cases:
            assert(SnailfishNumber(sfn).magnitude == magnitude)
            tests_run += 1

        assert(tests_run > 0)

    def test_sum(self):
        test_cases = [
            (
                (
                    [1,1],
                    [2,2],
                    [3,3],
                    [4,4],
                ),
                [[[[1,1],[2,2]],[3,3]],[4,4]],
            ),
            (
                (
                    [1,1],
                    [2,2],
                    [3,3],
                    [4,4],
                    [5,5],
                ),
                [[[[3,0],[5,3]],[4,4]],[5,5]],
            ),
            (
                (
                    [1,1],
                    [2,2],
                    [3,3],
                    [4,4],
                    [5,5],
                    [6,6],
                ),
                [[[[5,0],[7,4]],[5,5]],[6,6]],
            ),
            (
                (
                    [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
                    [7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
                    [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
                    [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
                    [7,[5,[[3,8],[1,4]]]],
                    [[2,[2,2]],[8,[8,1]]],
                    [2,9],
                    [1,[[[9,3],9],[[9,0],[0,7]]]],
                    [[[5,[7,4]],7],1],
                    [[[[4,2],2],6],[8,7]],
                ),
                [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]],
            ),
            (
                (
                    [[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]],
                    [[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]],
                ),
                [[[[7,8],[6,6]],[[6,0],[7,7]]],[[[7,8],[8,8]],[[7,9],[0,6]]]],
            ),
        ]

        tests_run = 0
        for sfns, expected in test_cases:
            snailfish_nums = [
                SnailfishNumber(sfn)
                for sfn
                in sfns
            ]
            snailfish_num = reduce(lambda a, b: a.add(b), snailfish_nums)
            assert(str(snailfish_num) == str(expected)), f'\nExpected:\n{expected}\nActual:\n{snailfish_num}'
            tests_run += 1

        assert(tests_run > 0)

    def test_addition_pairwise(self):
        test_cases = [
            (
                [[[[4,3],4],4],[7,[[8,4],9]]],
                [1,1],
                [[[[0,7],4],[[7,8],[6,0]]],[8,1]],
            ),
            (
                [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
                [7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
                [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]],
            ),
            (
                [[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]],
                [[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
                [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],
            ),
            (
                [[[[6,7],[6,7]],[[7,7],[0,7]]],[[[8,7],[7,7]],[[8,8],[8,0]]]],
                [[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
                [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],
            ),
            (
                [[[[7,0],[7,7]],[[7,7],[7,8]]],[[[7,7],[8,8]],[[7,7],[8,7]]]],
                [7,[5,[[3,8],[1,4]]]],
                [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]],
            ),
            (
                [[[[7,7],[7,8]],[[9,5],[8,7]]],[[[6,8],[0,8]],[[9,9],[9,0]]]],
                [[2,[2,2]],[8,[8,1]]],
                [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]],
            ),
            (
                [[[[6,6],[6,6]],[[6,0],[6,7]]],[[[7,7],[8,9]],[8,[8,1]]]],
                [2,9],
                [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]],
            ),
            (
                [[[[6,6],[7,7]],[[0,7],[7,7]]],[[[5,5],[5,6]],9]],
                [1,[[[9,3],9],[[9,0],[0,7]]]],
                [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]],
            ),
            (
                [[[[7,8],[6,7]],[[6,8],[0,8]]],[[[7,7],[5,0]],[[5,5],[5,6]]]],
                [[[5,[7,4]],7],1],
                [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]],
            ),
            (
                [[[[7,7],[7,7]],[[8,7],[8,7]]],[[[7,0],[7,7]],9]],
                [[[[4,2],2],6],[8,7]],
                [[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]],
            ),
        ]
        tests_run = 0
        for a, b, expected in test_cases:
            s = SnailfishNumber(a).add(SnailfishNumber(b))
            assert(s.pair == expected), f'\nExpected:\n{expected}\nActual:\n{s.pair}'
            tests_run += 1

        assert(tests_run > 0)

    def solve1(self):
        snailfish_nums = [SnailfishNumber(pair) for pair in self.pairs]

        snailfish_num = reduce(lambda a, b: a.add(b), snailfish_nums)
        answer = snailfish_num.magnitude
        return answer

    def solve2(self):
        max_magnitude = 0
        for a, b in itertools.permutations(self.pairs, 2):
            m = SnailfishNumber(a).add(SnailfishNumber(b)).magnitude
            if m > max_magnitude:
                max_magnitude = m

        answer = max_magnitude
        return answer


class SnailfishNumber:
    def __init__(self, pair):
        self.pair = copy.deepcopy(pair)
        self.reduce()

    def __str__(self):
        return str(self.pair)

    @property
    def magnitude(self):
        value = self.magnitude_of(self.pair)
        return value

    def magnitude_of(self, elt):
        if type(elt) == int:
            value = elt
        elif type(elt) == list:
            pair = elt
            left, right = elt
            value = 3 * self.magnitude_of(left) + 2 * self.magnitude_of(right)
        return value

    def add(self, other):
        return SnailfishNumber([copy.copy(self.pair), copy.copy(other.pair)])

    def reduce(self):
        """To reduce a snailfish number, you must repeatedly do the first action in this list that applies to the snailfish number:

        - If any pair is nested inside four pairs, the leftmost such pair explodes.
        - If any regular number is 10 or greater, the leftmost such regular number splits.
        """
        did_reduce = True
        while did_reduce:
            did_reduce = self.explode_if_nested_4() or self.split_if_ge_10()

    def explode_if_nested_4(self):
        did_reduce = False

        left, right = self.pair
        stack = []
        stack.append((right, [1]))  # FILO
        stack.append((left, [0]))  # LIFO: traverse left first

        while not did_reduce and len(stack) > 0:
            elt, indices = stack.pop()

            if type(elt) == int:
                # done traversing this part
                pass
            elif type(elt) == list:
                pair = elt
                if len(indices) >= 4:
                    self.explode(pair, indices)
                    did_reduce = True
                else:
                    left, right = pair
                    stack.append((right, indices + [1]))  # FILO
                    stack.append((left, indices + [0]))  # LIFO
            else:
                raise Exception('Illegal type')

        return did_reduce

    def split_if_ge_10(self):
        did_reduce = False

        left, right = self.pair
        stack = []
        stack.append((right, [1]))  # FILO
        stack.append((left, [0]))  # LIFO: traverse left first

        while not did_reduce and len(stack) > 0:
            elt, indices = stack.pop()

            if type(elt) == int:
                num = elt
                if num >= 10:
                    self.split(num, indices)
                    did_reduce = True
                else:
                    # done traversing this part
                    pass
            elif type(elt) == list:
                pair = elt
                left, right = pair
                stack.append((right, indices + [1]))  # FILO
                stack.append((left, indices + [0]))  # LIFO
            else:
                raise Exception('Illegal type')

        return did_reduce

    def update_node(self, item, indices):
        node = self.pair
        for index in indices[:-1]:
            node = node[index]

        node[indices[-1]] = item

    def add_to(self, num, indices):
        node = self.pair
        for index in indices[:-1]:
            node = node[index]

        node[indices[-1]] += num

    def is_num(self, indices):
        node = self.pair
        for index in indices:
            node = node[index]

        is_num = type(node) == int
        return is_num

    def explode(self, pair, indices):
        """To explode a pair, the pair's left value is added to the first regular number to the left of the exploding pair (if any), and the pair's right value is added to the first regular number to the right of the exploding pair (if any). Exploding pairs will always consist of two regular numbers. Then, the entire exploding pair is replaced with the regular number 0.
        """
        left, right = pair
        reg_num_indices_left = self.find_reg_num_indices_left(indices)
        reg_num_indices_right = self.find_reg_num_indices_right(indices)

        if reg_num_indices_left:
            self.add_to(left, reg_num_indices_left)

        if reg_num_indices_right:
            self.add_to(right, reg_num_indices_right)

        self.update_node(0, indices)

    def find_reg_num_indices_left(self, indices):
        indices = copy.copy(indices)
        reg_num_indices = None

        while len(indices) > 0 and reg_num_indices is None:
            if self.is_num(indices):
                reg_num_indices = indices
            else:
                index = indices.pop()
                if index == 1:
                    # right child, check left sibling or right-most child of left sibling
                    test_indices = indices + [0]
                    while not self.is_num(test_indices):
                        test_indices += [1]
                    reg_num_indices = test_indices
                elif index == 0:
                    # left child, continue to next loop
                    pass

        return reg_num_indices

    def find_reg_num_indices_right(self, indices):
        indices = copy.copy(indices)
        reg_num_indices = None

        while len(indices) > 0 and reg_num_indices is None:
            if self.is_num(indices):
                reg_num_indices = indices
            else:
                index = indices.pop()
                if self.is_num(indices):
                    reg_num_indices = indices
                elif index == 0:
                    # left child, check right sibling or left-most child of right sibling
                    test_indices = indices + [1]
                    while not self.is_num(test_indices):
                        test_indices += [0]

                    reg_num_indices = test_indices
                elif index == 1:
                    # right child, continue to next loop
                    pass

        return reg_num_indices

    def split(self, num, indices):
        """To split a regular number, replace it with a pair; the left element of the pair should be the regular number divided by two and rounded down, while the right element of the pair should be the regular number divided by two and rounded up. For example, 10 becomes [5,5], 11 becomes [5,6], 12 becomes [6,6], and so on.
        """
        new_pair = [
            int(math.floor(num / 2)),
            int(math.ceil(num / 2)),
        ]

        self.update_node(new_pair, indices)


if __name__ == '__main__':
    main()
