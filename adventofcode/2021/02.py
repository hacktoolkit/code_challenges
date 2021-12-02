# Third Party (PyPI) Imports
from utils import (
    BaseSolution,
    InputConfig,
    ingest,
)


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

    solution = Solution('02.in', input_config, EXPECTED_ANSWERS)
    # solution = Solution('02.test.in', input_config, TEST_EXPECTED_ANSWERS)

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
        position.do_moves1(self.moves)

        answer = position.x * position.y
        return answer

    def solve2(self):
        position = Position()
        position.do_moves2(self.moves)

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

    def do_moves1(self, moves):
        for move in moves:
            self.do_move1(move)

    def do_move1(self, move):
        change = move.orientation * move.distance
        if move.direction in ('forward',):
            self.x += change
        elif move.direction in ('up', 'down',):
            self.y += change
        else:
            print(f'Invalid move: {move}')

    def do_moves2(self, moves):
        for move in moves:
            self.do_move2(move)

    def do_move2(self, move):
        change = move.orientation * move.distance
        if move.direction in ('forward',):
            self.x += change
            self.y += self.aim * move.distance
        elif move.direction in ('up', 'down',):
            self.aim += change
        else:
            print(f'Invalid move: {move}')


if __name__ == '__main__':
    main()
