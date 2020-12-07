from utils import ingest


INPUT_FILE = '2.in'
EXPECTED_ANSWERS = (4945026, None, )

# INPUT_FILE = '2.test.in'
# EXPECTED_ANSWERS = (3500, None, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)
        self.numbers = [int(x) for x in ','.join(self.data).split(',')]

    def solve1(self):
        self.numbers[1] = 12
        self.numbers[2] = 2
        self.run()
        answer = self.numbers[0]
        return answer

    def solve2(self):
        answer = None
        return answer

    def run(self):
        index = 0
        while index < len(self.numbers):
            opcode, in1, in2, dest = (
                self.numbers[index],
                self.numbers[index + 1],
                self.numbers[index + 2],
                self.numbers[index + 3]
            )

            if opcode in (1, 2):
                val1, val2 = self.numbers[in1], self.numbers[in2]
                if opcode == 1:
                    self.numbers[dest] = val1 + val2
                else:
                    self.numbers[dest] = val1 * val2

            elif opcode == 99:
                break
            else:
                raise Exception('Unknown opcode: %s' % opcode)

            index += 4


if __name__ == '__main__':
    main()
