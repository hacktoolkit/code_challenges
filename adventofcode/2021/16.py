# Python Standard Library Imports
import operator
from collections import defaultdict
from functools import reduce

from utils import (
    BaseSolution,
    InputConfig,
    pairwise,
)


PROBLEM_NUM = '16'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (986, 18234816469452, )

# TEST_VERSION = 'a'
# TEST_EXPECTED_ANSWERS = (16, 15, )

# TEST_VERSION = 'b'
# TEST_EXPECTED_ANSWERS = (12, 46, )

# TEST_VERSION = 'c'
# TEST_EXPECTED_ANSWERS = (23, 46, )

TEST_VERSION = 'd'
TEST_EXPECTED_ANSWERS = (31, 54, )


def main():
    input_config = InputConfig(
        as_integers=False,
        as_comma_separated_integers=False,
        as_json=False,
        as_groups=False,
        as_oneline=False,
        as_table=False,
        row_func=None,
        cell_func=None
    )

    if TEST_MODE:
        input_filename = f'{PROBLEM_NUM}{TEST_VERSION}.test.in'
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

        hex_input = data[0]

        # hex_input = 'D2FE28'  # value: 2021
        # hex_input = '38006F45291200'  # version sum: 9
        # hex_input = 'EE00D40C823060'  # version sum: 14

        self.packet = Packet(hex_input=hex_input)

    def solve1(self):
        packet = self.packet

        version_sum = 0
        packets = [packet]
        while len(packets) > 0:
            p = packets.pop()
            version_sum += p.version
            packets.extend(p.subpackets)

        answer = version_sum
        return answer

    def solve2(self):
        packet = self.packet
        answer = packet.value
        return answer


HexMap = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}


def hex2bin(hex_digits):
    b = ''.join([HexMap[hex_dig] for hex_dig in hex_digits])
    return b


class Packet:
    VERSION_BITS_START = 0
    VERSION_BITS_END = 3

    TYPE_BITS_START = 3
    TYPE_BITS_END = 6

    LITERAL_GROUP_SIZE = 5

    LENGTH_TYPE_BITS_START = 6
    LENGTH_TYPE_BITS_END = 7

    LENGTH_TYPE_0_BITS_START = 7
    LENGTH_TYPE_0_BITS_END = 7 + 15

    LENGTH_TYPE_1_BITS_START = 7
    LENGTH_TYPE_1_BITS_END = 7 + 11

    @classmethod
    def subpackets_from_bits(cls, subpackets_bits, limit=None):
        packets = []
        bits_consumed = 0

        while (
            len(subpackets_bits) > 0
            and (
                limit is None
                or len(packets) < limit
            )
        ):
            # guess the subpacket type by looking ahead at the next bits
            # naively create 1 packet from all `subpackets_bits`
            test_packet = Packet(n_bin=subpackets_bits)

            end_index = test_packet.end_index
            packet_bits = subpackets_bits[:end_index]
            subpackets_bits = subpackets_bits[end_index:]
            packet = Packet(n_bin=packet_bits)
            packets.append(packet)
            bits_consumed += len(packet.n_bin)

        return packets, bits_consumed

    def __init__(self, hex_input=None, n_bin=None):
        if hex_input is not None:
            self.hex_input = hex_input

            self.n = int(hex_input, 16)

            # must manually expand as opposed to using `bin(n)[2:]`
            # because the latter will drop off significant leading 0's
            self.n_bin = hex2bin(hex_input)

        if n_bin is not None:
            self.n_bin = n_bin

        if self.packet_type == 'literal':
            self._calculate_literal_value()
            self.subpackets = []
        elif self.packet_type == 'operator':
            self._find_subpackets()

    @property
    def version(self):
        return int(self.n_bin[Packet.VERSION_BITS_START:Packet.VERSION_BITS_END], 2)

    @property
    def type_id(self):
        return int(self.n_bin[Packet.TYPE_BITS_START:Packet.TYPE_BITS_END], 2)

    @property
    def packet_type(self):
        if self.type_id == 4:
            t = 'literal'
        else:
            t = 'operator'

        return t

    @property
    def length_type_id(self):
        return int(self.n_bin[Packet.LENGTH_TYPE_BITS_START:Packet.LENGTH_TYPE_BITS_END], 2)

    @property
    def subpackets_bits_length(self):
        if self.length_type_id == 0:
            length = int(self.n_bin[Packet.LENGTH_TYPE_0_BITS_START:Packet.LENGTH_TYPE_0_BITS_END], 2)
        else:
            length = None
        return length

    @property
    def subpackets_bits(self):
        if self.length_type_id == 0:
            subpackets_bits = self.n_bin[Packet.LENGTH_TYPE_0_BITS_END:Packet.LENGTH_TYPE_0_BITS_END + self.subpackets_bits_length]
        elif self.length_type_id == 1:
            # for now, naively / optimistically assume all remaining bits are for subpackets
            # only count until the length is reached
            subpackets_bits = self.n_bin[Packet.LENGTH_TYPE_1_BITS_END:]
        else:
            raise Exception('Invalid length type id')
        return subpackets_bits

    @property
    def num_subpackets(self):
        if self.length_type_id == 1:
            num_subpackets = int(self.n_bin[Packet.LENGTH_TYPE_1_BITS_START:Packet.LENGTH_TYPE_1_BITS_END], 2)
        else:
            num_subpackets = 0

        return num_subpackets

    @property
    def value(self):
        if self.packet_type == 'literal':
            value = self.literal_value
        elif self.packet_type == 'operator':
            subpacket_values = [subpacket.value for subpacket in self.subpackets]
            if self.type_id == 0:
                # sum
                value = sum(subpacket_values)
            elif self.type_id == 1:
                # product
                value = reduce(operator.mul, [1] + subpacket_values)
            elif self.type_id == 2:
                value = min(subpacket_values)
            elif self.type_id == 3:
                value = max(subpacket_values)
            elif self.type_id in (5, 6, 7, ):
                a, b = subpacket_values
                operators = {
                    5: operator.gt,
                    6: operator.lt,
                    7: operator.eq,
                }
                op = operators[self.type_id]
                value = 1 if op(a, b) else 0
            else:
                raise Exception('Invalid type id')
        else:
            raise Exception('Invalid packet type')
        return value

    def _calculate_literal_value(self):
        start = Packet.TYPE_BITS_END

        bits = []

        has_more = True
        while has_more:
            end = start + Packet.LITERAL_GROUP_SIZE
            group = self.n_bin[start:end]
            bits.append(group[1:])
            has_more = int(group[0]) == 1
            start = end

        self.end_index = end
        self.literal_value = int(''.join(bits), 2)

    def _find_subpackets(self):
        if self.length_type_id == 0:
            self.subpackets, bits_consumed = Packet.subpackets_from_bits(self.subpackets_bits)
            self.end_index = Packet.LENGTH_TYPE_0_BITS_END + self.subpackets_bits_length
        elif self.length_type_id == 1:
            self.subpackets, bits_consumed = Packet.subpackets_from_bits(self.subpackets_bits, limit=self.num_subpackets)
            self.end_index = Packet.LENGTH_TYPE_1_BITS_END + bits_consumed
        else:
            raise Exception('Invalid length type id')


if __name__ == '__main__':
    main()
