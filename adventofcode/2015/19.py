# Python Standard Library Imports
from collections import defaultdict
from dataclasses import dataclass

from utils import (
    BaseSolution,
    InputConfig,
)


PROBLEM_NUM = '19'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (518, None)
TEST_EXPECTED_ANSWERS = (4, 3)


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
        input_filename = f'{PROBLEM_NUM}.test.in'
        expected_answers = TEST_EXPECTED_ANSWERS
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
        medicine_molecule = self.medicine_molecule
        lab = self.lab

        molecules = lab.generate_distinct_molecules(medicine_molecule)
        answer = len(molecules)
        return answer

    def solve2(self):
        medicine_molecule = self.medicine_molecule
        lab = self.lab

        avail_molecules = {'e'}
        steps = 0

        generated_medicine = False
        while not generated_medicine:
            all_new_molecules = set()
            for molecule in avail_molecules:
                new_molecules = lab.generate_distinct_molecules(molecule)
                if medicine_molecule in new_molecules:
                    generated_medicine = True
                    break

                all_new_molecules |= new_molecules

            avail_molecules = all_new_molecules
            steps += 1

        answer = steps
        return answer


class ReindeerOrganicChemistryLab:
    def __init__(self, formulas):
        self.formulas = formulas

        replacements = defaultdict(list)
        pairs = [formula.split(' => ') for formula in self.formulas]
        for molecule, replacement in pairs:
            replacements[molecule].append(replacement)

        self.replacements = replacements

    def generate_distinct_molecules(self, molecule):
        atoms = self.get_atoms(molecule)

        molecules = set()
        for i, a in enumerate(atoms):
            # replace one atom in each position
            a_replacements = self.replacements[a]

            prefix = ''.join(atoms[0:i])
            suffix = ''.join(atoms[i + 1 :])

            for replacement in a_replacements:
                new_molecule = f'{prefix}{replacement}{suffix}'
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


if __name__ == '__main__':
    main()
