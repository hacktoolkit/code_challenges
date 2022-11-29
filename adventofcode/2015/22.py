# Python Standard Library Imports
import copy
import math
import re
import typing as T
from collections import defaultdict
from dataclasses import (
    asdict,
    dataclass,
    field,
)
from itertools import (
    combinations_with_replacement,
    permutations,
)

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '22'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (None, None)
TEST_VARIANT = 'b'  # '', 'b', 'c', 'd', ...
TEST_EXPECTED_ANSWERS = {
    '': (226, None),
    'b': (641, None),
    'c': (None, None),
}

DEBUGGING = False
# DEBUGGING = True


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
        spells_data = data[2]

        rpg = RPG()
        rpg.load_player(player_data)
        rpg.load_boss(boss_data)
        rpg.load_spells(spells_data)

        self.rpg = rpg

    def solve1(self):
        (
            most_economical_sequence,
            mana_cost,
        ) = RPGSolverBFS.find_most_economical_spell_sequence(self.rpg)

        if most_economical_sequence:
            debug(most_economical_sequence)
            global DEBUGGING
            DEBUGGING = True
            self.rpg.reset()
            self.rpg.combat(
                most_economical_sequence,
                mana_limit=None,
                use_restore=False,
            )
            DEBUGGING = False
            print(', '.join([spell.name for spell in most_economical_sequence]))
        else:
            pass

        answer = mana_cost
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
        mana: int
        damage: int
        armor: int
        total_damage_received: int = 0
        total_mana_recharged: int = 0
        spells_cast: list['RPG.Spells.Spell'] = field(
            default_factory=lambda: []
        )
        spell_affects: list['RPG.Spells.Spell'] = field(
            default_factory=lambda: []
        )

        @classmethod
        def from_data(cls, name, data):
            kwargs = {
                'name': name,
            }
            for line in data:
                try:
                    raw_stat, raw_amount = line.split(':')
                except Exception as e:
                    print(line)
                    raise (e)

                stat = raw_stat.lower().replace(' ', '_')
                amount = int(raw_amount)

                kwargs[stat] = amount

            char = cls(**kwargs)

            return char

        @property
        def effective_hit_points(self):
            hit_points = self.hit_points - self.total_damage_received
            return hit_points

        @property
        def effective_mana(self):
            mana = self.mana - self.total_mana_spent + self.total_mana_recharged
            return mana

        @property
        def total_mana_spent(self):
            mana_spent = sum([spell.cost for spell in self.spells_cast])
            return mana_spent

        @property
        def spells_cast_names(self):
            spell_names = tuple([spell.name for spell in self.spells_cast])
            return spell_names

        @property
        def effective_damage(self):
            effective_damage = self.damage
            return effective_damage

        @property
        def effective_armor(self):
            spell_armor_contributions = [
                spell.armor for spell in self.spell_affects if spell.armor != 0
            ]
            effective_armor = self.armor + sum(spell_armor_contributions)
            return effective_armor

        def __copy__(self):
            kwargs = asdict(self)
            kwargs['spells_cast'] = copy.copy(self.spells_cast)
            kwargs['spell_affects'] = copy.copy(self.spell_affects)
            char_copy = self.__class__(**kwargs)

            return char_copy

        def __deepcopy__(self, memo):
            kwargs = asdict(self)
            kwargs['spells_cast'] = copy.deepcopy(self.spells_cast)
            kwargs['spell_affects'] = copy.deepcopy(self.spell_affects)
            char_copy = self.__class__(**kwargs)

            memo[id(self)] = char_copy
            return char_copy

        def reset(self):
            """Resets mana and damage received

            Called in preparation to test another combat scenario
            """
            self.total_damage_received = 0
            self.total_mana_recharged = 0
            self.spells_cast = []
            self.spell_affects = []

        def attack(self, other_char):
            damage_dealt = other_char.defend(self.effective_damage)
            debug(
                f'{self.name} attacks for {self.effective_damage}-{other_char.effective_armor} = {damage_dealt} damage! {other_char.name} goes down to {other_char.effective_hit_points} hit points.'
            )

        def cast_spell(self, spell, other_char):
            """Attempts to cast a spell

            Rules

            - On each of your turns, you must select one of your spells to cast.
            - If you cannot afford to cast any spell, you lose.
            - You cannot cast a spell that would start an effect which is already active
            - Effects can be started on the same turn they end
            """

            if self.effective_mana < spell.cost:
                debug(
                    f'{self.name} has insufficient mana to cast {spell.name}.'
                )
                successful_cast = False
            elif spell.has_defensive_effect and self.has_active_affect(spell):
                debug(f'{self.name} is already affected by {spell.name}.')
                successful_cast = False
            elif spell.has_offensive_effect and other_char.has_active_affect(
                spell
            ):
                debug(f'{other_char.name} is already affected by {spell.name}.')
                successful_cast = False
            else:
                self.spells_cast.append(spell)
                msg = f'{self.name} casts {spell.name}'

                if spell.damage:
                    damage_received = other_char.defend(spell.damage)
                    msg += f', dealing {damage_received} damage'

                if spell.healing:
                    self.total_damage_received -= spell.healing
                    msg += f', and healing {spell.healing} hit points'

                msg += '.'

                if spell.has_defensive_effect:
                    self.apply_spell_effect(spell)
                elif spell.has_offensive_effect:
                    other_char.apply_spell_effect(spell)
                else:
                    # no spell effects, do nothing
                    pass

                if spell.damage:
                    msg += f' {other_char.name} goes down to {other_char.effective_hit_points}.'

                debug(msg)
                successful_cast = True

            return successful_cast

        def apply_spell_effect(self, spell):
            spell_copy = copy.copy(spell)
            self.spell_affects.append(spell_copy)

        def has_active_affect(self, spell):
            has_affect = False
            for spell_affect in self.spell_affects:
                if spell_affect.name == spell.name and spell_affect.turns > 0:
                    has_affect = True

            return has_affect

        def perform_turn_effects(self):
            for spell in self.spell_affects:
                if spell.turns > 0:
                    spell.turns -= 1

                    if spell.armor > 0:
                        debug(f"{spell.name}'s timer is now {spell.turns}.")
                    if spell.recharge > 0:
                        self.total_mana_recharged += spell.recharge
                        debug(
                            f'{spell.name} provides {spell.recharge} mana; its timer is now {spell.turns}.'
                        )
                    if spell.dot > 0:
                        self.total_damage_received += spell.dot
                        debug(
                            f'{spell.name} deals {spell.dot} damage to {self.name}; its timer is now {spell.turns}. {self.name} is down to {self.effective_hit_points}.'
                        )
                else:
                    # expired spell, do nothing
                    pass

            # optimization/cleanup
            self.spell_affects = [
                spell for spell in self.spell_affects if spell.turns > 0
            ]

        def defend(self, damage):
            damage_received = max(1, damage - self.effective_armor)
            self.total_damage_received += damage_received
            return damage_received

    @dataclass
    class Spells:
        name: str
        catalog: list['RPG.Spells.Spell']

        @dataclass
        class Spell:
            name: str
            cost: int
            damage: int
            healing: int
            recharge: int
            armor: int
            dot: int
            turns: int

            @classmethod
            def from_data(cls, headings, data):
                values = data.split()
                kwargs = {
                    'name': values[0],
                }
                kwargs.update(dict(zip(headings[1:], map(int, values[1:]))))
                item = cls(**kwargs)
                return item

            def __copy__(self):
                kwargs = asdict(self)
                spell_copy = self.__class__(**kwargs)
                return spell_copy

            def __deepcopy__(self, memo):
                # a copy is already a deep copy, since all attributes are primitives
                return self.__copy__()

            @property
            def has_defensive_effect(self):
                has_defensive_effect = self.turns > 0 and self.dot == 0
                return has_defensive_effect

            @property
            def has_offensive_effect(self):
                has_offensive_effect = self.turns > 0 and self.dot > 0
                return has_offensive_effect

        @classmethod
        def from_data(cls, data):
            headings = [
                heading.lower().replace(':', '') for heading in data[0].split()
            ]
            name = headings[0]

            catalog = [
                cls.Spell.from_data(headings, spell_data)
                for spell_data in data[1:]
            ]

            spells = cls(name=name, catalog=catalog)
            return spells

    def load_player(self, data):
        player = self.Character.from_data('Player', data)
        self.player = player
        debug(player)

    def load_boss(self, data):
        boss = self.Character.from_data('Boss', data)
        self.boss = boss
        debug(boss)

    def load_spells(self, data):
        spells = self.Spells.from_data(data)
        # if we wanted to split up the spell cataog into different categores, we could do:
        # setattr(self, f'{spells.name}_spells', spells)
        self.spells = spells
        debug(spells)

    def combat(self, spell_sequence, mana_limit=None, use_restore=True):
        self.turn = 0

        if use_restore:
            self.restore_progress(spell_sequence[:-1])

        def _apply_turn_effects(whose_turn):
            prefix = '\n' if self.turn > 0 else ''
            debug(f'{prefix}-- Turn {self.turn + 1}: {whose_turn.name} --')
            debug(
                f'{self.player.name} has {self.player.effective_hit_points} hit points, {self.player.effective_armor} armor, {self.player.effective_mana} mana'
            )
            debug(
                f'{self.boss.name} has {self.boss.effective_hit_points} hit points'
            )
            self.player.perform_turn_effects()
            self.boss.perform_turn_effects()

        while (
            self.player.effective_hit_points > 0
            and self.boss.effective_hit_points > 0
            and (
                mana_limit is None or self.player.total_mana_spent < mana_limit
            )
        ):
            # player's turn
            spell_index = len(self.player.spells_cast)
            if spell_index < len(spell_sequence):
                spell = spell_sequence[spell_index]
            else:
                debug('Spell sequence exhausted.')
                break

            _apply_turn_effects(self.player)

            if spell is None:  # TODO: delete this case
                # Player performs no-op on turn (to simulate out-of-mana situation and waiting on effects to win)
                successful_cast = True
            else:
                successful_cast = self.player.cast_spell(spell, self.boss)

            if not successful_cast:
                # no spell cast due to either OOM or spell effect already applied
                break
            else:
                pass

            self.turn += 1

            if self.boss.effective_hit_points > 0:
                # boss's turn
                _apply_turn_effects(self.boss)

                if self.boss.effective_hit_points > 0:
                    self.boss.attack(self.player)
                    self.turn += 1
                else:
                    # boss died to DOT effect before attacking
                    pass
            else:
                pass

        winner = (
            self.player
            if self.boss.effective_hit_points <= 0
            else self.boss
            if self.player.effective_hit_points <= 0
            else None
        )

        if winner:
            debug(f'{winner.name} wins!')
            # debug(f'Player spent {self.player.total_mana_spent} mana.')

        elif mana_limit and self.player.total_mana_spent > mana_limit:
            debug('Mana cost exceeds best so far, pruning')
            winner = self.boss
        elif len(spell_sequence) == len(self.player.spells_cast):
            debug('Exhausted sequence, no winner determined yet')
            self.store_progress()
        elif not successful_cast:
            # OOM or spell target already has spell affect
            # set boss as winner to prune this branch
            winner = self.boss

            if (
                spell_sequence[len(self.player.spells_cast)].cost
                > self.player.effective_mana
            ):
                debug('Insufficient mana')
            else:
                # already has effect
                pass
        else:
            raise Exception(
                f'Impossible case: {turn} turns, spells: {spell_sequence}'
            )

        return winner

    def reset(self):
        """Resets player and boss state to do another battle/combat sequence

        Resets:
        - Damage received
        - Equipped items
        """
        self.turn = 0
        self.player.reset()
        self.boss.reset()

    def store_progress(self):
        if not hasattr(self, 'saved_progress'):
            self.saved_progress = {}

        self.saved_progress[self.player.spells_cast_names] = (
            self.turn,
            copy.deepcopy(self.player),
            copy.deepcopy(self.boss),
        )

    def restore_progress(self, spell_sequence):
        if not hasattr(self, 'saved_progress'):
            self.saved_progress = {}

        key = tuple([spell.name for spell in spell_sequence])
        if key in self.saved_progress:
            self.turn, self.player, self.boss = self.saved_progress[key]
            debug(
                f'Restored progress:\n- Completed Turns: {self.turn}\n- Player: {self.player}\n- Boss: {self.boss}'
            )
        else:
            # do nothing
            pass


