# Python Standard Library Imports
import re

from utils import ingest


INPUT_FILE = '07.in'
EXPECTED_ANSWERS = (110, 242, )

# INPUT_FILE = '07.test.in'
# EXPECTED_ANSWERS = (2, 3, )


def main():
    solution = Solution()
    answers = (solution.solve1(), solution.solve2(), )
    print(answers)
    assert(answers == EXPECTED_ANSWERS)


class Solution:
    def __init__(self):
        self.data = ingest(INPUT_FILE)
        self.ips = [IPV7(ip) for ip in self.data]

    def solve1(self):
        count = 0
        for ip in self.ips:
            if ip.supports_tls:
                count += 1

        answer = count
        return answer

    def solve2(self):
        count = 0
        for ip in self.ips:
            if ip.supports_ssl:
                count += 1

        answer = count
        return answer


def has_abba(code):
    """Checks for existence of a 4-letter palindromic substring within `code`
    The palindromic substring must contain 2 unique characters
    """
    palindrome = None
    for i in range(len(code) - 4 + 1):
        # substring = code[i:i + 4]
        if code[i] == code[i + 3] and code[i + 1] == code[i + 2]:
            palindrome = code[i:i + 4]
            break

    result = palindrome and len(set([c for c in palindrome])) == 2
    return result


def find_aba(code):
    """Checks for existence of a 3-letter palindromic substring within `code`
    The palindromic substring must contain 2 unique characters
    """
    palindromes = []
    for i in range(len(code) - 3 + 1):
        # substring = code[i:i + 3]
        if code[i] == code[i + 2] and code[i] != code[i + 1]:
            palindrome = code[i:i + 3]
            palindromes.append(palindrome)

    return palindromes


class IPV7:
    REGEXP = re.compile(r'\[[a-z]+\]')

    def __init__(self, ip):
        self.ip = ip

        self.phrases = [phrase for phrase in self.REGEXP.split(ip)]
        self.hypernets = [hypernet for hypernet in self.REGEXP.findall(ip)]

    @property
    def supports_tls(self):
        supports_tls = (
            any([has_abba(phrase) for phrase in self.phrases])
            and not any([has_abba(hypernet) for hypernet in self.hypernets])
        )
        return supports_tls

    @property
    def supports_ssl(self):
        aba_list = [
            aba
            for phrase in self.phrases
            for aba in find_aba(phrase)
        ]

        has_bab = False
        for aba in aba_list:
            bab = '{1}{0}{1}'.format(aba[0], aba[1])

            for hypernet in self.hypernets:
                if bab in hypernet:
                    has_bab = True
                    break

            if has_bab:
                break

        return has_bab


if __name__ == '__main__':
    main()
