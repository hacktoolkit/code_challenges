from utils import (
    InputConfig,
    ingest,
)


INPUT_FILE = '01.in'
EXPECTED_ANSWERS = (74, 1795, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        data = ingest(INPUT_FILE, InputConfig(as_oneline=True))
        self.instructions = data

    def solve1(self):
        floor = 0
        for c in self.instructions:
            floor += 1 if c == '(' else -1 if c == ')' else 0

        answer = floor
        return answer

    def solve2(self):
        answer = None

        floor = 0
        for position, c in enumerate(self.instructions):
            floor += 1 if c == '(' else -1 if c == ')' else 0
            if floor == -1:
                answer = position + 1
                break

        return answer


if __name__ == '__main__':
    main()
