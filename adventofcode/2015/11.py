from utils import ingest


INPUT = 'hxbxwxba'
EXPECTED_ANSWERS = ('hxbxxyzz', 'hxcaabcc', )

# INPUT = 'abcdefgh'
# EXPECTED_ANSWERS = ('abcdffaa', 'abcdffbb', )

# INPUT = 'ghijklmn'
# EXPECTED_ANSWERS = ('ghjaabcc', 'ghjbbcdd', )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = INPUT
        self.password = Password(INPUT)

    def solve1(self):
        self.password2 = self.password.find_next_valid_password()
        answer = self.password2.password
        return answer

    def solve2(self):
        self.password3 = self.password2.find_next_valid_password()
        answer = self.password3.password
        return answer


class Password:
    EXPECTED_LENGTH = 8
    ILLEGAL_CHARS = set(['i', 'o', 'l', ])

    def __init__(self, password):
        self.password = password
        self.chars = [c for c in password]
        self.char_codes = [ord(c) - ord('a') for c in self.chars]

    @property
    def has_illegal_chars(self):
        illegals = set(self.chars).intersection(self.ILLEGAL_CHARS)
        return len(illegals) > 0

    @property
    def has_two_distinct_non_overlapping_pairs(self):
        pairs = []

        for i in range(len(self.chars) - 2 + 1):
            a, b = self.chars[i:i + 2]
            if a == b:
                pairs.append(a*2)

        return len(set(pairs)) >= 2

    @property
    def has_increasing_straight_3(self):
        for i in range(len(self.chars) - 3 + 1):
            a, b, c = self.char_codes[i:i + 3]
            if a + 1 == b and b + 1 == c:
                return True

        return False

    @property
    def is_valid(self):
        valid = (
            len(self.password) == self.EXPECTED_LENGTH
            and not self.has_illegal_chars
            and self.has_two_distinct_non_overlapping_pairs
            and self.has_increasing_straight_3
        )
        return valid

    def next_password(self):
        next_char_codes = self.char_codes

        carry = 0

        for i in range(len(next_char_codes)):
            j = -1 - i
            code = next_char_codes[j]
            next_code = code + (1 if i == 0 else carry)
            carry = 1 if next_code >= 26 else 0
            next_code_candidate = next_code % 26
            if chr(next_code_candidate + ord('a')) in self.ILLEGAL_CHARS:
                next_code_candidate += 1

            next_char_codes[j] = next_code_candidate
            if carry == 0:
                break

        next_password = ''.join([chr(n + ord('a')) for n in next_char_codes])
        return Password(next_password)

    def find_next_valid_password(self):
        p = self.next_password()
        while not p.is_valid:
            p = p.next_password()

        return p


if __name__ == '__main__':
    main()
