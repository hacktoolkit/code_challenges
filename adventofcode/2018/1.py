from utils import ingest


INPUT_FILE = '1.in'
EXPECTED_ANSWERS = (525, 75749, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        data = ingest(INPUT_FILE)

        self.numbers = [
            int(num[1:]) * (1 if num[0] == '+' else -1)
            for num
            in data
        ]

    def solve1(self):
        answer = sum(self.numbers)
        return answer

    def solve2(self):
        answer = None

        visited = {
            0: True,
        }

        frequency = 0

        index = 0

        while answer is None:
            n = self.numbers[index]
            frequency += n

            if frequency in visited:
                answer = frequency
                break
            else:
                visited[frequency] = True

            index = (index + 1) % len(self.numbers)

        return answer


if __name__ == '__main__':
    main()
