# Python Standard Library Imports
import json

# PE Solution Library Imports
from utils import *


def main():
    primes = generate_primes(10**7)
    with open('primes.txt', 'w') as f:
        for prime in primes:
            f.write('%s\n' % prime)
        f.close()

if __name__ == '__main__':
    main()
