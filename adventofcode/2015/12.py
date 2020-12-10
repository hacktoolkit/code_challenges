from utils import ingest


INPUT_FILE = '12.in'
EXPECTED_ANSWERS = (191164, 87842, )

# INPUT_FILE = '12.test.in'
# EXPECTED_ANSWERS = (6, 4, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE, as_json=True)

    def solve1(self):
        answer = add_numbers_json(self.data)
        return answer

    def solve2(self):
        def _should_ignore(o):
            if type(o) == dict:
                if 'red' in list(o.values()):
                    return True
            return False

        answer = add_numbers_json(self.data, ignore_fn=_should_ignore)
        return answer


def add_numbers_json(o, ignore_fn=None):
    total = 0
    if ignore_fn is not None and ignore_fn(o):
        pass
    elif type(o) == dict:
        for key, value in o.items():
            total += add_numbers_json(value, ignore_fn=ignore_fn)
    elif type(o) == list:
        for child in o:
            total += add_numbers_json(child, ignore_fn=ignore_fn)
    elif type(o) == int:
        total += o
    return total


if __name__ == '__main__':
    main()
