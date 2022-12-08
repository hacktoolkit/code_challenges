# Python Standard Library Imports
from enum import Enum

from utils import (
    BaseSolution,
    config,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (10994, 12526)
config.TEST_CASES = {
    '': (15, 12),
}


@solution
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
