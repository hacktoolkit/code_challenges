# Python Standard Library Imports
import math

from utils import ingest


INPUT_FILE = '5.in'
EXPECTED_ANSWERS = (959, 527, )


def main():
    # print(BoardingPass('FBFBBFFRLR').seat_id)
    answers = (solve1(), solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


def solve1():
    data = ingest(INPUT_FILE)
    boarding_pass_seat_ids = [BoardingPass(code).seat_id for code in data]
    answer = max(boarding_pass_seat_ids)
    return answer


def solve2():
    data = ingest(INPUT_FILE)
    boarding_pass_seat_ids = [BoardingPass(code).seat_id for code in data]
    unoccupied_seats = set(list(range(128 * 8))) - set(boarding_pass_seat_ids)

    # print(unoccupied_seats)

    answer = None

    prev_seat = None
    for seat_id in unoccupied_seats:
        if prev_seat is None:
            prev_seat = seat_id
        else:
            if seat_id > prev_seat + 1:
                answer = seat_id
                break
            prev_seat = seat_id

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


if __name__ == '__main__':
    main()
