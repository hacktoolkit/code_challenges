# Python Standard Library Imports
import re

from utils import (
    Re,
    ingest,
)


INPUT_FILE = '16.in'
EXPECTED_ANSWERS = (26988, None, )

# INPUT_FILE = '16.test.in'
# EXPECTED_ANSWERS = (71, None, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        data = ingest(INPUT_FILE, as_groups=True)
        self.ticket_scanner = TicketScanner(*data)

    def solve1(self):
        answer = self.ticket_scanner.get_ticket_scanning_error_rate()

        self.answer1 = answer
        return answer

    def solve2(self):
        answer = None

        self.answer2 = answer
        return answer


class TicketScanner:
    RULE_REGEX = re.compile(r'^(?P<field>[a-z][a-z ]+): (?P<range1_lower>\d+)-(?P<range1_upper>\d+) or (?P<range2_lower>\d+)-(?P<range2_upper>\d+)$')

    def __init__(self, rules, ticket, nearby_tickets):
        self.fields = {}

        for rule in rules:
            regex = Re()
            if regex.match(TicketScanner.RULE_REGEX, rule):
                m = regex.last_match
                field, range1_lower, range1_upper, range2_lower, range2_upper = (
                    m.group('field'),
                    int(m.group('range1_lower')),
                    int(m.group('range1_upper')),
                    int(m.group('range2_lower')),
                    int(m.group('range2_upper')),
                )
                self.fields[field] = [
                    range1_lower,
                    range1_upper,
                    range2_lower,
                    range2_upper,
                ]
            else:
                raise Exception('Bad rule: %s' % rule)

        self.ticket = [int(x) for x in ticket[1].split(',')]
        self.nearby_tickets = [
            [int(x) for x in ticket.split(',')]
            for ticket
            in nearby_tickets[1:]
        ]

    @property
    def ranges(self):
        ranges = list(self.fields.values())
        return ranges

    def is_valid_value(self, value):
        is_valid = False

        for r in self.ranges:
            if r[0] <= value <= r[1] or r[2] <= value <= r[3]:
                is_valid = True
                break

        return is_valid

    def get_ticket_scanning_error_rate(self):
        error_rate = 0
        for ticket in self.nearby_tickets:
            for value in ticket:
                if not self.is_valid_value(value):
                    error_rate += value

        return error_rate


if __name__ == '__main__':
    main()
