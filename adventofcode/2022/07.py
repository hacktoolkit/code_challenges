# Python Standard Library Imports
import re
import typing as T
from collections import defaultdict
from pathlib import Path

# Third Party (PyPI) Imports
import click

from utils import (
    BaseSolution,
    InputConfig,
    Re,
)


EXPECTED_ANSWERS = (1367870, 549173)
TEST_CASES = {
    '': (95437, 24933642),
}


YEAR = int(Path.cwd().parts[-1])
DAY = int(Path(__file__).stem)
PROBLEM_NUM = str(DAY).zfill(2)

TEST_MODE = True
DEBUGGING = False


def debug(*args):
    if DEBUGGING:
        print(*args)
    else:
        pass


@click.command()
@click.option('--is_real', '--real', is_flag=True, default=False)
@click.option('--submit', is_flag=True, default=False)
@click.option('--is_debug', '--debug', is_flag=True, default=False)
def main(is_real, submit, is_debug):
    global TEST_MODE
    global DEBUGGING
    TEST_MODE = not is_real
    DEBUGGING = is_debug

    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        strip_lines=True,
        as_oneline=False,
        as_coordinates=False,
        coordinate_delimeter=None,
        as_table=False,
        row_func=None,
        cell_func=None,
    )

    inputs = []

    if TEST_MODE:
        for test_variant, expected_answers in TEST_CASES.items():

            input_filename = f'{PROBLEM_NUM}{test_variant}.test.in'
            inputs.append((input_filename, expected_answers))
    else:
        input_filename = f'{PROBLEM_NUM}.in'
        expected_answers = EXPECTED_ANSWERS
        inputs.append((input_filename, expected_answers))

    for input_filename, expected_answers in inputs:
        print(f'Running with input file: {input_filename}')

        solution = Solution(
            input_filename,
            input_config,
            expected_answers,
            year=YEAR,
            day=DAY,
        )

        solution.solve()
        if submit:
            solution.submit(is_test=TEST_MODE)
        solution.report()


class Solution(BaseSolution):
    def process_data(self):
        data = self.data

        term = Terminal(self.data)
        term.process()

        self.term = term

    def solve1(self) -> int:
        term = self.term

        dirs = term.dirs_under_size()

        answer = sum([_[1] for _ in dirs])
        return answer

    def solve2(self) -> int:
        term = self.term

        answer = term.smallest_dir_to_free()
        return answer


class Terminal:
    COMMAND_REGEX = re.compile(r'^\$ (?P<command>(cd|ls)) ?(?P<arg>.*)$')
    DIR_REGEX = re.compile(r'^dir (?P<dirname>.*)$')
    FILE_REGEX = re.compile(r'^(?P<filesize>\d+) (?P<filename>.*)$')

    def __init__(self, output):
        self.output = output

        self.cwd = None
        self.dir_files = defaultdict(lambda: [])
        self.subdirs = defaultdict(lambda: [])
        self.dir_sizes = defaultdict(int)

    def process(self):
        regex = Re()

        for line in self.output:
            if regex.match(self.COMMAND_REGEX, line):
                m = regex.last_match
                command, arg = m.group('command'), m.group('arg')
                if command == 'cd':
                    if arg == '/':
                        self.cwd = Path('/')
                    elif arg == '..':
                        self.cwd = self.cwd.parent
                    else:
                        self.cwd /= arg
                elif command == 'ls':
                    # do nothing
                    pass
            elif regex.match(self.DIR_REGEX, line):
                m = regex.last_match
                dirname = m.group('dirname')
                self.subdirs[self.cwd].append(dirname)
            elif regex.match(self.FILE_REGEX, line):
                m = regex.last_match
                filesize = int(m.group('filesize'))
                filename = m.group('filename')
                file_path = self.cwd / filename

                self.dir_files[self.cwd].append((filename, filesize))
                self.update_sizes(file_path, filesize)

    def update_sizes(self, file_path, filesize):
        debug(f'update_sizes({file_path}, {filesize})')

        for d in file_path.parents:
            self.dir_sizes[d] += filesize

        debug(self.dir_sizes)

    def dirs_under_size(self, limit=100000):
        dirs = []
        for dirname, total_size in self.dir_sizes.items():
            if total_size <= limit:
                dirs.append((dirname, total_size))

        debug(dirs)

        return dirs

    def smallest_dir_to_free(self, total_size=70000000, target_free=30000000):
        used_size = self.dir_sizes[Path('/')]
        avail_size = total_size - used_size

        to_free = max(0, target_free - avail_size)
        debug(f'to free: {to_free}')

        eligible_dirs = filter(
            lambda size: size >= to_free, self.dir_sizes.values()
        )
        size = min(eligible_dirs)
        return size


if __name__ == '__main__':
    main()
