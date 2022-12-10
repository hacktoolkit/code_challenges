from utils import (
    CRT,
    BaseSolution,
    config,
    debug,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (638, 'CJCKBAPB')
config.TEST_CASES = {
    '': (17, '--------'),
}

config.INPUT_CONFIG.as_integers = False
config.INPUT_CONFIG.as_comma_separated_integers = False
config.INPUT_CONFIG.as_json = False
config.INPUT_CONFIG.as_groups = True
config.INPUT_CONFIG.strip_lines = True
config.INPUT_CONFIG.as_oneline = False
config.INPUT_CONFIG.as_coordinates = False
config.INPUT_CONFIG.coordinate_delimeter = None
config.INPUT_CONFIG.as_table = False
config.INPUT_CONFIG.row_func = None
config.INPUT_CONFIG.cell_func = None


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        raw_coords, raw_folds = data
        self.paper = Paper(raw_coords, raw_folds)

    def solve1(self):
        paper = self.paper
        paper.perform_fold()

        answer = paper.num_visible
        return answer

    def solve2(self):
        paper = self.paper
        paper.perform_all_folds()

        print(paper)

        with open(f'{config.PROBLEM_NUM}.out', 'w') as f:
            f.write(str(paper))

        debug(paper.num_visible)

        crt = CRT()
        crt.load_rendered(str(paper))

        answer = crt.read_characters()
        return answer


class Paper:
    def __init__(self, raw_coords, raw_folds):
        self.coords = [
            [int(c) for c in raw_coord.split(',')] for raw_coord in raw_coords
        ]

        self.grid = set()
        for (x, y) in self.coords:
            self.grid.add((x, y))

        self.reset_bounds()

        folds = [
            raw_fold.removeprefix('fold along ').split('=')
            for raw_fold in raw_folds
        ]
        self.folds = [[fold[0], int(fold[1])] for fold in folds]

        self.fold_n = 0

    def __str__(self):
        buf = []
        for y in range(self.max_y + 1):
            for x in range(self.max_x + 1):
                is_visible = (x, y) in self.grid
                c = '#' if is_visible else '.'
                buf.append(c)
            buf.append('\n')

        s = ''.join(buf)
        return s

    def reset_bounds(self):
        self.max_x = max([coord[0] for coord in self.grid])
        self.max_y = max([coord[1] for coord in self.grid])

    def perform_fold(self):
        fold = self.folds[self.fold_n]
        self.fold_n += 1
        fold_dimension, fold_position = fold

        for x in range(self.max_x + 1):
            for y in range(self.max_y + 1):
                dim = x if fold_dimension == 'x' else y
                if (x, y) in self.grid and dim > fold_position:
                    d = dim - fold_position
                    new_dim = fold_position - d
                    self.grid.remove((x, y))
                    new_coord = (
                        (new_dim, y) if fold_dimension == 'x' else (x, new_dim)
                    )
                    self.grid.add(new_coord)

        self.reset_bounds()

    def perform_all_folds(self):
        while self.fold_n < len(self.folds):
            self.perform_fold()

    @property
    def num_visible(self):
        return len(self.grid)


if __name__ == '__main__':
    main()
