# Python Standard Library Imports
import typing as T
from collections import deque
from dataclasses import dataclass

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (1591, 14579387544492)
config.TEST_CASES = {
    '': (3, 1623178306),
}

config.INPUT_CONFIG.as_integers = True


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data

    def solve1(self):
        encrypted_file = EncryptedFile(self.data)
        debug(encrypted_file.numbers)
        encrypted_file.mix()
        debug(encrypted_file.numbers)
        answer = sum(encrypted_file.grove_coordinates())
        return answer

    def solve2(self):
        encrypted_file = EncryptedFile(self.data, decrypt=True)
        debug(encrypted_file.numbers)
        for i in range(10):
            encrypted_file.mix()
            debug(encrypted_file.numbers)
        answer = sum(encrypted_file.grove_coordinates())
        return answer


class EncryptedFile:
    DECRYPTION_KEY = 811589153

    @dataclass
    class Node:
        value: int

    def __init__(self, numbers, decrypt=False):
        multiplier = self.DECRYPTION_KEY if decrypt else 1
        self.orig_positions = [
            (n * multiplier, i) for i, n in enumerate(numbers)
        ]
        self.q = deque(self.orig_positions)

    @property
    def numbers(self):
        numbers = [n[0] for n in self.q]
        return numbers

    def mix(self):
        for item in self.orig_positions:
            number, i = item
            if number != 0:
                index = self.q.index(item)
                self.q.remove(item)
                new_index = (index + number) % len(self.q)
                if new_index == 0:
                    new_index = len(self.q)
                self.q.insert(new_index, item)
            debug(self.numbers)

    def grove_coordinates(self):
        index = 0
        while self.q[index][0] != 0:
            index += 1
        debug(index)
        offsets = (1000, 2000, 3000)
        indices = [(index + offset) % len(self.q) for offset in offsets]
        print(indices)
        coordinates = [self.q[i][0] for i in indices]
        print(coordinates)
        return coordinates


if __name__ == '__main__':
    main()
