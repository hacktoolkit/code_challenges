# Python Standard Library Imports
import json
from dataclasses import dataclass
from typing import (
    Callable,
    Optional,
)

# Third Party (PyPI) Imports
import pyperclip


@dataclass
class InputConfig:
    as_integers: bool = False
    as_comma_separated_integers: bool = False
    as_json: bool = False
    as_groups: bool = False
    as_oneline: bool = False
    # for tables
    as_table: bool = False
    row_func: Optional[Callable] = None
    cell_func: Optional[Callable] = None


class BaseSolution:
    def __init__(self, input_file, input_config, expected_answers):
        self.input_file = input_file
        self.input_config = input_config
        self.expected_answers = expected_answers

        data = ingest(input_file, input_config)
        self.data = data

        self.process_data()

    def process_data(self):
        # data = self.data
        pass

    def solve(self):
        self.print_separator()
        print('# Solving Part 1...')
        self.answer1 = self.solve1()
        if self.answer1 is not None:
            print(self.answer1)
            pyperclip.copy(self.answer1)

        self.print_separator()
        print('# Solving Part 2...')
        self.answer2 = self.solve2()
        if self.answer2 is not None:
            print(self.answer2)
            pyperclip.copy(self.answer2)

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


def ingest(filename, input_config: InputConfig = None):
    if input_config is None:
        input_config = InputConfig()

    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    if input_config.as_integers:
        data = [int(line) for line in lines]
    elif input_config.as_comma_separated_integers:
        data = [int(x) for x in lines[0].split(',')]
    elif input_config.as_json:
        data = json.loads(''.join(lines))
    elif input_config.as_groups:
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
    elif input_config.as_oneline:
        data = ''.join(lines)
    elif input_config.as_table:
        row_func = input_config.row_func or (lambda _: _)
        cell_func = input_config.cell_func or (lambda _: _)

        data = [
            row_func([cell_func(value) for value in line.split()])
            for line
            in lines
        ]
    else:
        data = lines

    return data
