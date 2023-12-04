# Python Standard Library Imports
from dataclasses import dataclass
from functools import cached_property
from operator import (
    add,
    mul,
)

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (538046, 81709807)
config.TEST_CASES = {
    '': (4361, 467835),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        self.schematic = EngineSchematic(data)

    def solve1(self):
        answer = sum([_.value for _ in self.schematic.part_numbers])
        return answer

    def solve2(self):
        answer = sum(self.schematic.gear_ratios)
        return answer


@dataclass
class PartNumber:
    value: int
    row: int
    num_start: int
    num_end: int


@dataclass
class Symbol:
    row: int
    col: int

    def __hash__(self):
        return hash(self.coords)

    @property
    def coords(self):
        return (self.row, self.col)


class EngineSchematic:
    def __init__(self, data):
        self.grid = data
        self.M = len(self.grid)
        self.N = len(self.grid[0])

    @cached_property
    def part_numbers(self):
        """Scans engine schematic grid for numbers

        Not all numbers are part numbers; only numbers that are not adjacent
        (including diagonally) to symbols are part numbers.
        """
        part_numbers = []

        for i in range(self.M):
            current_num_start = None
            current_num_end = None
            for j in range(self.N):
                value = self.grid[i][j]
                if value.isdigit():
                    if current_num_start is None:
                        current_num_start = j
                    else:
                        pass
                else:
                    # not a digit
                    if current_num_start is not None:
                        current_num_end = j
                    else:
                        pass

                if (
                    current_num_start is not None
                    and current_num_end is not None
                ):
                    # found the start/end of a number
                    if self.has_adjacent_symbol(
                        i, current_num_start, current_num_end
                    ):
                        part_numbers.append(
                            self._make_part_number(
                                i, current_num_start, current_num_end
                            )
                        )
                    # reset start/end markers
                    current_num_start = current_num_end = None
                else:
                    pass

            if current_num_start is not None and current_num_end is None:
                # the number ran to the end of the line
                current_num_end = self.N
                if self.has_adjacent_symbol(
                    i, current_num_start, current_num_end
                ):
                    part_numbers.append(
                        self._make_part_number(
                            i, current_num_start, current_num_end
                        )
                    )

                # reset start/end markers
                current_num_start = current_num_end = None

        return part_numbers

    def _make_part_number(self, row, num_start, num_end):
        value = int(self.grid[row][num_start:num_end])
        return PartNumber(value, row, num_start, num_end)

    @property
    def gears(self):
        gears = []

        cogs_to_part_numbers_map = {}

        for part_number in self.part_numbers:
            cog = self.find_adjacent_cog(
                part_number.row, part_number.num_start, part_number.num_end
            )
            if cog is not None:
                other_part_number = cogs_to_part_numbers_map.get(cog)

                if other_part_number is not None:
                    gears.append((other_part_number.value, part_number.value))
                else:
                    pass

                cogs_to_part_numbers_map[cog] = part_number
            else:
                pass

        return gears

    @property
    def gear_ratios(self):
        gear_ratios = [mul(*gear) for gear in self.gears]
        return gear_ratios

    def find_adjacent_symbol(self, row, num_start, num_end, symbol_type=None):
        symbol = None

        for i in range(row - 1, row + 2):
            for j in range(num_start - 1, num_end + 1):
                if i < 0 or i >= self.M or j < 0 or j >= self.N:
                    # off the grid
                    pass
                else:
                    value = self.grid[i][j]
                    has_symbol_match = (
                        # match any symbol
                        symbol_type is None
                        and (value != '.' and not value.isdigit())
                    ) or (
                        # matches a specific symbol
                        symbol_type is not None
                        and value == symbol_type
                    )
                    if has_symbol_match:
                        symbol = Symbol(i, j)
                        break

            if symbol is not None:
                break

        return symbol

    def has_adjacent_symbol(self, row, num_start, num_end, symbol_type=None):
        symbol = self.find_adjacent_symbol(
            row, num_start, num_end, symbol_type=None
        )
        return symbol is not None

    def find_adjacent_cog(self, row, num_start, num_end):
        return self.find_adjacent_symbol(
            row, num_start, num_end, symbol_type='*'
        )


if __name__ == '__main__':
    main()
