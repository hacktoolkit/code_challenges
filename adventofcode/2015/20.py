# Python Standard Library Imports
import copy
import math
import re
from collections import defaultdict
from dataclasses import dataclass

from utils import (
    BaseSolution,
    InputConfig,
    factors_of,
)


PROBLEM_NUM = '20'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (776160, None)
TEST_VARIANT = ''  # '', 'b', 'c', 'd', ...
TEST_EXPECTED_ANSWERS = {
    '': (8, 8),
    'b': (None, None),
    'c': (None, None),
}

DEBUGGING = False
# DEBUGGING = True


def debug(s):
    if DEBUGGING:
        print(s)
    else:
        pass


def main():
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

    solution = Solution(input_filename, input_config, expected_answers)

    solution.solve()
    solution.report()


class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        self.target_num_presents = data[0]

    def solve1(self):
        print(self.target_num_presents)
        # house = Elves.lowest_house_receiving_n_presents__naive(
        #     self.target_num_presents
        # )
        house = Elves.lowest_house_receiving_n_presents(
            self.target_num_presents
        )
        answer = house
        return answer

    def solve2(self):
        house = Elves.lowest_house_receiving_n_presents(
            self.target_num_presents, elf_visits=50, presents_per_elf=11
        )
        answer = house
        return answer


class Elves:
    @classmethod
    def num_presents(cls, house):
        """Calculate the number of presents `house` receives

        `house` is a positive integer
        """
        factors = factors_of(house)
        # debug(f'Factors of {house}: {factors}')

        num_presents = sum([factor * 10 for factor in factors])
        return num_presents

    @classmethod
    def lowest_house_receiving_n_presents__naive(cls, n):
        house = 0
        num_presents = 0

        while num_presents < n:
            house += 1
            num_presents = cls.num_presents(house)
            debug(f'House {house} got {num_presents} presents.')

        return house

    @classmethod
    def lowest_house_receiving_n_presents(
        cls, n, elf_visits=None, presents_per_elf=10
    ):
        """Solves using step-wise approach, inspired by sieve of Erastothnes

        https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes

        In the worst-case theoretical scenario, will need to check at least `n/10` houses/elves
        """
        presents_at = defaultdict(int)

        house_with_n_presents = None

        upper = n // 10

        # fill out like a "sieve"
        for elf in range(1, upper + 1):
            num_visits = 0  # part 2
            for house in range(elf, upper + 1, elf):
                presents_at[house] += elf * presents_per_elf

                if presents_at[house] >= n:
                    # optimization: tighten the bounds
                    upper = house

                # part 2
                num_visits += 1
                if elf_visits and num_visits >= elf_visits:
                    break

        # find first (lowest) house number receiving at least `n` presents
        for house in range(1, upper + 1):
            if presents_at[house] >= n:
                house_with_n_presents = house
                break

        return house_with_n_presents


if __name__ == '__main__':
    main()
