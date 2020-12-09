from utils import ingest


INPUT_FILE = '9.in'
PREAMBLE_LENGTH = 25
EXPECTED_ANSWERS = (26134589, 3535124, )

# INPUT_FILE = '9.test.in'
# PREAMBLE_LENGTH = 5
# EXPECTED_ANSWERS = (127, 62, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        data = ingest(INPUT_FILE)
        self.numbers = [int(n) for n in data]

    def solve1(self):
        answer = None

        numbers = self.numbers
        offset = 0

        for i in range(PREAMBLE_LENGTH, len(self.numbers)):
            c = self.numbers[i]

            window = self.numbers[offset:offset + PREAMBLE_LENGTH]
            preamble = {
                n: True
                for n
                in window
            }

            x, y = None, None

            for a in window:
                b = c - a
                if b in preamble:
                    x, y = a, b
                    break

            if x is None or y is None:
                answer = c
                break

            offset += 1

        self.answer1 = answer

        return answer

    def solve2(self):
        answer = None
        numbers = self.numbers
        target = self.answer1

        target_set = None

        i = 0
        while target_set is None and i < len(numbers):
            for j in range(i + 1, len(numbers)):
                window = numbers[i:j]
                window_sum = sum(window)

                if window_sum == target:
                    target_set = window
                    break
                elif window_sum < target:
                    # continue to expand the window
                    pass
                elif window_sum > target:
                    # exceeded the target, shif window
                    break

            i += 1

        answer = max(target_set) + min(target_set)

        return answer


if __name__ == '__main__':
    main()
