from utils import ingest


INPUT_FILE = '1.in'
EXPECTED_ANSWERS = (1019904, 176647680, )


def main():
    answers = (solve1(), solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


def solve1():
    data = ingest(INPUT_FILE)
    numbers = [int(n) for n in data]

    TARGET_SUM = 2020

    a, b = None, None

    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i == j:
                # same index, skip
                pass
            else:
                x, y = numbers[i], numbers[j]
                if x + y == TARGET_SUM:
                    a, b = x, y
                    break

    if a is None or b is None:
        raise Exception('No numbers found that sum to: %s' % TARGET_SUM)
    else:
        answer = a * b

    return answer


def solve2():
    data = ingest(INPUT_FILE)
    numbers = [int(n) for n in data]

    TARGET_SUM = 2020

    a, b, c = None, None, None

    for i in range(len(numbers)):
        for j in range(len(numbers)):
            for k in range(len(numbers)):
                if i == j or i == k or j == k:
                    # same index, skip
                    pass
                else:
                    x, y, z = numbers[i], numbers[j], numbers[k]
                    if x + y + z == TARGET_SUM:
                        a, b, c = x, y, z
                        break

    if a is None or b is None or c is None:
        raise Exception('No numbers found that sum to: %s' % TARGET_SUM)
    else:
        answer = a * b * c

    return answer


if __name__ == '__main__':
    main()
