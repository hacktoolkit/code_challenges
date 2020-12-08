from utils import ingest


INPUT_FILE = '2.in'
EXPECTED_ANSWERS = (36174, 244, )

# INPUT_FILE = '2.test.in'
# EXPECTED_ANSWERS = (18, 9, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE, as_table=True, cell_func=int)

    def solve1(self):
        table = self.data

        checksum = 0

        for row in table:
            row_checksum = max(row) - min(row)
            checksum += row_checksum

        answer = checksum
        return answer

    def solve2(self):
        table = self.data

        checksum = 0

        for row in table:
            values = sorted(row, reverse=True)
            for i in range(len(values)):
                for j in range(i + 1, len(values)):
                    a, b = values[i], values[j]
                    if a % b == 0:
                        quotient = a / b
                        checksum += quotient

        answer = checksum
        return answer


if __name__ == '__main__':
    main()
