from utils import ingest


INPUT = (128392, 643281)
EXPECTED_ANSWERS = (2050, 1390, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        lower, upper = INPUT
        self.passwords = [Password(n) for n in range(lower, upper + 1)]

    def solve1(self):
        valid_passwords = list(filter(lambda x: x.is_valid, self.passwords))
        answer = len(valid_passwords)
        return answer

    def solve2(self):
        valid_passwords = list(filter(lambda x: x.is_valid2, self.passwords))
        answer = len(valid_passwords)
        return answer


class Password:
    def __init__(self, n):
        self.n = n
        self.digits = str(n)

    def _has_valid_length(self):
        return len(self.digits) == 6

    def _has_two_adjacent_digits_same(self):
        prev = None
        for d in self.digits:
            if d == prev:
                return True
            prev = d
        return False

    def _has_monotonically_increasing_digits(self):
        prev = None
        for d in self.digits:
            n = int(d)
            if prev is not None and n < prev:
                return False
            prev = n
        return True

    def _has_strict_double_streak(self):
        prev = None
        streak = 0
        for d in self.digits:
            if prev == None:
                prev = d
                streak = 1
            elif d == prev:
                streak += 1
            else:
                if streak == 2:
                    return True
                prev = d
                streak = 1

        if streak == 2:
            return True
        return False

    @property
    def is_valid(self):
        valid = (
            self._has_valid_length()
            and self._has_two_adjacent_digits_same()
            and self._has_monotonically_increasing_digits()
        )
        return valid

    @property
    def is_valid2(self):
        valid = (
            self._has_valid_length()
            and self._has_strict_double_streak()
            and self._has_monotonically_increasing_digits()
        )
        return valid


if __name__ == '__main__':
    main()
