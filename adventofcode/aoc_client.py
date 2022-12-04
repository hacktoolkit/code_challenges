# Python Standard Library Imports
import argparse
import datetime
import os

# Third Party (PyPI) Imports
import click
import markdownify
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()


SESSION = os.environ.get('SESSION')


DEFAULT_YEAR = os.path.dirname(__file__).rsplit('/', 1)[-1]
DEFAULT_DAY = datetime.datetime.now().day


@click.command()
@click.option('-y', '--year', default=DEFAULT_YEAR)
@click.option('-d', '--day', default=DEFAULT_DAY)
@click.option(
    '-t',
    '--type',
    type=click.Choice(['puzzle', 'input', 'answer']),
    default='puzzle',
)
@click.option('-s', '--save', default=False, is_flag=True)
@click.option('-p', '--part', type=click.IntRange(1, 2))
@click.option('-a', '--answer', is_flag=False, default=None)
def main(year, day, type, save, part, answer):
    cli = AOCClient(year, day)
    if type == 'puzzle':
        cli.download_puzzle(save=save)
    elif type == 'input':
        cli.download_input(save=save)
    elif type == 'answer':
        if part is None:
            raise Exception(
                'Please specify a which part to submit an answer for.'
            )
        if answer is None:
            raise Exception('Please specify answer')

        cli.submit_answer(part, answer)
    else:
        raise Exception(f'Unknown type: {type}')


class AOCClient:
    def __init__(self, year=None, day=None, save=False):
        if year is None:
            year = DEFAULT_YEAR

        if day is None:
            day = DEFAULT_DAY

        self.year = year
        self.day = day
        self.save = save

    @property
    def cookies(self):
        cookies = {
            'session': SESSION,
        }
        return cookies

    @property
    def puzzle_url(self):
        url = f'https://adventofcode.com/{self.year}/day/{self.day}'
        return url

    @property
    def input_url(self):
        url = f'https://adventofcode.com/{self.year}/day/{self.day}/input'
        return url

    @property
    def submit_url(self):
        url = f'https://adventofcode.com/{self.year}/day/{self.day}/answer'
        return url

    def get(self, url):
        response = requests.get(url, cookies=self.cookies)
        return response

    def make_filename(self, extension):
        filename = f'{str(self.day).zfill(2)}.{extension}'
        return filename

    @property
    def puzzle_filename(self):
        return self.make_filename('md')

    @property
    def input_filename(self):
        return self.make_filename('in')

    def download_puzzle(self, save=False):
        response = self.get(self.puzzle_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        content = markdownify.markdownify(str(soup.main))

        if save:
            with open(self.puzzle_filename, 'w') as f:
                f.write(content)
        else:
            print(content)

    def download_input(self, save=False):
        response = self.get(self.input_url)
        content = response.content.decode()

        if save:
            with open(self.input_filename, 'w') as f:
                f.write(content)
        else:
            print(content)

    def submit_answer(self, part, answer):
        data = {
            'level': part,
            'answer': answer,
        }
        response = requests.post(
            self.submit_url, cookies=self.cookies, data=data
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        content = soup.main.get_text()
        print(content)


if __name__ == '__main__':
    main()
