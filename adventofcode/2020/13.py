# Python Standard Library Imports
import copy
import math

# Third Party (PyPI) Imports
from sympy.ntheory.modular import crt as chinese_remainder_theorem

from utils import (
    BaseSolution,
    InputConfig,
    config,
    debug,
    ingest,
    main,
    solution,
)


config.EXPECTED_ANSWERS = (8063, 775230782877242)
config.TEST_CASES = {
    '': (295, 1068781),
    'b': (130, 3417),
    'c': (295, 754018),
    'd': (295, 779210),
    'e': (295, 1261476),
    'f': (47, 1202161486),
}


@solution
class Solution(BaseSolution):
    def process_data(self):
        data = self.data
        self.earliest_departure_time = int(data[0])
        bus_ids = [int(bid) if bid != 'x' else 0 for bid in data[1].split(',')]

        self.bus_schedule = BusSchedule(bus_ids)

    def solve1(self):
        bus_schedule = self.bus_schedule
        earliest_departure_time = self.earliest_departure_time

        bus_id, departure_time = bus_schedule.get_earliest_departure(
            earliest_departure_time
        )

        minutes_waiting = departure_time - earliest_departure_time
        answer = bus_id * minutes_waiting
        return answer

    def solve2(self):
        bus_schedule = self.bus_schedule
        answer = bus_schedule.get_earliest_sequential_departure()
        return answer


class BusSchedule:
    def __init__(self, bus_ids):
        self.bus_ids = bus_ids

    def get_earliest_departure(self, earliest_departure_time):
        best_bus_id = None
        best_departure_time = None

        for bus_id in filter(None, self.bus_ids):
            trip_num = int(math.ceil(1.0 * earliest_departure_time / bus_id))
            departure_time = bus_id * trip_num

            if best_bus_id is None or departure_time < best_departure_time:
                best_bus_id = bus_id
                best_departure_time = departure_time

        return best_bus_id, best_departure_time

    def get_earliest_sequential_departure(self):
        # result = self.get_earliest_sequential_departure__naive()
        result = self.get_earliest_sequential_departure__fast()
        return result

    def get_earliest_sequential_departure__fast(self):
        """Solve the equation:

        t % a = 0
        (t + 1) % b = 0
        (t + 2) % c = 0
        (t + 3) % d = 0
        ...
        (t + n - 1) % n = 0

        Using the Chinese remainder theorem:
        - https://en.wikipedia.org/wiki/Chinese_remainder_theorem
        - https://en.wikipedia.org/wiki/Chinese_remainder_theorem#Computation

        x = 0 (mod a) = 1 (mod b) = 2 (mod c) = 3 (mod d) = ... = (n - 1) (mod n)
        """
        remainders = []
        moduli = []
        for i, bus_id in enumerate(self.bus_ids):
            if bus_id > 0:
                remainders.append(i)
                moduli.append(bus_id)

        result, lcm = chinese_remainder_theorem(moduli, remainders)
        earliest_departure = lcm - result

        return earliest_departure

    def get_earliest_sequential_departure__naive(self):
        slots = copy.copy(self.bus_ids)

        def _test():
            is_sequential = True
            for i, value in enumerate(slots):
                if value == 0:
                    # skip
                    pass
                elif value == slots[0] + i:
                    # is sequential
                    pass
                else:
                    # out of sequence
                    is_sequential = False
                    break

            return is_sequential

        def _incr_slot_to_n(i, n):
            # nonlocal slots
            value = slots[i]
            bus_id = self.bus_ids[i]
            if value < n:
                difference = n - value
                remainder = difference % bus_id
                trips = difference // bus_id + (1 if remainder > 0 else 0)
                slots[i] = value + bus_id * trips

        if not config.TEST_MODE:
            _incr_slot_to_n(0, 100_000_000_000_000)

        while not _test():
            slots[0] += self.bus_ids[0]
            for i, value in enumerate(slots):
                if i == 0 or value == 0:
                    # skip first slot and blank slots
                    pass
                else:
                    _incr_slot_to_n(i, slots[0] + i)

        return slots[0]


if __name__ == '__main__':
    main()
