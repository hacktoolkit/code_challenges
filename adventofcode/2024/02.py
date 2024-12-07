# Python Standard Library Imports
import typing as T
from dataclasses import dataclass
from itertools import pairwise

# Third Party (PyPI) Imports
from htk import fdb  # noqa: F401

from utils import debug  # noqa: F401
from utils import (
    BaseSolution,
    config,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (287, 354)
config.TEST_CASES = {
    '': (2, 4),
}

config.INPUT_CONFIG.as_integers = False
config.INPUT_CONFIG.as_comma_separated_integers = False
config.INPUT_CONFIG.as_json = False
config.INPUT_CONFIG.as_groups = False
config.INPUT_CONFIG.strip_lines = True
config.INPUT_CONFIG.as_oneline = False
config.INPUT_CONFIG.as_coordinates = False
config.INPUT_CONFIG.coordinate_delimeter = None
config.INPUT_CONFIG.as_table = True
config.INPUT_CONFIG.row_func = None
config.INPUT_CONFIG.cell_func = int


@dataclass
class Report:
    levels: list[int]

    @classmethod
    def from_raw(cls, levels):
        report = cls(levels)
        return report

    def is_safe(self, with_dampeners=False) -> bool:
        result = self._is_safe(self.levels)
        if not result and with_dampeners:
            for i in range(len(self.levels)):
                # try skipping ith level
                levels = self.levels[:i] + self.levels[i + 1 :]  # noqa: E203
                result = self._is_safe(levels)
                if result:
                    break

        return result

    def _is_safe(self, levels) -> bool:
        result = (
            self.is_strictly_increasing(levels)
            or self.is_strictly_decreasing(levels)
        ) and self.is_level_deltas_within_tolerance(levels)
        return result

    def is_strictly_increasing(self, levels) -> bool:
        result = True
        for a, b in pairwise(levels):
            if a >= b:
                result = False
                break

        return result

    def is_strictly_decreasing(self, levels) -> bool:
        result = True
        for a, b in pairwise(levels):
            if a <= b:
                result = False
                break

        return result

    def is_level_deltas_within_tolerance(self, levels) -> bool:
        tol_low = 1
        tol_high = 3

        result = True
        for a, b in pairwise(levels):
            if not (tol_low <= abs(a - b) <= tol_high):
                result = False
                break

        return result


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data

        self.reports = [Report.from_raw(_) for _ in data]

    def solve1(self) -> T.Optional[int]:
        answer = len([_ for _ in self.reports if _.is_safe()])
        return answer

    def solve2(self) -> T.Optional[int]:
        answer = len(
            [_ for _ in self.reports if _.is_safe(with_dampeners=True)]
        )
        return answer


if __name__ == '__main__':
    main()
