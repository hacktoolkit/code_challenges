# Python Standard Library Imports
import math

from utils import ingest


INPUT_FILE = '13.in'
EXPECTED_ANSWERS = (8063, None, )

# INPUT_FILE = '13.test.in'
# EXPECTED_ANSWERS = (295, None, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        data = ingest(INPUT_FILE)

        self.earliest_departure_time = int(data[0])
        bus_ids = [int(bid) for bid in data[1].split(',') if bid != 'x']

        self.bus_schedule = BusSchedule(bus_ids)

    def solve1(self):
        bus_schedule = self.bus_schedule
        earliest_departure_time = self.earliest_departure_time

        bus_id, departure_time = bus_schedule.get_earliest_departure(earliest_departure_time)

        minutes_waiting = departure_time - earliest_departure_time
        answer = bus_id * minutes_waiting

        self.answer1 = answer
        return answer

    def solve2(self):
        answer = None

        self.answer2 = answer
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
