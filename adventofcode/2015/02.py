from utils import (
    BaseSolution,
    config,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (1588178, 3783758)


@solution
class Solution(BaseSolution):
    def process_data(self):
        self.presents = [Present(dimensions) for dimensions in self.data]

    def solve1(self):
        answer = sum([present.wrapping_paper_area for present in self.presents])
        return answer

    def solve2(self):
        answer = sum([present.total_ribbon for present in self.presents])
        return answer


class Present:
    def __init__(self, dimensions):
        self.l, self.w, self.h = [int(x) for x in dimensions.split('x')]

    @property
    def surface_area(self):
        l, w, h = self.l, self.w, self.h
        area = 2 * l * w + 2 * w * h + 2 * h * l
        return area

    @property
    def lw_area(self):
        return self.l * self.w

    @property
    def wh_area(self):
        return self.w * self.h

    @property
    def lh_area(self):
        return self.l * self.h

    @property
    def smallest_side_area(self):
        return min(
            [
                self.lw_area,
                self.wh_area,
                self.lh_area,
            ]
        )

    @property
    def wrapping_paper_area(self):
        return self.surface_area + self.smallest_side_area

    @property
    def smallest_perimeter(self):
        a, b, c = sorted([self.l, self.w, self.h])
        return 2 * a + 2 * b

    @property
    def volume(self):
        return self.l * self.w * self.h

    @property
    def total_ribbon(self):
        return self.smallest_perimeter + self.volume


if __name__ == '__main__':
    main()
