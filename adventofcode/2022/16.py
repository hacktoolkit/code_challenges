# Python Standard Library Imports
import re
import typing as T
from dataclasses import (
    dataclass,
    field,
)
from functools import cache

from utils import (
    RE,
    BaseSolution,
    Edge,
    Graph,
    InputConfig,
    Vertex,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (2056, 2513)
config.TEST_CASES = {
    '': (1651, 1707),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        self.volcano = Volcano(data)

    def solve1(self):
        volcano = self.volcano

        answer = volcano.maximize_pressure_release()
        return answer

    def solve2(self):
        volcano = self.volcano

        answer = volcano.maximize_pressure_release(
            ticks=Volcano.ELEPHANT_TURNS, elephant=True
        )
        return answer


@dataclass
class Valve:
    REGEX = re.compile(
        r'^Valve (?P<name>\w+) has flow rate=(?P<flow_rate>\d+); tunnels? leads? to valves? (?P<valves>[\w ,]+)$'
    )

    name: str
    flow_rate: int = 0
    tunnels: list['str'] = field(default_factory=list)

    @classmethod
    def from_raw(cls, raw):
        keys = ['name', 'flow_rate', 'valves']
        transforms = [lambda x: x, int, lambda x: x.split(', ')]
        if RE.match(cls.REGEX, raw):
            values = [
                transform(RE.m.group(key))
                for (key, transform) in zip(keys, transforms)
            ]
            valve = cls(*values)
        else:
            raise Exception(f'Bad raw input: {raw}')

        return valve

    def as_vertex(self):
        vertex = Vertex(self.name, self.flow_rate)
        return vertex


class Volcano(Graph):
    ELEPHANT_TURNS = 26

    def __init__(self, data):
        super(Volcano, self).__init__()

        valves = [Valve.from_raw(line) for line in data]

        for valve in valves:
            vertex = valve.as_vertex()
            self.add_vertex(vertex, map_by_label=True)

        for valve in valves:
            source = self.vertices_by_label[valve.name]
            for tunnel in valve.tunnels:
                sink = self.vertices_by_label[tunnel]
                edge = Edge(source, sink, weight=1)
                self.add_edge(edge)

        # calculate shortest path from every vertex to every other vertex
        self.dist = self.all_shortest_paths()

    def maximize_pressure_release(self, ticks=30, elephant=False):
        source = self.vertices_by_label['AA']
        closed_valves = frozenset(v for v in self.vertices if v.weight > 0)
        pressure_released = self.dp(
            source, ticks, closed_valves, elephant=elephant
        )
        return pressure_released

    @cache
    def dp(
        self,
        source: Vertex,
        ticks: int,
        closed_valves: frozenset,
        elephant: bool = False,
    ):
        pressure_released = (
            # dispatch the elephant to open the remaining closed valves
            self.dp(
                self.vertices_by_label['AA'],
                self.ELEPHANT_TURNS,
                closed_valves,
                elephant=False,
            )
            if elephant
            # no elephant available to open values
            else 0
        )

        for target in closed_valves:
            # time to travel to `target` valve and open it
            next_tick = ticks - self.dist[source][target] - 1
            if next_tick >= 0:
                pressure_released = max(
                    # skip `target` and evaluate the next available closed valve
                    pressure_released,
                    # move to the `target` valve and open it
                    (
                        # cumulative pressure released by opening `target` valve
                        target.weight * next_tick
                        + self.dp(
                            target,
                            next_tick,
                            closed_valves - {target},
                            elephant=elephant,
                        )
                    ),
                )
        return pressure_released


if __name__ == '__main__':
    main()
