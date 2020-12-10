from utils import ingest


INPUT_FILE = '01.in'
EXPECTED_ANSWERS = (1343, 1274, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE, as_oneline=True)

    def solve1(self):
        digits = self.data

        total = 0
        for i, c in enumerate(digits):
            digit = int(c)
            j = (i + 1) % len(digits)
            next_digit = int(digits[j])
            if digit == next_digit:
                total += digit

        answer = total
        return answer

    def solve2(self):
        digits = self.data

        total = 0
        for i, c in enumerate(digits):
            digit = int(c)
            j = (i + (len(digits) / 2)) % len(digits)
            next_digit = int(digits[j])
            if digit == next_digit:
                total += digit

        answer = total
        return answer


if __name__ == '__main__':
    main()
