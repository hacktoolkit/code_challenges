# Python Standard Library Imports
import math

from utils import ingest


INPUT_FILE = '1.in'
EXPECTED_ANSWERS = (3369286, 5051054, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)
        self.masses = [int(mass) for mass in self.data]

    def solve1(self):
        fuel_requirements = [
            self.basic_fuel_requirement(mass)
            for mass
            in self.masses
        ]
        answer = sum(fuel_requirements)
        return answer

    def solve2(self):
        fuel_requirements = [
            self.fuel_requirement(mass)
            for mass
            in self.masses
        ]
        answer = sum(fuel_requirements)
        return answer

    def basic_fuel_requirement(self, mass):
        fuel = int(math.floor(mass / 3.0)) - 2
        return max(fuel, 0)

    def fuel_requirement(self, mass):
        fuel = self.basic_fuel_requirement(mass)
        total_fuel = fuel

        while fuel > 0:
            fuel = self.basic_fuel_requirement(fuel)
            total_fuel += fuel

        return total_fuel


if __name__ == '__main__':
    main()
