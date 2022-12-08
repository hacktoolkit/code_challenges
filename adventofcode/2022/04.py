# Python Standard Library Imports
import re

from utils import (
    BaseSolution,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (483, 874)
config.TEST_CASES = {
    '': (2, 4),
}


@solution
class Solution(BaseSolution):
    REGEX = re.compile(r'^(?P<a>\d+)-(?P<b>\d+),(?P<c>\d+)-(?P<d>\d+)$')

    def process_data(self):
        data = self.data

    def solve1(self) -> int:
        total = 0
        for line in self.data:
            m = self.REGEX.match(line)
            a, b, c, d = map(int, [m.group(_) for _ in 'abcd'])
            debug(a, b, c, d)

            s1 = set(range(a, b + 1))
            s2 = set(range(c, d + 1))

            if len(s1 | s2) == max(len(s1), len(s2)):
                total += 1

        answer = total
        return answer

    def solve2(self) -> int:
        total = 0
        for line in self.data:
            m = self.REGEX.match(line)
            a, b, c, d = map(int, [m.group(_) for _ in 'abcd'])
            debug(a, b, c, d)

            s1 = set(range(a, b + 1))
            s2 = set(range(c, d + 1))

            if len(s1 | s2) < len(s1) + len(s2):
                total += 1

        answer = total
        return answer


if __name__ == '__main__':
    main()
