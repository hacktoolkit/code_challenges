from utils import (
    BaseSolution,
    config,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (74, 1795)

config.INPUT_CONFIG.as_oneline = True


@solution
class Solution(BaseSolution):
    def process_data(self):
        self.instructions = self.data

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
