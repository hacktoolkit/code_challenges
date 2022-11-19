# Python Standard Library Imports
import copy
import math
import re
from collections import defaultdict
from dataclasses import (
    dataclass,
    fields,
)

from utils import (
    BaseSolution,
    InputConfig,
    Re,
)


PROBLEM_NUM = '03'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (
    109716,
    124,
)
TEST_EXPECTED_ANSWERS = (
    4,
    3,
)


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=False,
        row_func=None,
        cell_func=None,
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

        claims = [claim for line in data if (claim := Claim.from_line(line))]
        self.fabric = Fabric(claims)

    def solve1(self):
        fabric = self.fabric
        answer = fabric.count_overlapping_cells()
        return answer

    def solve2(self):
        fabric = self.fabric
        non_overlapping_claim = fabric.find_non_overlapping_claim()
        answer = non_overlapping_claim.num
        return answer


@dataclass
class Claim:
    num: int
    left: int
    top: int
    width: int
    height: int

    REGEX = re.compile(
        r'^#(?P<num>\d+) @ (?P<left>\d+),(?P<top>\d+): (?P<width>\d+)x(?P<height>\d+)$'
    )

    @classmethod
    def from_line(cls, line):
        regex = Re()
        if regex.match(cls.REGEX, line):
            m = regex.last_match
            kwargs = {
                field.name: int(m.group(field.name)) for field in fields(cls)
            }
            obj = cls(**kwargs)
        else:
            obj = None
        return obj


class Fabric:
    def __init__(self, claims):
        self.claims = claims

        self.grid = defaultdict(int)
        self._process_claims()

    def _process_claims(self):
        for claim in self.claims:
            x = claim.left
            y = claim.top
            for dx in range(claim.width):
                for dy in range(claim.height):
                    coord = (x + dx, y + dy)
                    self.grid[coord] += 1

    def count_overlapping_cells(self):
        count = 0
        for coord, num_claims in self.grid.items():
            if num_claims >= 2:
                count += 1
        return count

    def find_non_overlapping_claim(self):
        non_overlapping_claim = None

        for claim in self.claims:
            has_overlap = False
            x = claim.left
            y = claim.top
            for dx in range(claim.width):
                for dy in range(claim.height):
                    coord = (x + dx, y + dy)
                    if self.grid[coord] > 1:
                        has_overlap = True
                        break
                if has_overlap:
                    break

            if not has_overlap:
                non_overlapping_claim = claim
                break

        return non_overlapping_claim


if __name__ == '__main__':
    main()
