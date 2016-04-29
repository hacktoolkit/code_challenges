"""http://projecteuler.net/problem=096

Su Doku

Su Doku (Japanese meaning number place) is the name given to a popular puzzle concept. Its origin is unclear, but credit must be attributed to Leonhard Euler who invented a similar, and much more difficult, puzzle idea called Latin Squares. The objective of Su Doku puzzles, however, is to replace the blanks (or zeros) in a 9 by 9 grid in such that each row, column, and 3 by 3 box contains each of the digits 1 to 9. Below is an example of a typical starting puzzle grid and its solution grid.

003020600
900305001
001806400
008102900
700000008
006708200
002609500
800203009
005010300

483921657
967345821
251876493
548132976
729564138
136798245
372689514
814253769
695417382

A well constructed Su Doku puzzle has a unique solution and can be solved by logic, although it may be necessary to employ "guess and test" methods in order to eliminate options (there is much contested opinion over this). The complexity of the search determines the difficulty of the puzzle; the example above is considered easy because it can be solved by straight forward direct deduction.
The 6K text file, sudoku.txt (right click and 'Save Link/Target As...'), contains fifty different Su Doku puzzles ranging in difficulty, but all with unique solutions (the first puzzle in the file is the example above).
By solving all fifty puzzles find the sum of the 3-digit numbers found in the top left corner of each solution grid; for example, 483 is the 3-digit number found in the top left corner of the solution grid above.

Solution by jontsai <hello@jontsai.com>
"""
from utils import *

EXPECTED_ANSWER = 0

NUM_ROWS = 9
NUM_COLS = 9
NUM_BOXES = 9
DEFAULT_GRID = '0' * NUM_ROWS * NUM_COLS


class Sudoku(object):
    def __init__(self, name='Sudoku', grid=DEFAULT_GRID, *args, **kwargs):
        self.name = name
        self.grid = grid

    def print_grid(self):
        """Prints this Sudoku grid
        """
        print self.name
        for m in xrange(NUM_ROWS):
            start = m * NUM_COLS
            end = start + NUM_COLS
            print self.grid[start:end]

    def is_valid(self):
        """Checks whether the current grid state is legal
        """
        valid = self.has_valid_rows() and self.has_valid_cols() and self.has_valid_boxes()
        return valid

    def has_valid_rows(self):
        valid = True
        for m in xrange(NUM_ROWS):
            start = m * NUM_COLS
            end = start + NUM_COLS
            row_values = filter(lambda x: x, [int(v) for v in self.grid[start:end]])
            if len(set(row_values)) != len(row_values):
                valid = False
                break
        return valid

    def has_valid_cols(self):
        valid = True
        for n in xrange(NUM_COLS):
            col_values = []
            for m in xrange(NUM_ROWS):
                index = m * NUM_COLS + n
                value = int(self.grid[index])
                if value:
                    col_values.append(value)
            if len(set(col_values)) != len(col_values):
                valid = False
                break
        return valid

    def has_valid_boxes(self):
        valid = True
        for k in xrange(NUM_BOXES):
            box_values = []
            # TODO
            if len(set(box_values)) != len(box_values):
                valid = False
                break
        return valid

    def is_filled(self):
        """Checks whether every cell is filled
        """
        filled = '0' not in self.grid
        return filled

    def solve_brute_force(self):
        """Attempts to solve this Sudoku puzzle by trying every combination
        """
        pass

    def solve(self):
        """Attempts to solve this Sudoku puzzle, if it is solvable
        """
        self.solve_brute_force()

def read_sudokus():
    i = 0
    name = None
    grid = ''
    sudokus = []
    with open('sudoku.txt') as f:
        for line in f.readlines():
            line = line.strip()
            # new grid
            if i % 10 == 0:
                name = line
            else:
                # accumulate the grid
                grid += line
            # last row in grid, construct sudoku
            if i % 10 == 9:
                sudoku = Sudoku(name=name, grid=grid)
                sudokus.append(sudoku)
                name = None
                grid = ''
            # update row num
            i += 1
    return sudokus

def solve():
    sudokus = read_sudokus()
    total = 0
    for sudoku in sudokus:
        sudoku.print_grid()
        sudoku.solve()
        total += int(sudoku.grid[0:3])
    answer = total
    return answer

answer = solve()

print 'Expected: %s, Answer: %s' % (EXPECTED_ANSWER, answer)
