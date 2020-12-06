from utils import ingest


INPUT_FILE = 'n.in'
# EXPECTED_ANSWERS = (None, None, )

# INPUT_FILE = 'n.test.in'
# EXPECTED_ANSWERS = (None, None, )


def main():
    answers = (solve1(), solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


def solve1():
    data = ingest(INPUT_FILE)
    answer = None
    return answer


def solve2():
    data = ingest(INPUT_FILE)
    answer = None
    return answer


if __name__ == '__main__':
    main()
