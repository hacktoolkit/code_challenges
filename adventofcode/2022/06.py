from utils import (
    BaseSolution,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (1198, 3120)
config.TEST_CASES = {
    '': (7, 19),
    'b': (5, 23),
    'c': (6, 23),
    'd': (10, 29),
    'e': (11, 26),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        self.s = data[0]

    def solve1(self):
        s = self.s
        answer = find_first_marker(s)
        return answer

    def solve2(self):
        s = self.s
        answer = find_first_packet(s)
        return answer


def find_first_marker(s, L=4):
    debug(s)

    i = 0
    j = None
    found_marker = False

    while not found_marker:
        j = i + L
        candidate = s[i:j]
        if len(set(candidate)) < L:
            i += 1
        elif len(set(candidate)) == L:
            debug(candidate, j)
            found_marker = True

    return j


def find_first_packet(s, L=14):
    return find_first_marker(s, L=L)


if __name__ == '__main__':
    main()
