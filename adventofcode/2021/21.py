# Python Standard Library Imports
from dataclasses import dataclass
from functools import cache

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '21'

TEST_MODE = False
TEST_MODE = True

EXPECTED_ANSWERS = (1006866, 273042027784929, )
TEST_EXPECTED_ANSWERS = (739785, 444356092776315, )


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
        self.p1_start = int(data[0].split(' ')[-1])
        self.p2_start = int(data[1].split(' ')[-1])

    def solve1(self):
        dice = DeterministicDice(self.p1_start, self.p2_start)

        while not dice.has_winner:
            dice.play()

        answer = dice.losing_score
        return answer

    def solve2(self):
        dice = DiracDice()
        wins = dice.play(self.p1_start, self.p2_start)
        answer = max(wins)
        return answer


@dataclass
class DeterministicDice:
    p1_pos: int
    p2_pos: int
    winning_score: int = 1000
    p1_score: int = 0
    p2_score: int = 0
    turn: int = 1
    num_rolls: int = 0
    next_throw: int = 1

    def roll(self):
        rolls = [
            n if n <= 100 else n % 100
            for n
            in range(self.next_throw, self.next_throw + 3)
        ]
        self.next_throw = (self.next_throw + 3 - 1) % 100 + 1
        self.num_rolls += 3
        return rolls

    def move(self, player, spaces):
        if player == 1:
            self.p1_pos = (self.p1_pos + spaces - 1) % 10 + 1
            self.p1_score += self.p1_pos
        elif player == 2:
            self.p2_pos = (self.p2_pos + spaces - 1) % 10 + 1
            self.p2_score += self.p2_pos
        else:
            raise Exception('Illegal player')

    def play(self):
        rolls = self.roll()
        moves = sum(rolls)
        player = 1 if self.turn == 1 else 2
        self.move(player, moves)
        self.turn = self.turn % 2 + 1

    @property
    def p1_won(self):
        return self.p1_score >= self.winning_score

    @property
    def p2_won(self):
        return self.p2_score >= self.winning_score

    @property
    def has_winner(self):
        return self.p1_won or self.p2_won

    @property
    def losing_score(self):
        loser_score = self.p2_score if self.p1_won else self.p1_score
        score = loser_score * self.num_rolls
        return score


class DiracDice:
    WINNING_SCORE = 21

    @cache
    def play(self, p1_pos, p2_pos, p1_score=0, p2_score=0):
        # Observation: even though the dice rolls are not "deterministic,"
        # for a given input (player positions and scores), the outcomes are deterministic
        # Each turn is symmetrical, so this cuts down on the computational complexity
        wins = [0, 0]

        for roll_score in self.roll():
            next_p1_pos = (p1_pos + roll_score - 1) % 10 + 1
            next_p1_score = p1_score + next_p1_pos
            if next_p1_score >= DiracDice.WINNING_SCORE:
                wins[0] += 1
            else:
                # recursively play, swap players and scores
                wins2, wins1 = self.play(
                    p2_pos,
                    next_p1_pos,
                    p1_score=p2_score,
                    p2_score=next_p1_score
                )
                wins[0] += wins1
                wins[1] += wins2

        return wins

    @cache
    def roll(self):
        universes = [1, 2, 3]
        roll_sums = [x + y + z for x in universes for y in universes for z in universes]
        return roll_sums


if __name__ == '__main__':
    main()
