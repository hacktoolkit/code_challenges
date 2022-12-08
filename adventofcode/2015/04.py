# Python Standard Library Imports
import hashlib

from utils import (
    BaseSolution,
    config,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (254575, 1038736)
config.TEST_CASES = {'': (609043, 6742839)}

config.INPUT_CONFIG.as_oneline = True


@solution
class Solution(BaseSolution):
    def process_data(self):
        self.key = self.data

    def solve1(self):
        n = 1
        while True:
            prehash = '{}{}'.format(self.key, n)
            h = hashlib.md5(prehash.encode()).hexdigest()
            if h[:5] == '00000':
                answer = n
                break

            n += 1

        return answer

    def solve2(self):
        n = 1
        while True:
            prehash = '{}{}'.format(self.key, n)
            h = hashlib.md5(prehash.encode()).hexdigest()
            if h[:6] == '000000':
                answer = n
                break

            n += 1

        return answer


if __name__ == '__main__':
    main()
