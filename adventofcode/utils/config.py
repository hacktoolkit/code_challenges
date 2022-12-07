# Python Standard Library Imports
import typing as T
from dataclasses import dataclass


TEST_MODE = True
DEBUGGING = False


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
