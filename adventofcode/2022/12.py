# Python Standard Library Imports
import copy
from collections import deque

from utils import (
    BaseSolution,
    Graph,
    InputConfig,
    Vertex,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (481, 480)
config.TEST_CASES = {
    '': (31, 29),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data

    def solve1(self):
        hill = Hill(self.data)
        answer = hill.best_climb()
        return answer

    def solve2(self):
        hill = Hill(self.data, is_part2=True)
        answer = hill.best_climb()
        return answer


class Hill:
    ELEVATION_MAP = {'S': 'a', 'E': 'z'}

    def __init__(self, raw, is_part2=False):
        self.grid = [[c for c in line] for line in raw]

        self.M = len(self.grid)
        self.N = len(self.grid[0])

        self.starts = set()
        self.end = None

        def found_starts_and_end():
            return (
                not is_part2 and len(self.starts) > 0
            ) and self.end is not None

        # find start(s) and end
        for m in range(self.M):
            for n in range(self.N):
                cell = self.grid[m][n]
                if (not is_part2 and cell == 'S') or (
                    is_part2 and cell in ('a', 'S')
                ):
                    self.starts.add((m, n))
                elif cell == 'E':
                    self.end = (m, n)
                else:
                    pass

                if found_starts_and_end():
                    break

            if found_starts_and_end():
                break

        # build a graph to represent the hill
        graph = P12Graph(self)
        for m in range(self.M):
            for n in range(self.N):
                coord = (m, n)
                vertex = P12Vertex(coord, weight=self.elevation(m, n))
                graph.add_vertex(vertex, map_by_label=True)

        self.graph = graph

    def neighbors(self, i, j):
        """Returns all valid neighbors of `(i, j)`

        Spots off grid are not valid.
        """
        elevation = self.elevation(i, j)

        neighbors = []
        for (dy, dx) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            i2, j2 = i + dy, j + dx
            if 0 <= i2 < self.M and 0 <= j2 < self.N:
                elevation2 = self.elevation(i2, j2)
                if (elevation2 - elevation) <= 1:
                    neighbors.append((i2, j2))
                else:
                    debug(
                        f'Cannot proceed from {(i, j)} to {(i2, j2)}: requires climbing gear'
                    )
            else:
                # out of bounds
                pass

        return neighbors

    def elevation(self, i, j):
        value = self.grid[i][j]
        elevation = ord(self.ELEVATION_MAP.get(value, value)) - ord('a')
        # debug(f'Elevation at {(i,j)}: {elevation} ({value})')
        return elevation

    def best_climb(self):
        """Returns the most optimal cost to ravel from any start to `E`"""
        best_distance = None

        for (i, j) in self.starts:

            start_vertex = self.graph.vertices_by_label[(i, j)]
            end_vertex = self.graph.vertices_by_label[self.end]
            # value = self.climb__naive(i, j)  # janky DFS implementation
            # value = self.climb__bfs(start_vertex, end_vertex)
            value = self.climb__dijkstra(start_vertex, end_vertex)

            if best_distance is None or value and value < best_distance:
                best_distance = value

            # housekeeping
            self.graph.reset_vertices()

        return best_distance

    def climb__bfs(self, source, target):
        path, distance = self.graph.bfs(source, target)
        return (distance - 1) if distance else None

    def climb__dijkstra(self, source, target):
        path, distance = self.graph.shortest_path(source, target)
        return (len(path) - 1) if path else None

    def climb__naive(self, i, j, visited=None):
        """Returns the most optimal cost to travel from `(i, j)` to `E`

        Naive implementation using DFS
        """
        if visited is None:
            visited = set()

        debug(
            f'Finding best path from {(i,j)} to {self.end}. Visited nodes: {visited}'
        )

        if self.grid[i][j] == 'E':
            result = 0
        else:
            visited.add((i, j))

            routes = []

            for (i2, j2) in self.neighbors(i, j):
                if (i2, j2) in visited:
                    debug(
                        f'Cannot proceed from {(i, j)} to {(i2, j2)}: already visited'
                    )
                else:
                    # neighbor is a valid candidate
                    next_visted = copy.deepcopy(visited)
                    path = self.climb__naive(i2, j2, copy.deepcopy(visited))
                    if path is None:
                        # not a valid path
                        pass
                    else:
                        # a valid climbing path
                        routes.append(1 + path)

            result = min(routes) if routes else None

        return result

    def climb__naive(self, i, j, visited=None):
        """Returns the most optimal cost to travel from `(i, j)` to `E`

        Naive implementation
        """
        if visited is None:
            visited = set()

        debug(
            f'Finding best path from {(i,j)} to {self.end}. Visited nodes: {visited}'
        )

        if self.grid[i][j] == 'E':
            result = 0
        else:
            visited.add((i, j))

            routes = []

            for (i2, j2) in self.neighbors(i, j):
                if (i2, j2) in visited:
                    debug(
                        f'Cannot proceed from {(i, j)} to {(i2, j2)}: already visited'
                    )
                else:
                    # neighbor is a valid candidate
                    next_visted = copy.deepcopy(visited)
                    path = self.climb__naive(i2, j2, copy.deepcopy(visited))
                    if path is None:
                        # not a valid path
                        pass
                    else:
                        # a valid climbing path
                        routes.append(1 + path)

            result = min(routes) if routes else None

        return result


class P12Graph(Graph):
    def __init__(self, hill, *args, **kwargs):
        self.hill = hill
        super(P12Graph, self).__init__(*args, **kwargs)

    def neighbors_of(self, vertex, color=None):
        """Finds the neighbors of `vertex`

        If `color` is provided, the neighbor must be of that color.

        Utilizes coordinate shifts on `self.vertices_by_label`

        Returns a collection of `(Vertex, edge-weight)` pairs
        """
        coord = vertex.label
        i, j = coord

        neighbors = set()
        for (dy, dx) in [
            (-1, 0),  # above
            (1, 0),  # below
            (0, -1),  # left
            (0, 1),  # right
        ]:
            i2, j2 = i + dy, j + dx
            neighbor = self.vertices_by_label.get((i2, j2))
            if (
                neighbor
                and (color is None or neighbor.color == color)
                and (neighbor.weight - vertex.weight) <= 1
            ):
                neighbors.add((neighbor, 1))
            else:
                # invalid neighbor
                pass

        return neighbors


class P12Vertex(Vertex):
    def __repr__(self):
        return f'V({self.label}, {self.weight})'

    def __str__(self):
        return str(self.__repr__())


if __name__ == '__main__':
    main()
