from utils import ingest


INPUT = 1113222113
EXPECTED_ANSWERS = (252594, 3579328, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = INPUT

    def solve1(self):
        n = INPUT

        encoded = n
        for x in range(40):
            encoded = run_length_encode(encoded)

        answer = len(encoded)
        return answer

    def solve2(self):
        n = INPUT

        encoded = n
        for x in range(50):
            encoded = run_length_encode(encoded)

        answer = len(encoded)
        return answer


def run_length_encode(n):
    """Generates the run-length encoded version of `n`

    https://en.wikipedia.org/wiki/Run-length_encoding
    """
    prev = None
    count = 0

    output = []

    for d in str(n):
        if prev is None:
            count = 1
            prev = d
        elif d == prev:
            count += 1
        else:
            output.extend([str(count), prev])
            prev = d
            count = 1

    if count > 0 and prev is not None:
        output.extend([str(count), prev])

    encoded = ''.join(output)
    return encoded


if __name__ == '__main__':
    main()
