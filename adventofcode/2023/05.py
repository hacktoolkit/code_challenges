# Python Standard Library Imports
import copy
import heapq
import math
import re
import typing as T
from collections import (
    defaultdict,
    deque,
)
from dataclasses import (
    dataclass,
    field,
)
from functools import (
    cache,
    lru_cache,
)
from itertools import (
    combinations,
    permutations,
    product,
)
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


config.EXPECTED_ANSWERS = (403695602, None)
config.TEST_CASES = {
    '': (35, None),
    # 'b': (None, None),
    # 'c': (None, None),
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
        self.garden = Garden(self.data)

    def solve1(self):
        lowest_location = None
        for seed_id in self.garden.seeds:
            location_id = self.garden.convert_seed_to_location(seed_id)
            if lowest_location is None or location_id < lowest_location:
                lowest_location = location_id

        answer = lowest_location
        return answer

    def solve2(self):
        #
        # TODO: FILL THIS IN
        #
        answer = None
        return answer


class Garden:
    """Start with seeds, end with locations

    Perform "stoichiometry" with each pairing
    - seed
    - soil
    - fertilizer
    - water
    - light
    - temperature
    - humidity
    - location
    """

    CONVERSIONS = {
        'seed': 'soil',
        'soil': 'fertilizer',
        'fertilizer': 'water',
        'water': 'light',
        'light': 'temperature',
        'temperature': 'humidity',
        'humidity': 'location',
    }

    class ObjectMap:
        def __init__(self, raw_group_data):
            ranges = []
            for line in raw_group_data:
                destination_range_start, source_range_start, range_length = [
                    int(_) for _ in line.split()
                ]
                ranges.append(
                    (source_range_start, destination_range_start, range_length)
                )

            self.ranges = ranges

        def convert(self, src):
            dest = src
            for (
                source_range_start,
                destination_range_start,
                range_length,
            ) in self.ranges:
                if (
                    source_range_start
                    <= src
                    < source_range_start + range_length
                ):
                    dest = destination_range_start + (src - source_range_start)
                    break

            return dest

    def __init__(self, raw_garden_data):
        for raw_group_data in raw_garden_data:
            self._process_group(raw_group_data)

    def _process_group(self, raw_group_data):
        group_heading = raw_group_data[0]
        category = self._extract_group_category(group_heading)

        if category == 'seeds':
            self.seeds = [int(_) for _ in raw_group_data[0].split()[1:]]
        elif category.endswith('map'):
            print(category)
            object_map = self.ObjectMap(raw_group_data[1:])
            setattr(self, category, object_map)
        else:
            raise Exception(f'Unexpected category: {category}')

    def _extract_group_category(self, group_heading):
        if group_heading.startswith('seeds:'):
            category = 'seeds'
        elif group_heading.endswith('map:'):
            category = (
                group_heading[:-1].lower().replace('-', '_').replace(' ', '_')
            )
        else:
            raise Exception(f'Unexpected group heading: {group_heading}')

        return category

    def convert_seed_to_location(self, seed_id):
        src_id = seed_id
        for src, dest in self.CONVERSIONS.items():
            dest_id = self.convert_obj(src_id, src, dest)
            src_id = dest_id

        return dest_id

    def convert_obj(self, src_id, src, dest):
        dest_id = getattr(self, f'{src}_to_{dest}_map').convert(src_id)
        return dest_id


if __name__ == '__main__':
    main()