# Python Standard Library Imports
import math
from dataclasses import dataclass

from utils import (
    BaseSolution,
    InputConfig,
    gauss_sum,
)


PROBLEM_NUM = '17'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (6555, 4973, )
TEST_EXPECTED_ANSWERS = (45, 112, )


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=False,
        row_func=None,
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
        parts = data[0].removeprefix('target area: ').split(', ')
        x1, x2 = [int(n) for n in parts[0].removeprefix('x=').split('..')]
        y1, y2 = [int(n) for n in parts[1].removeprefix('y=').split('..')]
        self.target_area = Rect(x1=x1, x2=x2, y1=y1, y2=y2)

    def solve1(self):
        target_area = self.target_area

        min_dx = 1
        max_dx = target_area.x2
        min_dy = target_area.y1 if target_area.y1 <= 0 else 1

        self.total_solutions = 0

        best_dx, best_dy, best_y = None, None, None
        for dx in range(min_dx, max_dx + 1):
            max_steps = 0
            x = 0
            dx_trial = dx
            while x < target_area.x2 and dx_trial > 0:
                x += dx_trial
                dx_trial -= 1
                max_steps += 1

            # guess and check/brute force ?
            # attempt to intelligently calculate an upper bound for dy based on max_steps
            # max_dy = 120
            max_dy = 2 * max_steps + abs(target_area.y1)
            for dy in range(min_dy, max_dy + 1):
                probe = Probe(dx=dx, dy=dy, target_area=target_area)
                probe.launch()
                if probe.has_arrived:
                    self.total_solutions += 1
                    if best_y is None or probe.max_y > best_y:
                        best_dx, best_dy, best_y = dx, dy, probe.max_y
                    else:
                        pass
                else:
                    pass


        print(best_dx, best_dy, best_y)

        answer = best_y
        return answer

    def solve2(self):
        answer = self.total_solutions
        return answer


@dataclass
class Rect:
    x1: int
    x2: int
    y1: int
    y2: int

    def __str__(self):
        s = f'x={self.x1}..{self.x2}, y={self.y1}..{self.y2}'
        return s

    def contains_point(self, x, y):
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2


@dataclass
class Probe:
    dx: int
    dy: int
    target_area: Rect
    x: int = 0
    y: int = 0
    max_y: int = 0
    step_count: int = 0

    def launch(self):
        while not self.has_arrived and not self.has_passed_target:
            self.step()

    def step(self):
        # update position
        self.x += self.dx
        self.y += self.dy

        # update velocity
        ddx = -1 if self.dx > 0 else 1 if self.dx < 0 else 0
        ddy = -1
        self.dx += ddx
        self.dy += ddy

        # update meta
        self.max_y = max(self.max_y, self.y)
        self.step_count += 1

    @property
    def has_arrived(self):
        return self.target_area.contains_point(self.x, self.y)

    @property
    def has_passed_target(self):
        has_passed = (
            (self.dx == 0 and self.y < self.target_area.y1)
            or (self.dx > 0 and self.x > self.target_area.x2)
            or (self.dy < 0 and self.y < self.target_area.y1)
        )
        return has_passed


if __name__ == '__main__':
    main()
