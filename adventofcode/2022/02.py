# Python Standard Library Imports
import typing as T
from dataclasses import dataclass
from enum import Enum

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '02'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (10994, 12526)
TEST_VARIANT = ''  # '', 'b', 'c', 'd', ...
TEST_EXPECTED_ANSWERS = {
    '': (15, 12),
    'b': (None, None),
    'c': (None, None),
}

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

    def solve1(self):
        # A, X: Rock
        # B, Y: Paper
        # C, Z: Scissors
        total_score = 0
        for pair in self.data:
            abc, xyz = pair.split()
            p1 = RPSGame.Form(ord(abc) - ord('A') + 1)
            p2 = RPSGame.Form(ord(xyz) - ord('X') + 1)
            result = RPSGame.find_wlt(p1, p2)
            score = p2.value + result.value
            total_score += score

        answer = total_score
        return answer

    def solve2(self):
        total_score = 0
        for pair in self.data:
            abc, xyz = pair.split()
            p1 = RPSGame.Form(ord(abc) - ord('A') + 1)
            result = RPSGame.Result.from_alias(xyz)
            p2 = RPSGame.find_p2(p1, result)
            score = p2.value + result.value
            total_score += score

        answer = total_score
        return answer


class RPSGame:
    class Form(Enum):
        Rock = 1
        Paper = 2
        Scissors = 3

        @classmethod
        def win_map(cls) -> dict['RPGGame.Form', 'RPGGame.Form']:
            win_map = {
                cls.Rock: cls.Scissors,
                cls.Paper: cls.Rock,
                cls.Scissors: cls.Paper,
            }
            return win_map

        @classmethod
        def loss_map(cls) -> dict['RPGGame.Form', 'RPGGame.Form']:
            win_map = cls.win_map()
            loss_map = {v: k for k, v in win_map.items()}
            return loss_map

        def ties(self, other: 'RPGGame.Form') -> bool:
            return self == other

        def wins(self, other: 'RPGGame.Form') -> bool:
            wins = not self.ties(other) and self.wins_against == other
            return wins

        @property
        def wins_against(self) -> 'RPGGame.Form':
            win_map = self.__class__.win_map()
            losing_opponent = win_map[self]
            return losing_opponent

        @property
        def loses_to(self) -> 'RPGGame.Form':
            loss_map = self.__class__.loss_map()
            winning_opponent = loss_map[self]
            return winning_opponent

    class Result(Enum):
        Loss = 0
        Tie = 3
        Win = 6

        @classmethod
        def from_alias(cls, alias: str) -> 'RPSGame.Result':
            aliases = {
                'X': cls.Loss,
                'Y': cls.Tie,
                'Z': cls.Win,
            }
            result = aliases[alias]
            return result

    @classmethod
    def find_wlt(
        cls, p1: 'RPSGame.Form', p2: 'RPSGame.Form'
    ) -> 'RPSGame.Result':
        Result = cls.Result
        result = (
            Result.Tie
            if p2.ties(p1)
            else Result.Win
            if p2.wins(p1)
            else Result.Loss
        )
        return result

    @classmethod
    def find_p2(
        cls, p1: 'RPSGame.Form', result: 'RPSGame.Result'
    ) -> 'RPSGame.Form':
        Form = cls.Form
        Result = cls.Result

        p2 = (
            p1
            if result == Result.Tie
            else p1.loses_to
            if result == Result.Win
            else p1.wins_against
        )
        return p2


if __name__ == '__main__':
    main()
