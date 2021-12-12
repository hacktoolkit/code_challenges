# Python Standard Library Imports
import itertools
from collections import defaultdict

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '12'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (4885, 117905, )
# TEST_EXPECTED_ANSWERS = (10, 36, )  # 12a.test.in
TEST_EXPECTED_ANSWERS = (19, 103, )  # 12b.test.in
# TEST_EXPECTED_ANSWERS = (226, 3509, )  # 12c.test.in


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


# Python Standard Library Imports
import copy


class Solution(BaseSolution):
    def process_data(self):
        data = self.data

    def solve1(self):
        graph = Graph(self.data)
        paths = graph.dfs('start')
        answer = len(paths)
        return answer

    def solve2(self):
        graph = Graph(self.data, mode=2)
        paths = graph.dfs('start')
        # paths_str = set([','.join(path) for path in paths])
        # print(paths_str)
        # answer = len(paths_str)
        answer = len(paths)
        return answer


class Graph:
    def __init__(self, raw_paths, mode=1):
        self.G = defaultdict (list)
        self.mode = mode

        for path in raw_paths:
            a, b = path.split('-')
            self.add_path(a, b)

    def add_path(self, a, b):
        if b != 'start':
            self.G[a].append(b)
        if a != 'start' and b != 'end':
            self.G[b].append(a)

    def is_small_cave(self, cave):
        return cave.lower() == cave

    def dfs(self, node, path=None, visited=None):
        if visited is None:
            visited = defaultdict(int)

        if path is None:
            path = []

        G = self.G

        def _dfs(child, path, visited):
            path_copy = copy.copy(path)
            visited_copy = copy.copy(visited)
            child_paths = self.dfs(
                child,
                path=path_copy,
                visited=visited_copy
            )
            return child_paths

        if not self.can_visit_cave(node, visited):
            return None
        else:
            path.append(node)
            if self.is_small_cave(node):
                visited[node] += 1

            if node == 'end':
                return path
            else:
                paths = []
                for child in G[node]:
                    child_paths = _dfs(child, path, visited)
                    if child_paths is None or len(child_paths) == 0:
                        pass
                    elif type(child_paths[0]) == list:
                        for child_path in child_paths:
                            if child_path is not None:
                                paths.append(child_path)
                            else:
                                pass
                    else:
                        paths.append(child_paths)

        return paths

    def can_visit_cave(self, node, visited):
        can_visit = True
        if self.is_small_cave(node):
            if node in visited:
                if self.mode == 1:
                    # a small cave can only be visited once
                    can_visit = False
                elif self.mode == 2:
                    # only a single small cave can be visited at most twice
                    # remaining small caves can be visited at most once
                    visit_counts = set(list(visited.values()))
                    if 2 in visit_counts:
                        # another cave has already been visited twice
                        can_visit = False
                    else:
                        pass
                else:
                    raise Exception('Invalid mode')

        return can_visit


if __name__ == '__main__':
    main()
