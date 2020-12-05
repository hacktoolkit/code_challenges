INPUT_FILE = '4.in'
# INPUT_FILE = '4.test.in'


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


class Passport:
    REQUIRED_FIELDS = [
        'byr',
        'iyr',
        'eyr',
        'hgt',
        'hcl',
        'ecl',
        'pid',
        # 'cid',  # optional
    ]

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
        missing_keys = set(self.REQUIRED_FIELDS) - set(list(self.keys))
        is_valid = len(missing_keys) == 0
        return is_valid


def ingest():
    with open(INPUT_FILE, 'r') as f:
        data = [line.strip() for line in f.readlines()]
    return data


if __name__ == '__main__':
    main()
