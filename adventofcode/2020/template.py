INPUT_FILE = 'n.in'
# INPUT_FILE = 'n.test.in'

def main():
    answer = solve()
    print(answer)


def solve():
    data = ingest()
    answer = None
    return answer


def ingest():
    with open(INPUT_FILE, 'r') as f:
        data = [line.strip() for line in f.readlines()]
    return data


if __name__ == '__main__':
    main()
