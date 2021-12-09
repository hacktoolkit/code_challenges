# Python Standard Library Imports
import re

from utils import (
    Re,
    ingest,
)


INPUT_FILE = '16.in'
EXPECTED_ANSWERS = (103, 405, )

MFCSAM = {
    'children': 3,
    'cats': 7,
    'samoyeds': 2,
    'pomeranians': 3,
    'akitas': 0,
    'vizslas': 0,
    'goldfish': 5,
    'trees': 3,
    'cars': 2,
    'perfumes': 1,
}


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        data = ingest(INPUT_FILE)
        self.aunts = [AuntSue(s) for s in data]

    def solve1(self):
        answer = None

        for aunt in self.aunts:
            if aunt.matches_mfcsam(MFCSAM):
                answer = aunt.id
                break

        self.answer1 = answer
        return answer

    def solve2(self):
        answer = None

        for aunt in self.aunts:
            if aunt.matches_mfcsam2(MFCSAM):
                answer = aunt.id
                break

        self.answer2 = answer
        return answer


class AuntSue:
    REGEX = re.compile(r'^Sue (?P<id>\d+): (?P<compounds>.*)$')

    def __init__(self, sue_data):
        regex = Re()
        if regex.match(AuntSue.REGEX, sue_data):
            m = regex.last_match

            self.id, compounds = (
                int(m.group('id')),
                m.group('compounds')
            )

            self.stuff = {}

            things = compounds.split(', ')
            for thing in things:
                item, count = thing.split(':')
                self.stuff[item] = int(count)

            print(self.stuff)
        else:
            raise Exception('Bad data format: %s' % sue_data)

    def matches_mfcsam(self, mfcsam):
        is_match = True

        for thing, count in self.stuff.items():
            expected_count = mfcsam.get(thing)
            if count != expected_count:
                is_match = False
                break

        return is_match

    def matches_mfcsam2(self, mfcsam):
        is_match = True

        for thing, count in self.stuff.items():
            expected_count = mfcsam.get(thing)
            if thing in ('cats', 'trees', ):
                is_match = count > expected_count
            elif thing in ('pomeranians', 'goldfish', ):
                is_match = count < expected_count
            else:
                if count != expected_count:
                    is_match = False

            if not is_match:
                break

        return is_match


if __name__ == '__main__':
    main()
