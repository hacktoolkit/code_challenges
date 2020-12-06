INPUT_FILE = '6.in'
# INPUT_FILE = '6.test.in'


def main():
    answer1 = solve1()
    answer2 = solve2()
    print(answer1, answer2)


def solve1():
    data = ingest()

    groups = []

    group = None
    for line in data:
        if group is None:
            group = Group()
        if line:
            group.add_line(line)
        else:
            groups.append(group)
            group = None

    if group:
        groups.append(group)

    scores = [group.num_yes_answers for group in groups]
    answer = sum(scores)
    return answer


def solve2():
    data = ingest()

    groups = []

    group = None
    for line in data:
        if group is None:
            group = Group()
        if line:
            group.add_line(line)
        else:
            groups.append(group)
            group = None

    if group:
        groups.append(group)

    scores = [group.num_shared_yes_answers for group in groups]
    answer = sum(scores)
    return answer


class Group:
    def __init__(self):
        self.lines = []

    def add_line(self, line):
        self.lines.append(line)

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


def ingest():
    with open(INPUT_FILE, 'r') as f:
        data = [line.strip() for line in f.readlines()]
    return data


if __name__ == '__main__':
    main()
