from utils import ingest


INPUT = [8, 0, 17, 4, 1, 12, ]
EXPECTED_ANSWERS = (981, 164878, )

# INPUT = [0, 3, 6, ]
# EXPECTED_ANSWERS = (436, 175594, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        pass

    def solve1(self):
        numbers = INPUT

        game = NumberMemoryGame(numbers)

        answer = game.number_at(2020)

        self.answer1 = answer
        return answer

    def solve2(self):
        numbers = INPUT

        game = NumberMemoryGame(numbers)

        answer = game.number_at(30000000)

        self.answer2 = answer
        return answer


class NumberMemoryGame:
    def __init__(self, seed_numbers):
        self.num_sequence = seed_numbers

        self.num_lru = {
            num: [i + 1]
            for i, num
            in enumerate(seed_numbers)
        }

    def number_at(self, n):
        while len(self.num_sequence) < n:
            self.generate_next()

        number = self.num_sequence[n - 1]
        return number

    def generate_next(self):
        last_num = self.num_sequence[-1]

        lru = self.num_lru.get(last_num, [])
        if len(lru) < 2:
            number = 0
        else:
            number = lru[-1] - lru[-2]

        self.num_sequence.append(number)
        if number in self.num_lru:
            self.num_lru[number] = [self.num_lru[number][-1], len(self.num_sequence)]
        else:
            self.num_lru[number] = [len(self.num_sequence)]

        return number


if __name__ == '__main__':
    main()
