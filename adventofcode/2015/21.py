# Python Standard Library Imports
import copy
import math
import re
from collections import defaultdict
from dataclasses import dataclass

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '21'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (None, None)
TEST_VARIANT = ''  # '', 'b', 'c', 'd', ...
TEST_EXPECTED_ANSWERS = {
    '': (None, None),
    'b': (None, None),
    'c': (None, None),
}

DEBUGGING = False
DEBUGGING = True


def debug(s):
    if DEBUGGING:
        print(s)
    else:
        pass


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=True,
        as_oneline=False,
        as_coordinates=False,
        coordinate_delimeter=None,
        as_table=False,
        row_func=None,
        cell_func=None,
    )

    if TEST_MODE:
        input_filename = f'{PROBLEM_NUM}{TEST_VARIANT}.test.in'
        expected_answers = TEST_EXPECTED_ANSWERS[TEST_VARIANT]
    else:
        input_filename = f'{PROBLEM_NUM}.in'
        expected_answers = EXPECTED_ANSWERS

    solution = Solution(input_filename, input_config, expected_answers)

    solution.solve()
    solution.report()


class Solution(BaseSolution):
    def process_data(self):
        data = self.data

        player_data = data[0]
        boss_data = data[1]
        shops_data = data[2:]

        rpg = RPG()
        rpg.load_player(player_data)
        rpg.load_boss(boss_data)
        rpg.load_shops(shops_data)

        self.rpg = rpg

    def solve1(self):
        rpg = self.rpg
        winner = rpg.combat()
        debug(f'The {winner.name} wins!')

        answer = None
        return answer

    def solve2(self):
        #
        # TODO: FILL THIS IN
        #
        answer = None
        return answer


class RPG:
    @dataclass
    class Character:
        name: str
        hit_points: int
        damage: int
        armor: int

        @classmethod
        def from_data(cls, name, data):
            kwargs = {
                'name': name,
            }
            for line in data:
                raw_stat, amount = line.split(':')
                stat = raw_stat.lower().replace(' ', '_')
                kwargs[stat] = int(amount)

            char = cls(**kwargs)

            return char

        def attack(self, other_char):
            damage_dealt = other_char.defend(self.damage)
            debug(
                f'The {self.name} deals {self.damage}-{other_char.armor} = {damage_dealt} damage; the {other_char.name} goes down to {other_char.hit_points} hit points.'
            )

        def defend(self, damage):
            damage_received = max(1, damage - self.armor)
            self.hit_points -= damage_received
            return damage_received

    @dataclass
    class Shop:
        name: str
        items: list['Item']

        @dataclass
        class Item:
            name: str
            cost: int
            damage: int
            armor: int

            @classmethod
            def from_data(cls, headings, data):
                values = data.split()
                kwargs = {
                    'name': values[0],
                }
                kwargs.update(dict(zip(headings[1:], map(int, values[1:]))))
                item = cls(**kwargs)
                return item

        @classmethod
        def from_data(cls, data):
            headings = [
                heading.lower().replace(':', '') for heading in data[0].split()
            ]
            name = headings[0]

            items = [
                cls.Item.from_data(headings, item_data)
                for item_data in data[1:]
            ]

            shop = cls(name=name, items=items)
            return shop

    def load_player(self, data):
        player = self.Character.from_data('player', data)
        self.player = player
        debug(player)

    def load_boss(self, data):
        boss = self.Character.from_data('boss', data)
        self.boss = boss
        debug(boss)

    def load_shops(self, data):
        for shop_data in data:
            shop = self.Shop.from_data(shop_data)
            setattr(self, f'{shop.name}_shop', shop)
            debug(shop)

    def combat(self):
        while self.player.hit_points > 0 and self.boss.hit_points > 0:
            self.player.attack(self.boss)
            if self.boss.hit_points > 0:
                self.boss.attack(self.player)

        winner = self.player if self.player.hit_points > 0 else self.boss
        return winner


if __name__ == '__main__':
    main()
