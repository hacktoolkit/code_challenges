# Python Standard Library Imports
import argparse
import os

# Third Party (PyPI) Imports
import requests
from dotenv import load_dotenv


load_dotenv()


SESSION = os.environ.get('SESSION')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('day', type=int)
    args = parser.parse_args()

    download_input(args.day)


def download_input(day):
    year = os.path.dirname(__file__).rsplit('/', 1)[-1]
    url = f'https://adventofcode.com/{year}/day/{day}/input'

    cookies = {
        'session': SESSION,
    }
    response = requests.get(url, cookies=cookies)
    filename = f'{str(day).zfill(2)}.in'
    with open(filename, 'w') as f:
        f.write(response.content.decode())


if __name__ == '__main__':
    main()
