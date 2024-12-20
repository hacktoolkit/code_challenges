# Python Standard Library Imports
import re
from collections import defaultdict
from dataclasses import dataclass

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '19'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (518, 200)
TEST_VARIANT = 'b'
TEST_EXPECTED_ANSWERS = {
    '': (4, 3),
    'b': (7, 6),
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

        formulas = data[0]
        medicine_molecule = data[1][0]

        self.medicine_molecule = medicine_molecule
        self.lab = ReindeerOrganicChemistryLab(formulas)

    def solve1(self):
        lab = self.lab
        molecules = lab.generate_distinct_molecules(self.medicine_molecule)

        answer = len(molecules)
        return answer

    def solve2(self):
        lab = self.lab
        # steps = lab.fabricate_molecule_naive(self.medicine_molecule)
        steps = lab.fabricate_molecule_by_reduction(self.medicine_molecule)

        answer = steps
        return answer


class ReindeerOrganicChemistryLab:
    def __init__(self, formulas):
        self.formulas = formulas

        expansions = defaultdict(list)
        pairs = [formula.split(' => ') for formula in self.formulas]
        for atom, molecule in pairs:
            expansions[atom].append(molecule)

        self.expansions = expansions

        self.reductions = {
            molecule: atom
            for atom, molecules in self.expansions.items()
            for molecule in molecules
        }

    def generate_distinct_molecules(self, molecule):
        atoms = self.get_atoms(molecule)

        molecules = set()
        for i, atom in enumerate(atoms):
            prefix = ''.join(atoms[0:i])
            suffix = ''.join(atoms[i + 1 :])

            # replace one atom in each position
            for molecule in self.expansions[atom]:
                new_molecule = f'{prefix}{molecule}{suffix}'
                molecules.add(new_molecule)

        return molecules

    def get_atoms(self, molecule):
        atoms = []

        l = len(molecule)
        i = 0
        while i < l:
            a1 = molecule[i]
            a2 = molecule[i + 1] if (i + 1 < l) else ''

            if 'a' <= a2 <= 'z':
                a = f'{a1}{a2}'
                i += 1
            else:
                a = a1

            atoms.append(a)

            i += 1

        return atoms

    def fabricate_molecule_naive(self, medicine_molecule):
        """Returns the number of steps it takes to fabricate `medicine_molecule`
        starting from just a single electron `e`
        """
        avail_molecules = {'e'}
        steps = 0

        generated_medicine = False
        while not generated_medicine:
            all_new_molecules = set()
            for molecule in avail_molecules:
                new_molecules = self.generate_distinct_molecules(molecule)
                if medicine_molecule in new_molecules:
                    generated_medicine = True
                    break

                all_new_molecules |= new_molecules

            avail_molecules = all_new_molecules
            steps += 1

        return steps

    def fabricate_molecule_by_reduction(self, medicine_molecule):
        """Start with the medicine molecule and work backwards to reduce to 'e'

        Returns the number of steps
        """
        steps = 0
        molecule = medicine_molecule

        rn_ar_molecules = [
            molecule
            for molecule in self.reductions.keys()
            if molecule.endswith('Ar')
        ]

        regular_molecules = [
            molecule
            for molecule in self.reductions.keys()
            if not molecule.endswith('Ar')
        ]

        # by joining all patterns, `re.sub()` below will be greedy
        rn_ar_pattern = '|'.join(rn_ar_molecules)
        regular_pattern = '|'.join(regular_molecules)

        def repl(match):
            molecule = match.group()
            atom = self.reductions[molecule]
            return atom

        debug(f'Starting molecule: {molecule}')

        did_reduce = True
        while molecule != 'e' and did_reduce:

            # prioritize replacing Rn...Ar molecules first
            if rn_ar_pattern:
                molecule, num_subs = re.subn(
                    rn_ar_pattern, repl, molecule, count=1
                )
            else:
                num_subs = 0

            if num_subs == 0:
                # no Rn...Ar molecule to replace, perform regular sub
                molecule, num_subs = re.subn(
                    regular_pattern, repl, molecule, count=1
                )
            else:
                pass

            did_reduce = num_subs > 0
            if did_reduce:
                steps += 1
                debug(f'Reduced to: {molecule}')
            else:
                debug(f'No further reductions of {molecule}')

        return steps


if __name__ == '__main__':
    main()
