# Python Standard Library Imports
import math


INPUT_FILE = '5.in'


def main():
    # print(BoardingPass('FBFBBFFRLR').seat_id)
    answer = solve()
    print(answer)


def solve():
    data = ingest()
    boarding_pass_seat_ids = [BoardingPass(code).seat_id for code in data]
    answer = max(boarding_pass_seat_ids)
    return answer


class BoardingPass:
    def __init__(self, code):
        self.code = code

    @property
    def seat_id(self):
        seat_id = self.row * 8 + self.col
        return seat_id

    @property
    def row(self):
        dirs = [
            0 if x == 'F' else 1 if x == 'B' else None
            for x
            in self.code[:7]
        ]
        row = binary_walk(dirs, 0, 127)
        return row

    @property
    def col(self):
        dirs = [
            0 if x == 'L' else 1 if x == 'R' else None
            for x
            in self.code[-3:]
        ]
        col = binary_walk(dirs, 0, 7)
        return col


def binary_walk(dirs, lower, upper):
    for step in dirs:
        # print(step, lower, upper)
        mid = (upper + lower) / 2.0
        if step == 0:
            upper = int(math.floor(mid))
        elif step == 1:
            lower = int(math.ceil(mid))
        else:
            raise Exception('Illegal step')

    if lower == upper:
        result = lower
    else:
        raise Exception('lower != upper, %s != %s' % (lower, upper))
    return result


def ingest():
    with open(INPUT_FILE, 'r') as f:
        data = [line.strip() for line in f.readlines()]
    return data


if __name__ == '__main__':
    main()
