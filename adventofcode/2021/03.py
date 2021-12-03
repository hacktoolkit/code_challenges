# Python Standard Library Imports
import copy

from utils import (
    BaseSolution,
    InputConfig,
    ingest,
)


PROBLEM_NUM = '03'

TEST_MODE = False
# TEST_MODE = True

EXPECTED_ANSWERS = (4147524, 3570354, )
TEST_EXPECTED_ANSWERS = (198, 230, )


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

    def solve1(self):
        submarine = Submarine(self.data)

        answer = submarine.power_consumption
        return answer

    def solve2(self):
        submarine = Submarine(self.data)

        answer = submarine.life_support_rating
        return answer


class Submarine:
    def __init__(self, diagnostic_report):
        self.diagnostic_report = diagnostic_report

    def _count_bits(self, bin_numbers, index):
        b1 = 0
        b0 = 0

        for n in bin_numbers:
            b = n[index]
            b1 += 1 if b == '1' else 0
            b0 += 1 if b == '0' else 0

        return b1, b0


    def _most_frequent_bit(self, bin_numbers, index):
        b1, b0 = self._count_bits(bin_numbers, index)
        mfb = '1' if b1 >= b0 else '0'
        return mfb

    def _least_frequent_bit(self, bin_numbers, index):
        b1, b0 = self._count_bits(bin_numbers, index)
        lfb = '1' if b1 < b0 else '0'
        return lfb

    def bin2dec(self, b):
      return int(b, base=2)

    ##
    # Part 1

    @property
    def gamma_rate(self):
        # most common bit for each position
        size = len(self.diagnostic_report[0])
        new_bits = [
            self._most_frequent_bit(self.diagnostic_report, i)
            for i
            in range(size)
        ]
        rate_bits = ''.join(new_bits)
        rate = self.bin2dec(rate_bits)
        return rate

    @property
    def epsilon_rate(self):
        # least common bit for each position
        size = len(self.diagnostic_report[0])
        new_bits = [
            self._least_frequent_bit(self.diagnostic_report, i)
            for i
            in range(size)
        ]
        rate_bits = ''.join(new_bits)
        rate = self.bin2dec(rate_bits)
        return rate

    @property
    def power_consumption(self):
        return self.gamma_rate * self.epsilon_rate

    ##
    # Part 2

    @property
    def oxygen_generator_rating(self):
        size = len(self.diagnostic_report[0])

        bin_numbers = copy.copy(self.diagnostic_report)

        for i in range(size):
            mfb = self._most_frequent_bit(bin_numbers, i)
            bin_numbers = [n for n in bin_numbers if n[i] == mfb]

            if len(bin_numbers) == 1:
                break

        rating_bin = bin_numbers[0]
        rating = self.bin2dec(rating_bin)
        return rating

    @property
    def co2_scrubber_rating(self):
        size = len(self.diagnostic_report[0])

        bin_numbers = copy.copy(self.diagnostic_report)

        for i in range(size):
            lfb = self._least_frequent_bit(bin_numbers, i)
            bin_numbers = [n for n in bin_numbers if n[i] == lfb]

            if len(bin_numbers) == 1:
                break

        rating_bin = bin_numbers[0]
        rating = self.bin2dec(rating_bin)
        return rating

    @property
    def life_support_rating(self):
        return self.oxygen_generator_rating * self.co2_scrubber_rating


if __name__ == '__main__':
    main()
