# Python Standard Library Imports
import copy
import heapq

from utils import (
    BaseSolution,
    config,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (69912, 208180)
config.TEST_CASES = {
    '': (24000, 45000),
}

config.INPUT_CONFIG.as_integers = False
config.INPUT_CONFIG.as_comma_separated_integers = False
config.INPUT_CONFIG.as_json = False
config.INPUT_CONFIG.as_groups = True
config.INPUT_CONFIG.strip_lines = True
config.INPUT_CONFIG.as_oneline = False
config.INPUT_CONFIG.as_coordinates = False
config.INPUT_CONFIG.coordinate_delimeter = None
config.INPUT_CONFIG.as_table = False
config.INPUT_CONFIG.row_func = None
config.INPUT_CONFIG.cell_func = None


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data

    def solve1(self):
        max_calories = None
        for elf in self.data:
            calories = sum(map(int, elf))
            if max_calories is None or calories > max_calories:
                max_calories = calories

        answer = max_calories
        return answer

    def solve2(self):
        podium = []
        for elf in self.data:
            calories = sum(map(int, elf))
            heapq.heappush(podium, calories)
            podium = heapq.nlargest(3, podium)

        answer = sum(podium)
        return answer


if __name__ == '__main__':
    main()
