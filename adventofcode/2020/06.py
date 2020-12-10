from utils import ingest


INPUT_FILE = '06.in'
EXPECTED_ANSWERS = (6437, 3229, )

# INPUT_FILE = '06.test.in'
# EXPECTED_ANSWERS = (11, 6, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE, as_groups=True)
        self.groups = [Group(lines) for lines in self.data]

    def solve1(self):
        scores = [group.num_yes_answers for group in self.groups]
        answer = sum(scores)
        return answer

    def solve2(self):
        scores = [group.num_shared_yes_answers for group in self.groups]
        answer = sum(scores)
        return answer


class Group:
    def __init__(self, lines):
        self.lines = lines

    @property
    def yes_answers(self):
        yes_answers = []
        for line in self.lines:
            for c in line:
                yes_answers.append(c)

        yes_answers = list(set(yes_answers))
        return yes_answers

    @property
    def num_yes_answers(self):
        return len(self.yes_answers)

    @property
    def shared_yes_answers(self):
        shared_yes_answers = None
        for line in self.lines:
            answers = set([c for c in line])
            if shared_yes_answers is None:
                shared_yes_answers = answers
            else:
                shared_yes_answers = shared_yes_answers.intersection(answers)

        return list(shared_yes_answers)

    @property
    def num_shared_yes_answers(self):
        return len(self.shared_yes_answers)


if __name__ == '__main__':
    main()
