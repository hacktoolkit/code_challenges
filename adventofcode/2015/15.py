# Python Standard Library Imports
import re
from itertools import combinations_with_replacement

from utils import (
    Re,
    ingest,
)


INPUT_FILE = '15.in'
EXPECTED_ANSWERS = (222870, 117936,  )

# INPUT_FILE = '15.test.in'
# EXPECTED_ANSWERS = (62842880, 57600000, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        data = ingest(INPUT_FILE)
        self.ingredients = [Ingredient(x) for x in data]

    def solve1(self):
        bakery = Bakery(self.ingredients)

        recipe, score = bakery.bake_off()

        answer = score

        self.answer1 = answer
        return answer

    def solve2(self):
        bakery = Bakery(self.ingredients)

        recipe, score = bakery.bake_off(calorie_target=500)

        answer = score

        self.answer2 = answer
        return answer


class Bakery:
    def __init__(self, ingredients):
        self.ingredients = ingredients

    def bake_off(self, calorie_target=None):
        # generate every cookie combo, find the score of the best one
        best_recipe = None
        best_score = 0

        for recipe in combinations_with_replacement(self.ingredients, 100):
            capacity = 0
            durability = 0
            flavor = 0
            texture = 0
            calories = 0

            for ingredient in recipe:
                capacity += ingredient.capacity
                durability += ingredient.durability
                flavor += ingredient.flavor
                texture += ingredient.texture
                calories += ingredient.calories

            capacity = max(0, capacity)
            durability = max(0, durability)
            flavor = max(0, flavor)
            texture = max(0, texture)

            score = capacity * durability * flavor * texture

            if calorie_target is None or calories == calorie_target:
                if best_recipe is None or score > best_score:
                    best_recipe = recipe
                    best_score = score

        return best_recipe, best_score


class Ingredient:
    REGEX = re.compile(r'^(?P<name>[A-Z][a-z]+): capacity (?P<capacity>-?\d+), durability (?P<durability>-?\d+), flavor (?P<flavor>-?\d+), texture (?P<texture>-?\d+), calories (?P<calories>-?\d+)$')

    def __init__(self, ingredient_data):
        regex = Re()
        if regex.match(Ingredient.REGEX, ingredient_data):
            m = regex.last_match
            self.name = m.group('name')
            self.capacity = int(m.group('capacity'))
            self.durability = int(m.group('durability'))
            self.flavor = int(m.group('flavor'))
            self.texture = int(m.group('texture'))
            self.calories = int(m.group('calories'))
        else:
            raise Exception('Bad ingredient data: %s' % ingredient_data)


if __name__ == '__main__':
    main()
