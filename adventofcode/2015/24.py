# Python Standard Library Imports
import copy
import itertools
import math
import pathlib

# Third Party (PyPI) Imports
import click

from utils import (
    BaseSolution,
    InputConfig,
)


YEAR = int(pathlib.Path.cwd().parts[-1])
DAY = int(pathlib.Path(__file__).stem)
PROBLEM_NUM = str(DAY).zfill(2)


TEST_MODE = True

EXPECTED_ANSWERS = (10439961859, 72050269)
TEST_VARIANT = ''  # '', 'b', 'c', 'd', ...
TEST_EXPECTED_ANSWERS = {
    '': (99, 44),
    'b': (None, None),
    'c': (None, None),
}

DEBUGGING = False


def debug(*args):
    if DEBUGGING:
        print(*args)
    else:
        pass


@click.command()
@click.option('--is_real', '--real', is_flag=True, default=False)
@click.option('--submit', is_flag=True, default=False)
@click.option('--is_debug', '--debug', is_flag=True, default=False)
def main(is_real, submit, is_debug):
    global TEST_MODE
    global DEBUGGING
    TEST_MODE = not is_real
    DEBUGGING = is_debug

    input_config = InputConfig(
        as_integers=True,
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

    solution = Solution(
        input_filename,
        input_config,
        expected_answers,
        year=YEAR,
        day=DAY,
    )

    solution.solve()
    if submit:
        solution.submit(is_test=TEST_MODE)
    solution.report()


class Solution(BaseSolution):
    def process_data(self):
        data = self.data

    def solve1(self):
        sleigh = Sleigh(self.data, 3)
        optimal_arrangement = sleigh.find_optimal_arrangement()

        answer = optimal_arrangement.quantum_entanglement
        return answer

    def solve2(self):
        sleigh = Sleigh(self.data, 4)
        optimal_arrangement = sleigh.find_optimal_arrangement()

        answer = optimal_arrangement.quantum_entanglement
        return answer


class Sleigh:
    def __init__(self, weights, num_groups):
        self.weights = sorted(weights, reverse=True)
        self.num_groups = num_groups
        self.limit = sum(weights) // num_groups

        min_arrangement_size = 0
        subtotal = 0
        while subtotal < self.limit:
            subtotal += self.weights[min_arrangement_size]
            min_arrangement_size += 1

        self.min_arrangement_size = min_arrangement_size
        self.max_arrangement_size = (
            len(self.weights) - (num_groups - 1) * self.min_arrangement_size
        )

        debug(
            'Num Groups',
            num_groups,
            'Weights',
            len(self.weights),
            'Limit',
            self.limit,
            'Min arrangement size',
            min_arrangement_size,
            'Max arrangement size',
            self.max_arrangement_size,
        )

    class Arrangement:
        def __init__(self, weights):
            self.weights = weights
            self.key = tuple(sorted(weights))

        def __hash__(self):
            return hash(self.key)

        @property
        def quantum_entanglement(self):
            return math.prod(self.weights)

        def __lt__(self, other):
            result = len(self.weights) < len(other.weights) or (
                len(self.weights) == len(other.weights)
                and self.quantum_entanglement < other.quantum_entanglement
            )
            return result

        def __gt__(self, other):
            result = len(self.weights) > len(other.weights) or (
                len(self.weights) == len(other.weights)
                and self.quantum_entanglement > other.quantum_entanglement
            )
            return result

        def __eq__(self, other):
            result = (
                len(self.weights) == len(other.weights)
                and self.quantum_entanglement == other.quantum_entanglement
            )
            return result

    def find_optimal_arrangement(self):
        # arrangements = self.make_arrangements__iter()
        arrangements = self.make_arrangements__combos()
        optimal_arrangement = sorted(arrangements)[0]
        return optimal_arrangement

    def make_arrangements__combos(self):
        arrangements = set()

        for l in range(
            self.min_arrangement_size, self.max_arrangement_size + 1
        ):
            for c in itertools.combinations(self.weights, l):
                if sum(c) == self.limit:
                    arrangements.add(self.Arrangement(c))

            if len(arrangements) > 0:
                # the winning arrangement must be among the current set
                break

        return arrangements

    def make_arrangements__iter(
        self, remain_weights=None, used_weights=None, limit=None
    ):
        """While the large problem is to find all arrangments:

        `[c1, c2, c3]` such that `sum(c1) == sum(c2) == sum(c3) == self.limit`

        An optimization can be made to simply find all _possible_ arrangements for 1 compartment
        """
        if remain_weights is None:
            remain_weights = self.weights

        if used_weights is None:
            used_weights = set()

        if limit is None:
            limit = None

        arrangements = self.make_sub_arrangements(
            remain_weights, used_weights, limit=self.limit
        )

        return arrangements

    def make_sub_arrangements(self, remain_weights, used_weights, limit):
        arrangements = set()

        if limit == 0:
            # print('got here')
            arrangements.add(self.Arrangement(used_weights))
        elif len(remain_weights) == 0:
            print('case b')
            # no more weights to add, incomplete arrangement
            pass
        else:
            # print('case c')
            for w in sorted(remain_weights, reverse=True):
                if w <= limit:
                    next_remain_weights = copy.copy(remain_weights)
                    next_remain_weights.remove(w)
                    next_used_weights = copy.copy(used_weights)
                    next_used_weights.add(w)
                    next_limit = limit - w

                    arrangements = arrangements.union(
                        self.make_sub_arrangements(
                            next_remain_weights,
                            next_used_weights,
                            next_limit,
                        )
                    )
                else:
                    # weight w is too large for arrangement
                    pass

        return arrangements


if __name__ == '__main__':
    main()
