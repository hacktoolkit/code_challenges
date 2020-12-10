# Python Standard Library Imports
import hashlib

from utils import ingest


INPUT = 'ffykfhsq'
EXPECTED_ANSWERS = ('c6697b55', '8c35d1ab', )

# INPUT = 'abc'
# EXPECTED_ANSWERS = ('18f47a30', '05ace8e3', )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = INPUT

    def solve1(self):
        password_cracker = PasswordCracker(self.data)
        answer = password_cracker.crack()
        return answer

    def solve2(self):
        password_cracker = PasswordCracker(self.data)
        answer = password_cracker.crack2()
        return answer


class PasswordCracker:
    def __init__(self, door_id):
        self.door_id = door_id

    def crack(self):
        password_chars = []

        i = 0

        while len(password_chars) < 8:
            prehash = '{}{}'.format(self.door_id, i)
            hashed = hashlib.md5(prehash).hexdigest()

            if hashed[:5] == '00000':
                password_chars.append(hashed[5])

            i += 1

        password = ''.join(password_chars)
        return password

    def crack2(self):
        password_chars = ['_'] * 8

        i = 0

        while '_' in password_chars:
            prehash = '{}{}'.format(self.door_id, i)
            hashed = hashlib.md5(prehash).hexdigest()

            if hashed[:5] == '00000':
                try:
                    position = int(hashed[5])
                    if 0 <= position < 8 and password_chars[position] == '_':
                        c = hashed[6]
                        password_chars[position] = c
                        print(''.join(password_chars))
                except ValueError:
                    pass

            i += 1

        password = ''.join(password_chars)
        return password


if __name__ == '__main__':
    main()
