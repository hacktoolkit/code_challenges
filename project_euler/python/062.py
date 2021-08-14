#!/usr/bin/env python3
"""http://projecteuler.net/problem=062

Cubic permutations

The cube, 41063625 (345^3), can be permuted to produce two other cubes: 56623104 (384^3) and 66430125 (405^3). In fact, 41063625 is the smallest cube which has exactly three permutations of its digits which are also cube.

Find the smallest cube for which exactly five permutations of its digits are cube.

Solution by jontsai <hello@jontsai.com>
"""
# Python Standard Library Imports
import json
from collections import defaultdict

# PE Solution Library Imports
from utils import *


class Solution(object):
    # TARGET, EXPECTED_ANSWER = 3, 41063625
    TARGET, EXPECTED_ANSWER = 5, 127035954683

    def __init__(self):
        with open('cubes.json') as f:
            cube_roots_dict = json.loads(f.read())
            self.cube_roots = {
                int(k): v
                for k, v
                in cube_roots_dict.items()
            }

    def solve(self):
        answer = None

        buckets = defaultdict(lambda: [])

        for cube in sorted(self.cube_roots.keys()):
            cube_root = self.cube_roots[cube]
            key = ''.join(sorted(str(cube)))
            bucket = buckets[key]
            bucket.append(cube_root)
            if len(bucket) == self.TARGET:
                answer = bucket[0] ** 3
                break

        return answer

    def solve_slow(self):
        answer = None

        for cube in sorted(self.cube_roots.keys()):
            cube_root = self.cube_roots[cube]
            cubes = self.get_cubic_permutations(cube)
            if len(cubes) == self.TARGET:
                print(cubes)
                answer = cube
                break
            else:
                pass

        return answer

    def get_cubic_permutations(self, cube):
        """Get permutations of `cube` which are also cubes
        """

        cubes = [
            p for p in numeric_permutations(cube)
            if p in self.cube_roots
        ]
        return cubes


def main():
    solution = Solution()
    answer = solution.solve()

    print(f'Expected: {Solution.EXPECTED_ANSWER}, Answer: {answer}')


if __name__ == '__main__':
    main()
