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
