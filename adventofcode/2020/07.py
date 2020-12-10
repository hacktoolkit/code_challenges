# Python Standard Library Imports
import re
from collections import defaultdict

from utils import ingest


INPUT_FILE = '7.in'
EXPECTED_ANSWERS = (155, 54803, )

# INPUT_FILE = '7.test.in'
# EXPECTED_ANSWERS = (4, 32, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)

        self.bag_rules = [BagRule(rule) for rule in self.data]

        self.bag_map = BagMap(self.bag_rules)

    def solve1(self):
        all_colors = []

        visited = {}

        colors = ['shiny gold']

        while len(colors) > 0:
            new_colors = []

            for color in colors:
                if color not in visited:
                    visited[color] = True

                    cur_colors = self.bag_map.reversed_m[color]
                    all_colors.extend(cur_colors)
                    new_colors.extend(cur_colors)

            colors = new_colors

        answer = len(set(all_colors))
        return answer

    def solve2(self):
        answer = self.bag_map.count_bags('shiny gold')
        return answer


CONTAINS_REGEX = re.compile(r'^(?P<count>\d+) (?P<color>.*) bags?$')


class BagRule:
    def __init__(self, rule):
        self.rule = rule

        bag_color, contents = [x.strip() for x in rule.split('contain')]

        self.bag_color = bag_color.rstrip('bags').strip()

        self.contents = {}

        contents = [content.strip() for content in contents.rstrip('.').split(',')]
        for content in contents:
            if content == 'no other bags':
                pass
            else:
                m = CONTAINS_REGEX.match(content)
                if m:
                    count, color = (
                        int(m.group('count')),
                        m.group('color'),
                    )
                    self.contents[color] = count


class BagMap:
    def __init__(self, bag_rules):
        self.m = {}

        reversed_m = defaultdict(list)

        for bag_rule in bag_rules:
            outer_color = bag_rule.bag_color
            contents = bag_rule.contents

            self.m[outer_color] = contents
            for inner_color in contents.keys():
                reversed_m[inner_color].append(outer_color)

        # self.reversed_m = dict(reversed_m)
        self.reversed_m = reversed_m

    def count_bags(self, color):
        children = self.m[color]

        total = 0
        for child, count in children.items():
            total += count + count * self.count_bags(child)

        return total


if __name__ == '__main__':
    main()
