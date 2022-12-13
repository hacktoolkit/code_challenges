# Python Standard Library Imports
import datetime
import traceback
import typing as T
from dataclasses import dataclass
from pathlib import Path


TEST_MODE = True
DEBUGGING = False

EXPECTED_ANSWERS = (None, None)
TEST_CASES = {
    # '': (None, None),
    # 'b': (None, None),
    # 'c': (None, None),
}

##################################################
# Automatic inference of PROBLEM_NUM | DAY | YEAR
#
# Accomplishes this by inferring file paths of call-stack
#
# Inspiration:
# https://github.com/hacktoolkit/advent-of-code-data/blob/aa0688d7a09f6a5a1817d29a161df99ddc0b0122/aocd/get.py#L80-L177

most_recent_frame = traceback.extract_stack()[0]
solution_filename = most_recent_frame[0]
solution_filepath = Path(solution_filename)

if not solution_filename.endswith('.py'):
    # loaded from shell
    # filename could be: ('<stdin>', 'ipython')
    PROBLEM_NUM = None
    DAY = datetime.date.today().day
    YEAR = datetime.date.today().year
else:
    PROBLEM_NUM = solution_filepath.stem
    DAY = int(PROBLEM_NUM)
    YEAR = int(solution_filepath.parent.name)


# end Automatic inference of PROBLEM_NUM | DAY | YEAR
##################################################


@dataclass
class InputConfig:
    as_integers: bool = False
    as_comma_separated_integers: bool = False
    as_json: bool = False
    as_groups: bool = False
    strip_lines: bool = True
    as_oneline: bool = False
    # coordinates
    as_coordinates: bool = False
    coordinate_delimeter: T.Optional[str] = None
    # for tables
    as_table: bool = False
    row_func: T.Optional[T.Callable] = None
    cell_func: T.Optional[T.Callable] = None


INPUT_CONFIG = InputConfig()
SOLUTION = None
