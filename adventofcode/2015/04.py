import hashlib

from utils import ingest


INPUT_FILE = '4.in'
EXPECTED_ANSWERS = (254575, 1038736, )

# INPUT_FILE = '4.test.in'
# EXPECTED_ANSWERS = (609043, 6742839, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        data = ingest(INPUT_FILE, as_oneline=True)
        self.key = data

    def solve1(self):
        n = 1
        while True:
            prehash = '{}{}'.format(self.key, n)
            h = hashlib.md5(prehash).hexdigest()
            if h[:5] == '00000':
                answer = n
                break

            n += 1

        return answer

    def solve2(self):
        n = 1
        while True:
            prehash = '{}{}'.format(self.key, n)
            h = hashlib.md5(prehash).hexdigest()
            if h[:6] == '000000':
                answer = n
                break

            n += 1

        return answer


if __name__ == '__main__':
    main()
