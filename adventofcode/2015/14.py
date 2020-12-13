# Python Standard Library Imports
import re
from collections import defaultdict

from utils import (
    Re,
    ingest,
)


RACE_DURATION = 2503
INPUT_FILE = '14.in'
EXPECTED_ANSWERS = (2660, 1256, )

# RACE_DURATION = 1000
# INPUT_FILE = '14.test.in'
# EXPECTED_ANSWERS = (1120, 689, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        data = ingest(INPUT_FILE)
        reindeer = [Reindeer(r) for r in data]

        self.santa = Santa(reindeer)
        self.santa.conduct_race(RACE_DURATION)

    def solve1(self):
        r, distance = self.santa.distance_leaders

        answer = distance
        return answer

    def solve2(self):
        r, points = self.santa.point_leaders

        answer = points
        return answer


class Santa:
    def __init__(self, reindeer):
        self.reindeer = reindeer
        self.points = defaultdict(int)

    @property
    def distance_leaders(self):
        best_so_far = None
        best_distance = 0

        for r in self.reindeer:
            if best_so_far is None or r.distance > best_distance:
                best_so_far = [r]
                best_distance = r.distance
            elif r.distance == best_distance:
                best_so_far.append(r)
            elif r.distance < best_distance:
                pass
            else:
                raise Exception('Illegal case')

        return best_so_far, best_distance

    @property
    def point_leaders(self):
        best_so_far = []
        best_points = 0

        for r, points in self.points.items():
            if best_so_far is None or points > best_points:
                best_so_far = [r]
                best_points = points
            elif points == best_points:
                best_so_far.append(r)
            elif points < best_points:
                pass
            else:
                raise Exception('Illegal case')

        return best_so_far, best_points

    @property
    def pretty_points(self):
        s = []
        for r in self.reindeer:
            s.append('{}: {} km, {} pt'.format(r.name, r.distance, self.points[r]))

        return ', '.join(s)

    def award_point_to_distance_leaders(self):
        reindeer, distance = self.distance_leaders
        for r in reindeer:
            self.points[r] += 1

    def conduct_race(self, duration):
        for tick in range(duration):
            for r in self.reindeer:
                r.travel_for(1)
            self.award_point_to_distance_leaders()
            print(tick + 1, self.pretty_points)

class Reindeer:
    REGEX = re.compile(r'^(?P<name>[A-Z][a-z]+) can fly (?P<kms>\d+) km/s for (?P<endurance>\d+) seconds, but then must rest for (?P<rest>\d+) seconds\.$')

    def __init__(self, reindeer_desc):
        regex = Re()
        if regex.match(Reindeer.REGEX, reindeer_desc):
            m = regex.last_match
            self.name, self.kms, self.endurance, self.rest = (
                m.group('name'),
                int(m.group('kms')),
                int(m.group('endurance')),
                int(m.group('rest')),
            )

            self.reset()
        else:
            raise Exception('Bad reindeer input: %s' % reindeer_desc)

    def reset(self):
        self.distance = 0
        self.resting_for = 0
        self.stamina = self.endurance

    def travel_for(self, seconds):
        time_remaining = seconds

        while time_remaining > 0:
            if self.resting_for > 0:
                if time_remaining < self.resting_for:
                    self.resting_for -= time_remaining
                    time_remaining = 0
                elif time_remaining >= self.resting_for:
                    time_remaining -= self.resting_for
                    self.resting_for = 0
                else:
                    raise Exception('Impossible case (bad resting math?)')

                if self.resting_for == 0:
                    self.stamina = self.endurance
            else:
                if time_remaining < self.stamina:
                    self.distance += self.kms * time_remaining
                    self.stamina -= time_remaining
                    time_remaining = 0
                elif time_remaining >= self.stamina:
                    self.distance += self.kms * self.stamina
                    time_remaining -= self.stamina
                    self.stamina = 0
                else:
                    raise Exception('Impossible case (bad stamina math?)')

                if self.stamina == 0:
                    self.resting_for = self.rest


if __name__ == '__main__':
    main()
