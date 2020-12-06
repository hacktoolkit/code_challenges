from utils import ingest


INPUT_FILE = 'n.in'
EXPECTED_ANSWERS = (None, None, )

# INPUT_FILE = 'n.test.in'
# EXPECTED_ANSWERS = (None, None, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)

    def solve1(self):
        answer = None
        return answer

    def solve2(self):
        answer = None
        return answer


if __name__ == '__main__':
    main()
