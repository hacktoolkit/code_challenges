def main():
    answer = solve()
    print(answer)


def solve():
    with open('1.in', 'r') as f:
        numbers = [int(n.strip()) for n in f.readlines()]

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
