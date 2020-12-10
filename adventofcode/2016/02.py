from utils import ingest


INPUT_FILE = '02.in'
EXPECTED_ANSWERS = ('98575', 'CD8D4', )

# INPUT_FILE = '02.test.in'
# EXPECTED_ANSWERS = ('1985', '5DB3', )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


STANDARD_KEYPAD = [
    [1, 2, 3, ],
    [4, 5, 6, ],
    [7, 8, 9, ],
]
STANDARD_KEYPAD_START = (1, 1, )


CUSTOM_KEYPAD = [
    [None, None, 1, None, None, ],
    [None, 2, 3, 4, None, ],
    [5, 6, 7, 8, 9, ],
    [None, 'A', 'B', 'C', None, ],
    [None, None, 'D', None, None, ],
]
CUSTOM_KEYPAD_START = (0, 2, )


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)

    def solve1(self):
        digits = []

        keypad = Keypad(STANDARD_KEYPAD, STANDARD_KEYPAD_START)
        for instructions in self.data:
            num = keypad.move(instructions)
            digits.append(str(num))

        answer = ''.join(digits)
        return answer

    def solve2(self):
        digits = []

        keypad = Keypad(CUSTOM_KEYPAD, CUSTOM_KEYPAD_START)
        for instructions in self.data:
            num = keypad.move(instructions)
            digits.append(str(num))

        answer = ''.join(digits)
        return answer


class Keypad:
    def __init__(self, keypad, starting_coords):
        self.keypad = keypad
        self.x, self.y = starting_coords

    def move(self, instructions):
        for step in instructions:
            if step == 'U':
                if self.code_at(self.x, self.y - 1) is not None:
                    self.y -= 1
            elif step == 'D':
                if self.code_at(self.x, self.y + 1) is not None:
                    self.y += 1
            elif step == 'L':
                if self.code_at(self.x - 1, self.y) is not None:
                    self.x -= 1
            elif step == 'R':
                if self.code_at(self.x + 1, self.y) is not None:
                    self.x += 1

        return self.code

    def code_at(self, x, y):
        if (
            x < 0  or x > len(self.keypad[0]) - 1
            or y < 0 or y > len(self.keypad) - 1
        ):
            code = None
        else:
            code = self.keypad[y][x]
        return code

    @property
    def code(self):
        return self.code_at(self.x, self.y)


if __name__ == '__main__':
    main()
