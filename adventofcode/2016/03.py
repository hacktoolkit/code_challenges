from utils import (
    InputConfig,
    ingest,
    transpose,
)


INPUT_FILE = '03.in'
EXPECTED_ANSWERS = (983, 1836, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE, InputConfig(as_table=True, cell_func=int))

    def solve1(self):
        valid_triangles = 0

        for values in self.data:
            a, b, c = sorted(values)
            if a + b > c:
                valid_triangles += 1

        answer = valid_triangles
        return answer

    def solve2(self):
        matrix = transpose(self.data)
        values = [
            col
            for row in matrix
            for col in row
        ]

        valid_triangles = 0

        for i in range(0, len(values), 3):
            a, b, c = sorted(values[i:i+3])
            if a + b > c:
                valid_triangles += 1

        answer = valid_triangles
        return answer


if __name__ == '__main__':
    main()
