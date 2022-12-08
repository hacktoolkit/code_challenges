from utils import (
    BaseSolution,
    config,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (255, 55)
config.TEST_CASES = {
    '': (2, 2),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        self.strings = [NaughtyOrNice(s) for s in self.data]

    def solve1(self):
        answer = len(list(filter(lambda nn: nn.is_nice, self.strings)))
        return answer

    def solve2(self):
        answer = len(list(filter(lambda nn: nn.is_nice2, self.strings)))
        return answer


class NaughtyOrNice:
    VOWELS = 'aeiou'
    NAUGHTY = [
        'ab',
        'cd',
        'pq',
        'xy',
    ]

    def __init__(self, s):
        self.s = s

    @property
    def contains_naughty(self):
        contains_naughty = False
        for naughty in self.NAUGHTY:
            if naughty in self.s:
                contains_naughty = True
                break

        return contains_naughty

    @property
    def contains_3_vowels(self):
        vowels = [c for c in self.s if c in self.VOWELS]
        has_3 = len(vowels) >= 3
        return has_3

    @property
    def has_repeated_letters(self):
        has_repeat = False

        prev = None
        for c in self.s:
            if prev is not None and c == prev:
                has_repeat = True
                break
            prev = c

        return has_repeat

    @property
    def is_nice(self):
        is_nice = (
            not self.contains_naughty
            and self.contains_3_vowels
            and self.has_repeated_letters
        )
        return is_nice

    @property
    def has_distinct_repeating_pair(self):
        s = self.s
        has_repeat = False

        for i in range(len(s) - 4 + 1):
            pair = s[i : i + 2]
            for j in range(i + 2, len(s) - 2 + 1):
                pair2 = s[j : j + 2]
                if pair == pair2:
                    has_repeat = True
                    break

        return has_repeat

    @property
    def has_3_palindrome(self):
        has_repeat = False

        prev = None
        prev2 = None
        for c in self.s:
            if prev2 is not None and c == prev2:
                has_repeat = True
                break

            prev2 = prev
            prev = c

        return has_repeat

    @property
    def is_nice2(self):
        is_nice = self.has_distinct_repeating_pair and self.has_3_palindrome

        return is_nice


if __name__ == '__main__':
    main()
