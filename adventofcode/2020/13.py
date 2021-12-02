# Python Standard Library Imports
import math

from utils import (
    BaseSolution,
    InputConfig,
    ingest,
)


PROBLEM_NUM = '13'

TEST_MODE = False
#TEST_MODE = True

EXPECTED_ANSWERS = (8063, None, )
TEST_EXPECTED_ANSWERS = (295, None, )


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
        data = self.data
        self.earliest_departure_time = int(data[0])
        bus_ids = [int(bid) for bid in data[1].split(',') if bid != 'x']

        self.bus_schedule = BusSchedule(bus_ids)

    def solve1(self):
        bus_schedule = self.bus_schedule
        earliest_departure_time = self.earliest_departure_time

        bus_id, departure_time = bus_schedule.get_earliest_departure(earliest_departure_time)

        minutes_waiting = departure_time - earliest_departure_time
        answer = bus_id * minutes_waiting
        return answer

    def solve2(self):
        #
        # TODO: FILL THIS IN
        #
        answer = None
        return answer


class BusSchedule:
    def __init__(self, bus_ids):
        self.bus_ids = bus_ids

    def get_earliest_departure(self, earliest_departure_time):
        best_bus_id = None
        best_departure_time = None

        for bus_id in self.bus_ids:
            trip_num = int(math.ceil(1.0 * earliest_departure_time / bus_id))
            departure_time = bus_id * trip_num

            if best_bus_id is None or departure_time < best_departure_time:
                best_bus_id = bus_id
                best_departure_time = departure_time

        return best_bus_id, best_departure_time


if __name__ == '__main__':
    main()
