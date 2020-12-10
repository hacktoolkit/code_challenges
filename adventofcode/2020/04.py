# Python Standard Library Imports
import re

from utils import ingest


INPUT_FILE = '04.in'
EXPECTED_ANSWERS = (250, 158, )

# INPUT_FILE = '04.test.in'
# INPUT_FILE = '04b.test.in'
# EXPECTED_ANSWERS = (2, 4, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE, as_groups=True)
        self.passports = [Passport(lines) for lines in self.data]

    def solve1(self):
        answer = len(filter(lambda passport: passport.is_valid1, self.passports))
        return answer

    def solve2(self):
        answer = len(filter(lambda passport: passport.is_valid2, self.passports))
        return answer


def is_valid_height(hgt):
    is_valid = False

    m = re.match(r'^(?P<value>\d+)(?P<unit>(cm)|(in))$', hgt)
    if m:
        height = int(m.group('value'))
        unit = m.group('unit')
        if unit == 'cm':
            is_valid = 150 <= height <= 193
        elif unit == 'in':
            is_valid = 59 <= height <= 76
        else:
            raise Exception('invalid unit')

    return is_valid


class Passport:
    REQUIRED_FIELDS = {
        'byr': lambda x: 1920 <= int(x) <= 2002,
        'iyr': lambda x: 2010 <= int(x) <= 2020,
        'eyr': lambda x: 2020 <= int(x) <= 2030,
        'hgt': is_valid_height,
        'hcl': lambda x: bool(re.match(r'^#[0-9a-f]{6}$', x)),
        'ecl': lambda x: x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'],
        'pid': lambda x: bool(re.match(r'^[0-9]{9}$', x)),
        # 'cid',  # optional
    }

    def __init__(self, lines):
        self.data = {}

        for line in lines:
            fields = line.split()
            for field in fields:
                key, value = field.split(':')
                self.data[key] = value

    @property
    def keys(self):
        return list(self.data.keys())

    @property
    def is_valid1(self):
        missing_keys = set(self.REQUIRED_FIELDS) - set(list(self.keys))
        is_valid = len(missing_keys) == 0
        return is_valid

    @property
    def is_valid2(self):
        missing_keys = set((self.REQUIRED_FIELDS.keys())) - set(list(self.keys))

        if len(missing_keys) == 0:
            is_valid = True

            for key, rule in self.REQUIRED_FIELDS.items():
                value = self.data[key]
                if not rule(value):
                    # print(key, value)
                    is_valid = False
                    break
        else:
            is_valid = False

        return is_valid


if __name__ == '__main__':
    main()
