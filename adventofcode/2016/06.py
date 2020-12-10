# Python Standard Library Imports
from collections import defaultdict

from utils import ingest


INPUT_FILE = '06.in'
EXPECTED_ANSWERS = ('xdkzukcf', 'cevsgyvd', )

# INPUT_FILE = '06.test.in'
# EXPECTED_ANSWERS = ('easter', 'advent', )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)

    def solve1(self):
        words = self.data
        counts = [defaultdict(int) for x in range(len(words[0]))]

        for word in words:
            for i, c in enumerate(word):
                counts[i][c] += 1

        message = []
        for i in range(len(counts)):
            pairs = list(counts[i].items())
            sorted_pairs = sorted(pairs, key=lambda (letter, count): count, reverse=True)
            letter = sorted_pairs[0][0]
            message.append(letter)

        answer = ''.join(message)
        return answer

    def solve2(self):
        words = self.data
        counts = [defaultdict(int) for x in range(len(words[0]))]

        for word in words:
            for i, c in enumerate(word):
                counts[i][c] += 1

        message = []
        for i in range(len(counts)):
            pairs = list(counts[i].items())
            sorted_pairs = sorted(pairs, key=lambda (letter, count): count)
            letter = sorted_pairs[0][0]
            message.append(letter)

        answer = ''.join(message)
        return answer


if __name__ == '__main__':
    main()
