# Python Standard Library Imports
from functools import cached_property

from utils import (
    BaseSolution,
    InputConfig,
    config,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (21138, 7185540)
config.TEST_CASES = {
    '': (13, 30),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        self.scratch_cards = [ScratchCard(line) for line in self.data]

    def solve1(self):
        answer = sum(scratch_card.score for scratch_card in self.scratch_cards)
        return answer

    def solve2(self):
        card_counts = {
            scratch_card.card_id: 1 for scratch_card in self.scratch_cards
        }

        num_cards = len(self.scratch_cards)

        total_num_additional_cards = 0
        for i, scratch_card in enumerate(self.scratch_cards, 1):
            count = card_counts[scratch_card.card_id]
            num_additional_cards = min(scratch_card.num_matches, num_cards - i)
            for k in range(num_additional_cards):
                bonus_card_id = i + 1 + k
                card_counts[bonus_card_id] += count

        answer = sum(card_counts.values())
        return answer


class ScratchCard:
    def __init__(self, raw):
        card_heading, numbers = raw.split(':')

        self.card_id = int(card_heading.split()[1].strip())

        raw_winning_numbers, raw_numbers = numbers.split('|')
        self.winning_numbers = [
            int(_) for _ in raw_winning_numbers.split() if _.isnumeric()
        ]
        self.numbers = [int(_) for _ in raw_numbers.split() if _.isnumeric()]

    @cached_property
    def num_matches(self):
        matches = set(self.winning_numbers) & set(self.numbers)
        num_matches = len(matches)
        return num_matches

    @property
    def score(self):
        score = 0 if self.num_matches == 0 else 2 ** (self.num_matches - 1)
        return score


if __name__ == '__main__':
    main()
