# Third Party (PyPI) Imports
from utils import (
    BaseSolution,
    InputConfig,
    ingest,
)


PROBLEM_NUM = '02'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (1882980, 1971232560, )
TEST_EXPECTED_ANSWERS = (150, 900, )


def main():
    input_config = InputConfig(
        as_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=False,
        cell_func=None
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
        self.moves = [
            Move(raw_move)
            for raw_move
            in self.data
        ]

    def solve1(self):
        position = Position()
        position.do_moves(self.moves, mode=1)

        answer = position.x * position.y
        return answer

    def solve2(self):
        position = Position()
        position.do_moves(self.moves, mode=2)

        answer = position.x * position.y
        return answer


class Move:
    def __init__(self, raw_move):
        self.direction, self.distance = raw_move.split(' ')
        self.distance = int(self.distance)

    def __str__(self):
        return f'{self.direction}({self.orientation}): {self.distance}'

    @property
    def orientation(self):
        orientation = {
            'forward': 1,
            'up': -1,
            'down': 1,
        }
        return orientation[self.direction]


class Position:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.aim = 0

    def do_moves(self, moves, mode):
        for move in moves:
            self.do_move(move, mode)

    def do_move(self, move, mode):
        change = move.orientation * move.distance

        if move.direction in ('forward',):
            if mode == 1:
                self.x += change
            elif mode == 2:
                self.x += change
                self.y += self.aim * move.distance
        elif move.direction in ('up', 'down',):
            if mode == 1:
                self.y += change
            elif mode == 2:
                self.aim += change
        else:
            print(f'Invalid move: {move}')


if __name__ == '__main__':
    main()
