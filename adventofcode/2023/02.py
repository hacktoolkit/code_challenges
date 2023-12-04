# Python Standard Library Imports
import re
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    list_product,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (2283, 78669)
config.TEST_CASES = {
    '': (8, 2286),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        self.games = [Game.from_raw(line) for line in self.data]

    def solve1(self):
        answer = sum([game.game_id for game in self.games if game.is_valid])
        return answer

    def solve2(self):
        answer = sum([game.power for game in self.games])
        return answer


@dataclass
class Game:
    GAME_ID_REGEX = re.compile(r'^Game (?P<game_id>\d+)$')
    MAX_CUBES = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    class Subset:
        def __init__(self, game_subset_str):
            """Example:

            `3 blue, 4 red`
            """

            def _extract_color_and_count(count_color_str):
                count, color = count_color_str.split()
                return color, int(count)

            self.cubes = dict(
                [
                    _extract_color_and_count(pair)
                    for pair in game_subset_str.split(', ')
                ]
            )

        @property
        def is_valid(self):
            is_valid = True
            for color, count in self.cubes.items():
                if count > Game.MAX_CUBES[color]:
                    is_valid = False
                    break

            return is_valid

    game_id: int
    subsets: list['Game.Subset']

    @classmethod
    def from_raw(cls, raw_game):
        """Example

        `Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green`
        """
        game_id_str, game_subsets_str = raw_game.split(':')

        game_id = int(cls.GAME_ID_REGEX.match(game_id_str).group('game_id'))
        subsets = [
            cls.Subset(game_subset_str.strip())
            for game_subset_str in game_subsets_str.split(';')
        ]

        game = cls(game_id=game_id, subsets=subsets)
        return game

    @property
    def is_valid(self):
        is_valid = all(subset.is_valid for subset in self.subsets)
        return is_valid

    @cached_property
    def min_cubes(self):
        cubes = defaultdict(int)
        for subset in self.subsets:
            for color, count in subset.cubes.items():
                cubes[color] = max(cubes[color], count)

        return cubes

    @property
    def power(self):
        result = list_product(list(self.min_cubes.values()))
        return result


if __name__ == '__main__':
    main()
