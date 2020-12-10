# Python Standard Library Imports
import re

from utils import ingest


INPUT_FILE = '02.in'
EXPECTED_ANSWERS = (398, 562, )

# INPUT_FILE = '02.test.in'
# EXPECTED_ANSWERS = (1, 1, )


def main():
    answers = (solve1(), solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


def solve1():
    data = ingest(INPUT_FILE)
    entries = data

    pattern = r'(?P<lower>\d+)-(?P<upper>\d+) (?P<letter>[a-z]): (?P<password>[a-z]+)'
    regex = re.compile(pattern)

    num_valid_passwords = 0

    for entry in entries:
        m = regex.match(entry)
        if m is None:
            raise Exception('Entry does not match pattern: %s' % entry)
        else:
            lower, upper, letter, password = [
                int(m.group('lower')),
                int(m.group('upper')),
                m.group('letter'),
                m.group('password'),
            ]

            occurrences = len(list(filter(lambda c: c == letter, password)))
            if lower <= occurrences <= upper:
                num_valid_passwords += 1

    answer = num_valid_passwords
    return answer


def solve2():
    data = ingest(INPUT_FILE)
    entries = data

    pattern = r'(?P<lower>\d+)-(?P<upper>\d+) (?P<letter>[a-z]): (?P<password>[a-z]+)'
    regex = re.compile(pattern)

    num_valid_passwords = 0

    for entry in entries:
        m = regex.match(entry)
        if m is None:
            raise Exception('Entry does not match pattern: %s' % entry)
        else:
            i, j, letter, password = [
                int(m.group('lower')) - 1,
                int(m.group('upper')) - 1,
                m.group('letter'),
                m.group('password'),
            ]

            chars = [password[i], password[j]]
            occurrences = len(list(filter(lambda c: c == letter, chars)))
            if occurrences == 1:
                num_valid_passwords += 1

    answer = num_valid_passwords
    return answer


if __name__ == '__main__':
    main()
