# Python Standard Library Imports
import json
from dataclasses import dataclass
from typing import (
    Callable,
    Optional,
)


@dataclass
class InputConfig:
    as_integers: bool = False
    as_comma_separated_integers: bool = False
    as_json: bool = False
    as_groups: bool = False
    as_oneline: bool = False
    # for tables
    as_table: bool = False
    cell_func: Optional[Callable] = None


class BaseSolution:
    def __init__(self, input_file, input_config, expected_answers):
        self.input_file = input_file
        self.input_config = input_config
        self.expected_answers = expected_answers

        data = ingest(
            input_file,
            as_integers=input_config.as_integers,
            as_comma_separated_integers=input_config.as_comma_separated_integers,
            as_json=input_config.as_json,
            as_groups=input_config.as_groups,
            as_oneline=input_config.as_oneline,
            as_table=input_config.as_table,
            cell_func=input_config.cell_func
        )
        self.data = data

        self.process_data()

    def process_data(self):
        # data = self.data
        pass

    def solve(self):
        self.print_separator()
        print('# Solving Part 1...')
        self.answer1 = self.solve1()
        print(self.answer1)

        self.print_separator()
        print('# Solving Part 2...')
        self.answer2 = self.solve2()
        print(self.answer2)

    def report(self):
        answers = (self.answer1, self.answer2, )

        self.print_separator()
        print('# Summary')
        print(f'Calculated: {answers}')
        print(f'Expected  : {self.expected_answers}')
        self.print_separator()

        assert(answers == self.expected_answers), "Sad panda"

    def print_separator(self, separator_length=40):
        print('-' * separator_length)

    def solve1(self):
        #
        # TODO: FILL THIS IN
        #
        answer = None
        return answer

    def solve2(self):
        #
        # TODO: FILL THIS IN
        #
        answer = None
        return answer


def ingest(
    filename,
    as_integers=False,
    as_comma_separated_integers=False,
    as_json=False,
    as_groups=False,
    as_oneline=False,
    # for tables
    as_table=False,
    cell_func=None
):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    if as_integers:
        data = [int(line) for line in lines]
    elif as_comma_separated_integers:
        data = [int(x) for x in lines[0].split(',')]
    elif as_json:
        data = json.loads(''.join(lines))
    elif as_groups:
        data = []

        group = None
        for line in lines:
            if group is None:
                group = []
            if line:
                group.append(line)
            else:
                data.append(group)
                group = None

        if group:
            data.append(group)
    elif as_oneline:
        data = ''.join(lines)
    elif as_table:
        data = []

        for line in lines:
            cells = list(filter(lambda x: x is not None, line.split()))

            if cell_func:
                cells = [cell_func(value) for value in cells]

            data.append(cells)
    else:
        data = lines

    return data
