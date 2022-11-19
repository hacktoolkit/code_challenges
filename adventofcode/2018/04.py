# Python Standard Library Imports
import copy
import math
import re
from collections import defaultdict
from dataclasses import (
    dataclass,
    fields,
)

from utils import (
    BaseSolution,
    InputConfig,
    Re,
)


PROBLEM_NUM = '04'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (
    125444,
    18325,
)
TEST_EXPECTED_ANSWERS = (
    240,
    4455,
)


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=False,
        row_func=None,
        cell_func=None,
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

        raw_events = list(sorted(data))
        events = [
            event
            for raw_event in raw_events
            if (event := Event.from_line(raw_event))
        ]
        self.log = Log(events)

    def solve1(self):
        log = self.log
        guard, minutes_asleep = log.get_sleepiest_guard()
        answer = guard.guard_num * guard.sleepiest_minute
        return answer

    def solve2(self):
        log = self.log
        guard, sleepiest_minute = log.get_most_consistently_sleepy_guard()
        answer = guard.guard_num * sleepiest_minute
        return answer


@dataclass
class Event:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    message: str

    REGEX = re.compile(
        r'^\[(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2}) (?P<hour>\d{2}):(?P<minute>\d{2})\] (?P<message>.*)$'
    )
    GUARD_REGEX = re.compile(r'^Guard #(?P<guard_num>\d+) begins shift$')

    @classmethod
    def from_line(cls, line):
        regex = Re()
        if regex.match(cls.REGEX, line):
            m = regex.last_match

            def _value_of(m, field):
                raw_value = m.group(field.name)
                value = int(raw_value) if field.type == int else raw_value
                return value

            kwargs = {field.name: _value_of(m, field) for field in fields(cls)}
            obj = cls(**kwargs)
        else:
            obj = None
        return obj

    @property
    def guard_num(self):
        m = self.GUARD_REGEX.match(self.message)
        guard_num = int(m.group('guard_num')) if m else None
        return guard_num


class Log:
    def __init__(self, events):
        self.events = events

        self.guards = {}

        self._process_events()
        self._calculate_sleep_stats()

    def _process_events(self):
        guard = None

        for event in self.events:
            if event.message == 'falls asleep':
                guard.sleep(event)
            elif event.message == 'wakes up':
                guard.wake(event)
            else:
                guard_num = event.guard_num
                if guard_num:
                    if guard_num in self.guards:
                        guard = self.guards[guard_num]
                    else:
                        guard = Guard(guard_num)
                        self.guards[guard_num] = guard
                else:
                    raise Exception(f'Bad event message: {event.message}')

    def _calculate_sleep_stats(self):
        for guard_num, guard in self.guards.items():
            guard.calculate_sleep_stats()

    def get_sleepiest_guard(self):
        sleepiest_guard = None
        best_sleep_minutes = None

        for guard_num, guard in self.guards.items():
            minutes_asleep = guard.minutes_asleep

            if sleepiest_guard is None or minutes_asleep > best_sleep_minutes:
                sleepiest_guard = guard
                best_sleep_minutes = minutes_asleep

        return sleepiest_guard, best_sleep_minutes

    def get_most_consistently_sleepy_guard(self):
        consistently_sleepy_guard = None
        sleepiest_minute = None
        sleepiest_minute_count = None

        for guard_num, guard in self.guards.items():
            minute = guard.sleepiest_minute
            count = guard.sleepiest_minute_count

            if (
                consistently_sleepy_guard is None
                or count > sleepiest_minute_count
            ):
                consistently_sleepy_guard = guard
                sleepiest_minute = minute
                sleepiest_minute_count = count

        return consistently_sleepy_guard, sleepiest_minute


class Guard:
    def __init__(self, guard_num):
        self.guard_num = guard_num

        self.sleep_periods = []
        self.sleep_event = None

    def sleep(self, sleep_event):
        self.sleep_event = sleep_event

    def wake(self, wake_event):
        period = (self.sleep_event, wake_event)
        self.sleep_periods.append(period)
        self.sleep_event = None

    def calculate_sleep_stats(self):
        minutes_asleep = 0
        sleeping_minutes_count = [0] * 60

        for sleep_event, wake_event in self.sleep_periods:
            for minute in range(sleep_event.minute, wake_event.minute):
                sleeping_minutes_count[minute] += 1

            minutes_asleep += wake_event.minute - sleep_event.minute

        self.minutes_asleep = minutes_asleep

        sleepiest_minute = None
        sleepiest_minute_count = None

        # calculate sleepiest minute
        for minute, count in enumerate(sleeping_minutes_count):
            if sleepiest_minute is None or count > sleepiest_minute_count:
                sleepiest_minute = minute
                sleepiest_minute_count = count

        self.sleepiest_minute = sleepiest_minute
        self.sleepiest_minute_count = sleepiest_minute_count


if __name__ == '__main__':
    main()
