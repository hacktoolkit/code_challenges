# Python Standard Library Imports
from functools import lru_cache

from utils import ingest


INPUT_FILE = '10.in'
EXPECTED_ANSWERS = (1890, 49607173328384, )

# INPUT_FILE = '10.test.in'
# EXPECTED_ANSWERS = (35, 8, )

# INPUT_FILE = '10b.test.in'
# EXPECTED_ANSWERS = (220, 19208, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)
        self.numbers = sorted([int(n) for n in self.data])

    def solve1(self):
        diff1 = 1
        diff3 = 1

        prev = None
        for n in self.numbers:
            if prev is not None:
                diff = n - prev
                if diff == 1:
                    diff1 += 1
                elif diff == 3:
                    diff3 += 1
            prev = n

        answer = diff1 * diff3
        return answer

    def solve2(self):
        lookup = {
            n: True
            for n
            in self.numbers
        }

        @lru_cache
        def _calculate_ways(n):
            ways = 0

            if n == 0:
                ways = 1
            elif n not in lookup:
                ways = 0
            elif n < 0:
                ways = 0
            else:
                ways = (
                    _calculate_ways(n - 3)
                    + _calculate_ways(n - 2)
                    + _calculate_ways(n - 1)
                )

            return ways

        answer = _calculate_ways(self.numbers[-1])
        return answer


if __name__ == '__main__':
    main()
