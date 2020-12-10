# Python Standard Library Imports
from collections import defaultdict

from utils import ingest


INPUT_FILE = '02.in'
EXPECTED_ANSWERS = (7657, 'ivjhcadokeltwgsfsmqwrbnuy', )

# INPUT_FILE = '02.test.in'
# EXPECTED_ANSWERS = (12, 'abcde', )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)
        self.boxes = [Box(box) for box in self.data]

    def solve1(self):
        num_has2 = sum([1 for box in self.boxes if box.has2])
        num_has3 = sum([1 for box in self.boxes if box.has3])

        answer = num_has2 * num_has3
        return answer

    def solve2(self):
        answer = None

        for i in range(len(self.boxes)):
            for j in range(i + 1, len(self.boxes)):
                box1, box2 = self.boxes[i], self.boxes[j]
                if box1.diff_is1(box2):
                    answer = box1.common_chars(box2)
                    break
            if answer:
                break

        return answer


class Box:
    def __init__(self, box_id):
        self.box_id = box_id

        letter_counts = defaultdict(int)
        for c in box_id:
            letter_counts[c] += 1

        self.letter_counts = dict(letter_counts)

        values = set(self.letter_counts.values())

        self.has2 = 2 in values
        self.has3 = 3 in values

    def diff_is1(self, other_box):
        box_id1, box_id2 = self.box_id, other_box.box_id

        num_diffs = 0
        for i in range(len(box_id1)):
            if box_id1[i] != box_id2[i]:
                num_diffs += 1

            if num_diffs > 1:
                break

        return num_diffs == 1

    def common_chars(self, other_box):
        box_id1, box_id2 = self.box_id, other_box.box_id
        chars = ''.join([c for i, c in enumerate(box_id1) if c == box_id2[i]])
        return chars


if __name__ == '__main__':
    main()
