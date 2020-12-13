# Python Standard Library Imports
from itertools import combinations

from utils import ingest


TARGET = 150
INPUT_FILE = '17.in'
EXPECTED_ANSWERS = (654, 57, )

# TARGET = 25
# INPUT_FILE = '17.test.in'
# EXPECTED_ANSWERS = (4, 3, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        data = ingest(INPUT_FILE)
        containers = sorted([int(c) for c in data], reverse=True)
        self.kitchen = Kitchen(containers)
        self.kitchen.store(TARGET)

    def solve1(self):
        answer = self.kitchen.ways

        self.answer1 = answer
        return answer

    def solve2(self):
        answer = len(self.kitchen.optimal_combos)

        self.answer2 = answer
        return answer


class Kitchen:
    def __init__(self, containers):
        self.containers = containers


    def store(self, amount):
        ways = 0

        optimal_combos = None
        min_containers = None

        for i in range(1, len(self.containers) + 1):
            for combo in combinations(self.containers, i):
                capacity = sum(combo)

                if capacity == amount:
                    ways += 1

                    if optimal_combos is None or len(combo) < min_containers:
                        optimal_combos = [combo]
                        min_containers = len(combo)
                    elif len(combo) == min_containers:
                        optimal_combos.append(combo)
                    else:
                        pass

        self.ways = ways
        self.optimal_combos = optimal_combos

if __name__ == '__main__':
    main()
