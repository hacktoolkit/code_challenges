# Python Standard Library Imports
import re
from collections import defaultdict

from utils import (
    Re,
    ingest,
)


INPUT_FILE = '04.in'
EXPECTED_ANSWERS = (361724, 482, )

# INPUT_FILE = '04.test.in'
# EXPECTED_ANSWERS = (1514, None, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)
        self.rooms = [Room(room) for room in self.data]

    def solve1(self):
        sector_ids = [room.sector_id for room in self.rooms if room.is_valid]
        answer = sum(sector_ids)
        return answer

    def solve2(self):
        answer = None
        for room in self.rooms:
            if room.is_valid:
                if room.real_name == 'northpole object storage':
                    answer = room.sector_id

        return answer


class Room:
    ROOM_REGEX = re.compile(r'^(?P<encrypted_name>[a-z-]*[a-z])-(?P<sector_id>\d+)\[(?P<checksum>[a-z]{5})\]$')

    def __init__(self, room):
        self.room = room

        regex = Re()
        if regex.match(self.ROOM_REGEX, room):
            m = regex.last_match
            self.encrypted_name, self.sector_id, self.checksum = (
                m.group('encrypted_name'),
                int(m.group('sector_id')),
                m.group('checksum')
            )

    @property
    def expected_checksum(self):
        counts = defaultdict(int)
        for c in self.encrypted_name.replace('-', ''):
            counts[c] += 1

        pairs = list(counts.items())
        sorted_pairs = sorted(pairs, key=lambda (letter, count): 1000 * count + (ord('z') - ord(letter)), reverse=True)
        checksum = ''.join([pair[0] for pair in sorted_pairs[:5]])
        return checksum

    @property
    def is_valid(self):
        return self.checksum == self.expected_checksum

    @property
    def real_name(self):
        deciphered = []
        for c in self.encrypted_name:
            if c == '-':
                deciphered.append(' ')
            else:
                code = ord(c) - ord('a')
                shifted_code = ord('a') + (code + self.sector_id) % 26
                deciphered.append(chr(shifted_code))

        real_name = ''.join(deciphered)
        return real_name


if __name__ == '__main__':
    main()
