# Python Standard Library Imports
import heapq
import typing as T

from utils import (
    BaseSolution,
    Graph,
    Vertex,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (415, 2864)
config.TEST_CASES = {
    '': (40, 315),
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
config.INPUT_CONFIG.row_func = lambda row: row[0]
config.INPUT_CONFIG.cell_func = lambda line: [int(d) for d in line]


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data

        self.matrix = data
        self.matrix2 = self.build_tiled_matrix(data, 5)

    def build_tiled_matrix(self, matrix, n):
        # tile horizontally first
        horizontal = [
            [(v + k - 1) % 9 + 1 for k in range(n) for v in row]
            for row in matrix
        ]

        # tile vertically
        vertical = [
            [(v + k - 1) % 9 + 1 for v in row]
            for k in range(n)
            for row in horizontal
        ]

        return vertical

    def solve1(self):
        answer = self.shortest_path(self.matrix)
        return answer

    def solve2(self):
        answer = self.shortest_path(self.matrix2)
        return answer

    def shortest_path(self, matrix):
        # Dijkstra's algorithm using utils.Graph data structure
        result = self.shortest_path__graph(matrix)

        # Dijkstra's algorithm in-place
        # result = self.shortest_path__matrix(matrix)

        return result

    def shortest_path__graph(self, matrix):
        graph = P15Graph()
        for i, row in enumerate(matrix):
            for j, weight in enumerate(row):
                coord = (i, j)
                vertex = Vertex(coord, weight=weight)
                graph.add_vertex(vertex, map_by_label=True)

        start_coord = (0, 0)
        end_coord = (len(matrix) - 1, len(matrix[0]) - 1)
        source = graph.vertices_by_label[start_coord]
        target = graph.vertices_by_label[end_coord]
        path, distance, distances = graph.shortest_path(source, target)

        # do not enter first cell
        return distance - source.weight

    def shortest_path__matrix(self, matrix):
        """Calculates the shortest path to traverse matrix

        Starting from `(0, 0)`
        Ending at `(m, n)`

        Where:
        - `m = self.M - 1`
        - `n = self.N - 1`

        References:
        - https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Using_a_priority_queue
        - https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
        """
        M = len(matrix)
        N = len(matrix[0])

        INF = 10**9
        best_distances = [[INF] * N for _ in range(M)]

        pq = [(0, 0, 0)]  # (priority, i, j)
        while pq:
            dist, i, j = heapq.heappop(pq)

            shifts = [
                (i - 1, j),  # above
                (i + 1, j),  # below
                (i, j - 1),  # left
                (i, j + 1),  # right
            ]

            for a, b in shifts:
                # only check valid neighbors
                if 0 <= a < M and 0 <= b < N:
                    alt_dist = dist + matrix[a][b]
                    if alt_dist < best_distances[a][b]:
                        # add to priority queue if `alt_dist` is better
                        best_distances[a][b] = alt_dist
                        heapq.heappush(pq, (alt_dist, a, b))

        shortest_path = best_distances[-1][-1]
        return shortest_path


class P15Graph(Graph):
    def neighbors_of(self, vertex) -> T.Collection[T.Tuple['Vertex', int]]:
        """Finds the neighbors of `vertex`

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
            if neighbor:
                neighbors.add((neighbor, neighbor.weight))

        return neighbors


if __name__ == '__main__':
    main()
