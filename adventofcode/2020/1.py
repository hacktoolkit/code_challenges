def main():
    answer = solve()
    print(answer)


def solve():
    with open('1.in', 'r') as f:
        numbers = [int(n.strip()) for n in f.readlines()]

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


if __name__ == '__main__':
    main()
