# Python Standard Library Imports
import re


INPUT_FILE = '4.in'
# INPUT_FILE = '4b.test.in'


def main():
    answer = solve()
    print(answer)


def solve():
    data = ingest()
    passports = get_passports(data)
    answer = len(filter(lambda passport: passport.is_valid, passports))
    return answer


def get_passports(data):
    passports = []

    passport = None

    for line in data:
        if passport is None:
            passport = Passport()

        if line:
            fields = line.split()
            passport.add_fields(fields)
        else:
            passports.append(passport)
            passport = None

    if passport:
        passports.append(passport)

    return passports


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

    def __init__(self):
        self.data = {}

    def add_fields(self, fields):
        for field in fields:
            key, value = field.split(':')
            self.data[key] = value

    @property
    def keys(self):
        return list(self.data.keys())

    @property
    def is_valid(self):
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


def ingest():
    with open(INPUT_FILE, 'r') as f:
        data = [line.strip() for line in f.readlines()]
    return data


if __name__ == '__main__':
    main()
