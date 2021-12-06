# Python Standard Library Imports
import time

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '06'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (375482, 1689540415957, )
TEST_EXPECTED_ANSWERS = (5934, 26984457539, )


def main():
    input_config = InputConfig(
        as_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=False,
        cell_func=None
    )

    if TEST_MODE:
        input_filename = f'{PROBLEM_NUM}.test.in'
        expected_answers = TEST_EXPECTED_ANSWERS
    else:
        input_filename = f'{PROBLEM_NUM}.in'
        expected_answers = EXPECTED_ANSWERS

    solution = Solution(input_filename, input_config, expected_answers)

    solution.solve()
    solution.report()


class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        raw_ages = data[0]
        self.ages = [int(age) for age in raw_ages.split(',')]

    def solve1(self):
        school = Ocean(self.ages)
        # print(school)

        for i in range(80):
            school.tick()
            # print(school)
            # time.sleep(0.3)

        answer = school.num_fish
        return answer

    def solve2(self):
        school = Ocean(self.ages, use_groups=True)

        for i in range(256):
            school.tick()

        answer = school.num_fish
        return answer


class Ocean:
    def __init__(self, ages, use_groups=False):
        self.fishes = [
            LanternFish(age)
            for age
            in ages
        ]
        self.use_groups = use_groups

    def __str__(self):
        ages = [str(fish.age) for fish in self.fishes]
        s = ','.join(ages)
        return s

    def tick(self):
        total_new_fish = 0
        for fish in self.fishes:
            num_new_fish = fish.tick()
            total_new_fish += num_new_fish

        if self.use_groups:
            self.fishes.append(LanternFish(count=total_new_fish))
        else:
            # this inefficient code is kept to display visualization for part 1
            self.fishes.extend([LanternFish() for _ in range(total_new_fish)])

    @property
    def num_fish(self):
        total = sum([fish.count for fish in self.fishes])
        return total


class LanternFish:
    def __init__(self, age=8, count=1):
        self.age = age
        self.count = count

    def tick(self):
        num_new_fish = 0

        if self.age > 0:
            self.age -= 1
        else:
            self.age = 6
            num_new_fish = self.count

        return num_new_fish


if __name__ == '__main__':
    main()
