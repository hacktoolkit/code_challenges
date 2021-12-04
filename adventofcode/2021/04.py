from utils import (
    BaseSolution,
    InputConfig,
    ingest,
)


PROBLEM_NUM = '04'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (None, None, )
TEST_EXPECTED_ANSWERS = (4512, 1924, )


def main():
    input_config = InputConfig(
        as_integers=False,
        as_json=False,
        as_groups=True,
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
        data = self.data

    def solve1(self):
        bingo = Bingo(self.data)
        board = bingo.find_winner()
        print(board)

        answer = board.score
        return answer

    def solve2(self):
        bingo = Bingo(self.data)
        board = bingo.find_last_winner()
        print(board)

        answer = board.score
        return answer


class Bingo:
    def __init__(self, raw_data):
        self.numbers = [int(n) for n in raw_data[0][0].split(',')]
        self.boards = [
            BingoBoard(raw_board)
            for raw_board
            in raw_data[1:]
        ]

    def find_winner(self):
        winner = None
        for n in self.numbers:
            for board in self.boards:
                board.play(n)
                if board.has_won():
                    winner = board
                    break
            if winner is not None:
                break

        return winner

    def find_last_winner(self):
        winner = None

        num_boards = len(self.boards)

        for n in self.numbers:
            for board in self.boards:
                board.play(n)

                num_winners = sum([
                    1 if board.has_won() else 0
                    for board
                    in self.boards
                ])

                if num_winners == num_boards:
                    winner = board
                    break

            if winner is not None:
                break

        return winner


class BingoBoard:
    def __init__(self, raw_board):
        self.raw_board = raw_board
        self.board = [
            [
                int(j)
                for j
                in raw_board[i].split(' ')
                if j != ''
            ]
            for i in range(5)
        ]

        self.drawn_numbers = []

    def __str__(self):
        s = ''
        for i in range(5):
            for j in range(5):
                s += str(self.board[i][j]) + ' '
            s += '\n'

        s += '\n'
        s += str(self.drawn_numbers)

        return s

    def play(self, n):
        self.drawn_numbers.append(n)
        for i in range(5):
            for j in range(5):
                if self.board[i][j] == n:
                    self.board[i][j] = None

    def has_won(self):
        has_won = False
        # check for row wins
        for i in range(5):
            numbers = [n for n in self.board[i] if n is not None]
            if len(numbers) == 0:
                has_won = True
                break

        # check for column wins
        for j in range(5):
            numbers = [
                self.board[i][j]
                for i in range(5)
                if self.board[i][j] is not None
            ]
            if len(numbers) == 0:
                has_won = True
                break

        return has_won

    @property
    def sum_unmarked_numbers(self):
        total = 0

        for i in range(5):
            for j in range(5):
                val = self.board[i][j]
                if val is not None:
                    total += val

        return total

    @property
    def score(self):
        return self.sum_unmarked_numbers * self.drawn_numbers[-1]


if __name__ == '__main__':
    main()
