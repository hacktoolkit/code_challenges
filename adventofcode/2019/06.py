# Python Standard Library Imports
from collections import defaultdict

from utils import (
    BaseSolution,
    InputConfig,
    ingest,
)


PROBLEM_NUM = '06'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (344238, 436, )
# TEST_EXPECTED_ANSWERS = (42, None, )
TEST_EXPECTED_ANSWERS = (54, 4, )  # 06b.test.in


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
        # input_filename = f'{PROBLEM_NUM}.test.in'
        input_filename = f'{PROBLEM_NUM}b.test.in'
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

    def solve1(self):
        orbit_map = OrbitMap(self.data)

        answer = orbit_map.total_orbits
        return answer

    def solve2(self):
        orbit_map = OrbitMap(self.data)

        answer = orbit_map.distance('YOU', 'SAN')
        return answer


class OrbitMap:
    def __init__(self, raw_orbits):
        self.orbits = {}

        for raw_orbit in raw_orbits:
            a, b = raw_orbit.split(')')
            self.orbits[b] = a

    @property
    def total_orbits(self):
        total = 0

        for obj in self.orbits.keys():
            if obj != 'COM':
                total += self.count_ancestors(obj)

        return total

    def count_ancestors(self, obj):
        node = obj
        count = 0

        while not self.is_root(node):
            node = self.parent_of(node)
            count += 1

        return count

    def is_root(self, obj):
        return obj == 'COM'

    def parent_of(self, obj):
        return self.orbits[obj]

    def find_common_ancestor(self, a, b):
        common_ancestor = None

        a_ancestors = {}

        while not self.is_root(a):
            a = self.parent_of(a)
            a_ancestors[a] = True

        while not self.is_root(b):
            b = self.parent_of(b)
            if b in a_ancestors:
                common_ancestor = b
                break

        return common_ancestor

    def distance_to_ancestor(self, node, ancestor):
        distance = 0
        while node != ancestor:
            node = self.parent_of(node)
            distance += 1

        return distance

    def distance(self, a, b):
        common_ancestor = self.find_common_ancestor(a, b)

        dist_a = self.distance_to_ancestor(a, common_ancestor)
        dist_b = self.distance_to_ancestor(b, common_ancestor)

        distance = dist_a + dist_b - 2
        return distance


if __name__ == '__main__':
    main()
