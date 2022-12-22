# Python Standard Library Imports
import re
from enum import Enum
from functools import cache
from itertools import zip_longest

from utils import (
    RE,
    BaseSolution,
    InputConfig,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (27492, 78291)
config.TEST_CASES = {
    '': (6032, 5031),
}

config.INPUT_CONFIG.as_groups = True
config.INPUT_CONFIG.strip_lines = False


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data

    def solve1(self):
        board = Board(self.data[0], self.data[1][0].strip())
        debug(board.pretty_print())
        board.walk()
        debug(board.pretty_print())
        answer = board.password
        return answer

    def solve2(self):
        board = Board(self.data[0], self.data[1][0].strip())
        debug(board.pretty_print())
        board.walk(part=2)
        debug(board.pretty_print())
        answer = board.password
        return answer


class Direction(Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    @property
    def dxdy(self):
        DXDY_MAP = {
            0: (0, 1),
            1: (1, 0),
            2: (0, -1),
            3: (-1, 0),
        }
        return DXDY_MAP[self.value]

    @property
    def symbol(self):
        SYMBOL_MAP = {
            0: '>',
            1: 'v',
            2: '<',
            3: '^',
        }
        return SYMBOL_MAP[self.value]

    @property
    def opposite_direction(self):
        DIR_MAP = {
            0: Direction.LEFT,
            1: Direction.UP,
            2: Direction.RIGHT,
            3: Direction.DOWN,
        }
        return DIR_MAP[self.value]

    def turn(self, turn):
        if turn == 'L':
            direction = self.turn_left()
        elif turn == 'R':
            direction = self.turn_right()
        else:
            raise Exception(f'Illegal turn: {turn}')
        return direction

    def turn_left(self):
        return Direction((self.value - 1) % (Direction.UP.value + 1))

    def turn_right(self):
        return Direction((self.value + 1) % (Direction.UP.value + 1))


class Board:
    def __init__(self, raw_board, raw_dirs):
        self.facing = Direction.RIGHT
        self.grid = {}

        self.M = len(raw_board)
        self.N = len(raw_board[0].rstrip('\n'))

        for i, row in enumerate(raw_board, 1):
            for j, cell in enumerate(row.rstrip('\n'), 1):
                self.N = max(self.N, j)
                if cell in ('.', '#'):
                    self.grid[(i, j)] = cell

        self.row = 1
        self.col = next(
            (
                j
                for j in range(1, self.N + 1)
                if self.grid.get((self.row, j)) is not None
            )
        )

        steps = list(map(int, re.findall(r'\d+', raw_dirs)))
        turns = re.findall(r'[LR]', raw_dirs)
        self.path = list(zip_longest(steps, turns))

    @property
    def password(self):
        password = 1000 * self.row + 4 * self.col + self.facing.value
        return password

    def walk(self, part=1):
        """Travels along `self.path`

        Side effect: marks the path
        """
        for (step, turn) in self.path:
            debug(f'{(self.row, self.col)} {self.facing.name} {step}')
            for n in range(step):
                dx, dy = self.facing.dxdy
                did_move = self.move(dx, dy, part)
                if not did_move:
                    debug(f'Ran into a wall at {(self.row, self.col)}')
                    break

            # debug(self.pretty_print())

            if turn is not None:
                debug(turn)
                self.facing = self.facing.turn(turn)

        self.grid[(self.row, self.col)] = self.facing.symbol

    def move(self, dx, dy, part):
        i, j = self.row + dx, self.col + dy
        cell = self.grid.get((i, j))
        if cell is None:
            i, j, direction = self.wrap(dx, dy, part)
            cell = self.grid.get((i, j))
        else:
            direction = None

        if cell in ('.', '>', 'v', '<', '^'):
            # move to next cell
            self.row, self.col = i, j
            if direction is not None:
                # changed directions due to wrapping
                self.facing = direction
            did_move = True
        elif cell == '#':
            did_move = False
        else:
            raise Exception(f'Landed on an illegal cell {(i, j)}: {cell}')

        # leave a mark
        self.grid[(self.row, self.col)] = self.facing.symbol

        return did_move

    def wrap(self, dx, dy, part):
        debug(f'Wrapping {(self.row, self.col)}: {self.facing}')

        if part == 1:
            # wrap around: go in the reverse direction until we fall off the grid
            d2x, d2y = self.facing.opposite_direction.dxdy
            i, j = self.row + d2x, self.col + d2y
            while self.grid.get((i, j)) is not None:
                i, j = i + d2x, j + d2y
            # backtrack one more in the forward direction
            i, j = i + dx, j + dy
            direction = self.facing
        elif part == 2:
            CUBE = TestCube if config.TEST_MODE else Cube
            i, j, direction = CUBE.WRAP_MAP()[(self.row, self.col, self.facing)]
        else:
            raise Exception(f'Illegal part: {part}')

        debug(f'Wrapped to {(i, j)}: {direction}')
        return i, j, direction

    def pretty_print(self):
        buf = []

        # column headings
        buf.append(' ')
        for j in range(1, self.N + 1):
            buf.append(str(j % 10))
        buf.append('\n')

        # rows with row headings
        for i in range(1, self.M + 1):
            buf.append(f'{str(i % 10)}')
            for j in range(1, self.N + 1 + 1):
                buf.append(self.grid.get((i, j), ' '))
            buf.append('\n')

        s = ''.join(buf)
        return s


class Cube:
    """Provides wrapping configuation

     12
     3
    45
    6
    """

    @classmethod
    def update_map(cls, MAP, egress, egress_dir, ingress, ingress_dir):
        MAP[(*egress, egress_dir)] = (*ingress, ingress_dir)
        MAP[(*ingress, ingress_dir.opposite_direction)] = (
            *egress,
            egress_dir.opposite_direction,
        )

    @classmethod
    @cache
    def WRAP_MAP(cls, size=50):
        M = {}
        #  6
        # 412
        #  3
        #
        # LEFT 1 -> RIGHT 4; LEFT 4 -> RIGHT 1
        for k, i in enumerate(range(1, size + 1)):
            egress = (i, size + 1)
            ingress = (3 * size - k, 1)
            cls.update_map(M, egress, Direction.LEFT, ingress, Direction.RIGHT)
        # UP 1 -> RIGHT 6; LEFT 6 -> DOWN 1
        for k, j in enumerate(range(size + 1, size + 1 + size)):
            egress = (1, j)
            ingress = (3 * size + 1 + k, 1)
            cls.update_map(M, egress, Direction.UP, ingress, Direction.RIGHT)
        #
        #  6
        # 125
        #  3
        #
        # RIGHT 2 -> LEFT 5; RIGHT 5 -> LEFT 2
        for k, i in enumerate(range(1, 1 + size)):
            egress = (i, 3 * size)
            ingress = (3 * size - k, 2 * size)
            cls.update_map(M, egress, Direction.RIGHT, ingress, Direction.LEFT)
        # DOWN 2 -> LEFT 3; RIGHT 3 -> UP 2
        for k, j in enumerate(range(2 * size + 1, 2 * size + 1 + size)):
            egress = (size, j)
            ingress = (size + 1 + k, 2 * size)
            cls.update_map(M, egress, Direction.DOWN, ingress, Direction.LEFT)
        # UP 2 -> UP 6; DOWN 6 -> DOWN 2
        for k, j in enumerate(range(2 * size + 1, 2 * size + 1 + size)):
            egress = (1, j)
            ingress = (4 * size, 1 + k)
            cls.update_map(M, egress, Direction.UP, ingress, Direction.UP)
        #
        #  1
        # 432
        #  5
        #
        # RIGHT 3 -> UP 2; DOWN 2 -> LEFT 3 (covered)
        # LEFT 3 -> DOWN 4; UP 4 -> RIGHT 3
        for k, i in enumerate(range(size + 1, size + 1 + size)):
            egress = (i, size + 1)
            ingress = (2 * size + 1, 1 + k)
            cls.update_map(M, egress, Direction.LEFT, ingress, Direction.DOWN)
        #
        #  3
        # 145
        #  6
        #
        # LEFT 4 -> RIGHT 1; LEFT 1 -> RIGHT 4 (covered)
        # UP 4 -> RIGHT 3; LEFT 3 -> DOWN 4 (covered)
        #
        #  4
        # 356
        #  2
        #
        # LEFT 5 -> UP 3; DOWN 3 -> RIGHT 5 (covered)
        # DOWN 5 -> UP 2; DOWN 2 -> UP 5 (covered)
        #
        #  3
        # 452
        #  6
        #
        # RIGHT 5 -> LEFT 2; RIGHT 2 -> LEFT 5 (covered)
        # DOWN 5 -> LEFT 6; RIGHT 6 -> UP 5
        for k, j in enumerate(range(size + 1, size + 1 + size)):
            egress = (size * 3, size + 1 + k)
            ingress = (size * 3 + 1 + k, size)
            cls.update_map(M, egress, Direction.DOWN, ingress, Direction.LEFT)
        #
        #  4
        # 165
        #  2
        #
        # RIGHT 6 -> UP 5; DOWN 5 -> LEFT 6 (covered)
        # DOWN 6 -> DOWN 2; UP 2 -> UP 6 (covered)
        # LEFT 6 -> DOWN 1; UP 1 -> RIGHT 6 (covered)
        return M


class TestCube(Cube):
    """Provides wrapping configuration

      1
    234
      56
    """

    @classmethod
    @cache
    def WRAP_MAP(cls, size=4):
        M = {}
        #
        #  2
        # 316
        #  4
        #
        # RIGHT 1 -> LEFT 6; RIGHT 6 -> LEFT 1
        for k, i in enumerate(range(1, 1 + size)):
            egress = (i, size * 3)
            ingress = (size * 3 - k, size * 3)
            cls.update_map(M, egress, Direction.RIGHT, ingress, Direction.LEFT)
        # LEFT 1 -> DOWN 3; UP 3 -> RIGHT 1
        for k, i in enumerate(range(1, 1 + size)):
            egress = (i, 1 + size * 2)
            ingress = (1 + size, 1 + size + k)
            cls.update_map(M, egress, Direction.LEFT, ingress, Direction.DOWN)
        # UP 1 -> DOWN 2; UP 2 -> DOWN 1
        for k, j in enumerate(range(1 + size * 2, 1 + size * 2 + size)):
            egress = (1, j)
            ingress = (1 + size, 1 + k)
            cls.update_map(M, egress, Direction.UP, ingress, Direction.DOWN)
        #
        #  1
        # 623
        #  5
        #
        # DOWN 2 -> UP 5; DOWN 5 -> UP 2
        for k, j in enumerate(range(1, 1 + size)):
            egress = (2 * size, j)
            ingress = (3 * size, 3 * size - k)
            cls.update_map(M, egress, Direction.DOWN, ingress, Direction.UP)
        # LEFT 2 -> UP 6; DOWN 6 -> RIGHT 2
        for k, i in enumerate(range(1 + size, 1 + size + size)):
            egress = (i, 1)
            ingress = (3 * size, 3 * size + 1 + k)
            cls.update_map(M, egress, Direction.LEFT, ingress, Direction.UP)
        # UP 2 -> DOWN 1; UP 1; DOWN 2 (covered)
        #
        #  1
        # 234
        #  5
        #
        # DOWN 3 -> RIGHT 5; LEFT 5 -> UP 3
        for k, j in enumerate(range(1 + size, 1 + size + size)):
            egress = (2 * size, j)
            ingress = ((size - 1) * size - k, 2 * size + 1)
            cls.update_map(M, egress, Direction.DOWN, ingress, Direction.RIGHT)
        # UP 3 -> RIGHT 1; LEFT 1 -> DOWN 3 (covered)
        #
        #  1
        # 346
        #  5
        #
        # RIGHT 4 -> DOWN 6; UP 6 -> LEFT 4
        for k, i in enumerate(range(1 + size, 1 + size + size)):
            egress = (i, 3 * size)
            ingress = (2 * size + 1, 4 * size - k)
            cls.update_map(M, egress, Direction.RIGHT, ingress, Direction.DOWN)
        #
        #  4
        # 356
        #  2
        #
        # LEFT 5 -> UP 3; DOWN 3 -> RIGHT 5 (covered)
        # DOWN 5 -> UP 2; DOWN 2 -> UP 5 (covered)
        #
        #  4
        # 561
        #  2
        #
        # RIGHT 6 -> LEFT 1; RIGHT 1 -> LEFT 6 (covered)
        # DOWN 6 -> RIGHT 2; LEFT 2 -> UP 6 (covered)
        # UP 6 -> LEFT 4; RIGHT 4 -> DOWN 6 (covered)
        return M


if __name__ == '__main__':
    main()
