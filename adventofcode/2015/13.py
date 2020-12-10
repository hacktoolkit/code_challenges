# Python Standard Library Imports
import re
from collections import defaultdict
from itertools import permutations

from utils import (
    Re,
    ingest,
)


INPUT_FILE = '13.in'
EXPECTED_ANSWERS = (618, 601, )

# INPUT_FILE = '13.test.in'
# EXPECTED_ANSWERS = (330, 286, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)
        self.seating_chart = SeatingChart(self.data)

    def solve1(self):
        best_arrangment, best_score = self.seating_chart.find_optimal_seating()
        answer = best_score
        return answer

    def solve2(self):
        self.seating_chart.add_player('undefined_player')
        best_arrangment, best_score = self.seating_chart.find_optimal_seating()
        answer = best_score
        return answer


class SeatingChart:
    SEATING_REGEX = re.compile(r'^(?P<name>[A-Z][a-z]+) would (?P<change>(gain)|(lose)) (?P<amount>\d+) happiness units by sitting next to (?P<partner>[A-Z][a-z]+)\.$')

    def __init__(self, rules):
        self.rules = rules

        chart = defaultdict(lambda: defaultdict(int))

        for rule in rules:
            regex = Re()
            if regex.match(self.SEATING_REGEX, rule):
                m = regex.last_match
                name, change, amount, partner = (
                    m.group('name'),
                    m.group('change'),
                    int(m.group('amount')),
                    m.group('partner'),
                )
                multiplier = 1 if change == 'gain' else -1
                score = multiplier * amount

                chart[name][partner] = score
            else:
                raise Exception('Bad seating rule: %s' % rule)

        self.chart = chart
        self.players = sorted(list(chart.keys()))

    def add_player(self, name):
        self.players.append(name)

    def find_optimal_seating(self):
        """Variant of stable marriage problem

        https://en.wikipedia.org/wiki/Stable_marriage_problem
        https://en.wikipedia.org/wiki/Gale%E2%80%93Shapley_algorithm
        """
        best_arrangement = None
        best_score = None

        num_players = len(self.players)

        for p in permutations(self.players):
            score = 0
            for i in range(num_players):
                player = p[i]
                neighbors = (
                    p[(i+1) % num_players],
                    p[(i-1) % num_players],
                )
                for neighbor in neighbors:
                    score += self.chart[player][neighbor]

            if best_arrangement is None or score > best_score:
                best_arrangement = p
                best_score = score

        return best_arrangement, best_score


if __name__ == '__main__':
    main()
