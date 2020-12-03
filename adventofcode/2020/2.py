# Python Standard Library Imports
import re


def main():
    answer = solve()
    print(answer)


def solve():
    with open('2.in', 'r') as f:
        entries = f.readlines()

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


if __name__ == '__main__':
    main()
