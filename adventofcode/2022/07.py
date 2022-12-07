# Python Standard Library Imports
import re
import typing as T
from collections import defaultdict
from pathlib import Path

# Third Party (PyPI) Imports
import click

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (1367870, 549173)
config.TEST_CASES = {
    '': (95437, 24933642),
}

config.INPUT_CONFIG.as_integers = False
config.INPUT_CONFIG.as_comma_separated_integers = False
config.INPUT_CONFIG.as_json = False
config.INPUT_CONFIG.as_groups = False
config.INPUT_CONFIG.strip_lines = True
config.INPUT_CONFIG.as_oneline = False
config.INPUT_CONFIG.as_coordinates = False
config.INPUT_CONFIG.coordinate_delimeter = None
config.INPUT_CONFIG.as_table = False
config.INPUT_CONFIG.row_func = None
config.INPUT_CONFIG.cell_func = None

config.YEAR = int(Path.cwd().parts[-1])
config.DAY = int(Path(__file__).stem)
config.PROBLEM_NUM = str(config.DAY).zfill(2)


@solution
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
        for line in self.output:
            if RE.match(self.COMMAND_REGEX, line):
                command, arg = RE.m.group('command'), RE.m.group('arg')
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
            elif RE.match(self.DIR_REGEX, line):
                dirname = RE.m.group('dirname')
                self.subdirs[self.cwd].append(dirname)
            elif RE.match(self.FILE_REGEX, line):
                filesize = int(RE.m.group('filesize'))
                filename = RE.m.group('filename')
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
