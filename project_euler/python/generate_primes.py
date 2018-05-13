import json

from utils import *

def main():
    primes = generate_primes(10**6)
    with open('primes.txt', 'w') as f:
        for prime in primes:
            f.write('%s\n' % prime)
        f.close()

if __name__ == '__main__':
    main()