class RPGSolverBFS:
    @classmethod
    def yield_spell_sequence_combos(cls, rpg):
        # TODO: determine if a no-op spell is needed or not?
        # spell_choices = [None] + rpg.spells.catalog
        spell_choices = rpg.spells.catalog

        # max_sequence_length = (
        #     rpg.boss.hit_points // rpg.spells.catalog[0].damage
        # ) + 1
        max_sequence_length = (
            rpg.boss.hit_points // rpg.spells.catalog[0].damage
        ) * 5
        max_sequence_length = 10

        for sequence_length in range(1, max_sequence_length + 1):
            # BFS traversal
            # iteratively increase spell sequence length until a winner is found
            print(f'BFS traversal depth: {sequence_length}')
            for spell_combos in combinations_with_replacement(
                spell_choices, sequence_length
            ):
                for sequence in permutations(spell_combos):
                    yield sequence

    @classmethod
    def terminating_sequence_visited(cls, spell_sequence):
        matches = False

        for terminating_sequence in cls.MEMO.keys():
            matches = True
            for i, spell_name in enumerate(terminating_sequence):
                if spell_sequence[i].name != spell_name:
                    matches = False
                    break

            if matches:
                break

        return matches

    @classmethod
    def find_most_economical_spell_sequence(cls, rpg):
        most_economical_sequence = None
        most_economical_sequence_mana_cost = None

        cls.MEMO = {}

        for spell_sequence in cls.yield_spell_sequence_combos(rpg):
            if cls.terminating_sequence_visited(spell_sequence):
                # already done same sequence, skip
                continue
            elif most_economical_sequence is not None and (
                sum([spell.cost for spell in spell_sequence])
                > most_economical_sequence_mana_cost
            ):
                # already found a winner, won't find any winners by going with more expensive sequences
                break
            else:
                winner = rpg.combat(
                    spell_sequence,
                    mana_limit=most_economical_sequence_mana_cost,
                )
                spells_cast = rpg.player.spells_cast
                spell_names = rpg.player.spells_cast_names
                spent_mana = rpg.player.total_mana_spent

                if winner is not None:
                    cls.MEMO[spell_names] = (winner, spent_mana)

                if winner == rpg.player:
                    if (
                        most_economical_sequence is None
                        or spent_mana < most_economical_sequence_mana_cost
                    ):
                        print(
                            f'Found a candidate: {most_economical_sequence} ({most_economical_sequence_mana_cost} mana).'
                        )
                        most_economical_sequence = spells_cast
                        most_economical_sequence_mana_cost = spent_mana
                    else:
                        # cannot be the solution, already found a cheaper spell sequence
                        pass
                else:
                    # not a winner, not a winning spell_sequence
                    pass

                # reset RPG state before next iteration
                rpg.reset()
                debug('=' * 10)

        return most_economical_sequence, most_economical_sequence_mana_cost


if __name__ == '__main__':
    main()
