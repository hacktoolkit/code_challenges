from utils import (
    BaseSolution,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (8233, 2821)
config.TEST_CASES = {
    '': (157, 70),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data

    def solve1(self) -> int:
        p_total = 0
        for sack in self.data:
            l = len(sack) // 2
            c1 = sack[:l]
            c2 = sack[l:]
            common = next(iter(set(c1) & set(c2)))
            p = priority(common)
            debug(common, p)
            p_total += p

        answer = p_total
        return answer

    def solve2(self) -> int:
        p_total = 0
        i = 0
        while i < len(self.data):
            c1, c2, c3 = self.data[i], self.data[i + 1], self.data[i + 2]
            common = next(iter(set(c1) & set(c2) & set(c3)))
            p = priority(common)
            debug(common, p)

            p_total += p
            i += 3

        answer = p_total
        return answer


def priority(letter: str) -> int:
    if 'a' <= letter <= 'z':
        return ord(letter) - ord('a') + 1
    elif 'A' <= letter <= 'Z':
        return ord(letter) - ord('A') + 27
    else:
        raise Exception(f"C'est impossible! {letter}")


if __name__ == '__main__':
    main()
