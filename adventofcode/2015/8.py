from utils import ingest


INPUT_FILE = '8.in'
EXPECTED_ANSWERS = (1350, 2085, )

# INPUT_FILE = '8.test.in'
# EXPECTED_ANSWERS = (12, 19, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)
        self.strings = [S(s) for s in self.data]

    def solve1(self):
        code_size = sum([s.code_length for s in self.strings])
        memory_size = sum([s.memory_length for s in self.strings])

        answer = code_size - memory_size
        return answer

    def solve2(self):
        encoded_size = sum([s.encoded_length for s in self.strings])
        code_size = sum([s.code_length for s in self.strings])

        answer = encoded_size - code_size
        return answer


CHAR_MAP = {
    '"': '\\"',
    '\\': '\\\\',
}


class S:
    def __init__(self, s):
        self.raw = s
        self.s = eval(s)
        self.encoded = ''.join([CHAR_MAP.get(c, c) for c in s])

    @property
    def code_length(self):
        return len(self.raw)

    @property
    def memory_length(self):
        return len(self.s)

    @property
    def encoded_length(self):
        return len(self.encoded) + 2


if __name__ == '__main__':
    main()
