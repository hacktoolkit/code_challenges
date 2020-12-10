from utils import (
    base_anagram,
    ingest,
)


INPUT_FILE = '04.in'
EXPECTED_ANSWERS = (337, 231, )

# INPUT_FILE = '04.test.in'
# EXPECTED_ANSWERS = (7, 5, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)
        self.passphrases = [Passphrase(passphrase) for passphrase in self.data]

    def solve1(self):
        valid_passphrases = list(filter(lambda x: x.is_valid, self.passphrases))
        answer = len(valid_passphrases)
        return answer

    def solve2(self):
        valid_passphrases = list(filter(lambda x: x.is_valid2, self.passphrases))
        answer = len(valid_passphrases)
        return answer


class Passphrase:
    def __init__(self, passphrase):
        self.passphrase = passphrase
        self.words = passphrase.split(' ')

    @property
    def is_valid(self):
        is_valid = len(self.words) == len(set(self.words))
        return is_valid

    @property
    def is_valid2(self):
        anagrams = [base_anagram(word) for word in self.words]
        is_valid = len(self.words) == len(set(anagrams))
        return is_valid


if __name__ == '__main__':
    main()
