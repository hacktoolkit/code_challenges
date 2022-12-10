class CRT:
    WIDTH = 8
    HEIGHT = 1

    def __init__(self):
        self.WIDTH_PIXELS = (Font.WIDTH + 1) * self.WIDTH
        self.HEIGHT_PIXELS = (Font.HEIGHT + 1) * self.HEIGHT

        self.pixels = [
            ['.' for col in range(self.WIDTH_PIXELS)]
            for row in range(self.HEIGHT_PIXELS)
        ]

    def pixel_draw(self, row, col, c):
        try:
            self.pixels[row][col] = c
        except IndexError:
            raise Exception(f'Invalid pixel: ({row},{col})')

    def pixel_on(self, row, col):
        self.pixel_draw(row, col, '#')

    def pixel_off(self, row, col):
        self.pixel_draw(row, col, '.')

    def render(self):
        rendered = '\n'.join([''.join(row) for row in self.pixels])
        return rendered

    def read_characters(self):
        chars = []
        for char in range(self.WIDTH):
            chars.append(self.read_character(char))

        s = ''.join(chars)
        return s

    def read_character(self, n, missing='-'):
        rendered_letter = '\n'.join(
            [
                ''.join(
                    self.pixels[y][x]
                    for x in range(
                        n + n * Font.WIDTH,
                        n + n * Font.WIDTH + Font.WIDTH,
                    )
                )
                for y in range(Font.HEIGHT)
            ]
        )

        detected_char = Font.LETTER_MAP.get(rendered_letter)
        if detected_char is None:
            # Uncomment to show broken mapping as one line
            # Font.LETTER_MAP[rendered_letter]
            print(f'Missing font mapping for:\n{rendered_letter}')

        char = detected_char or missing
        return char

    def load_rendered(self, s):
        for y, row in enumerate(s.split()):
            if y >= self.HEIGHT_PIXELS:
                break

            for x, c in enumerate(row):
                if x >= self.WIDTH_PIXELS:
                    break

                if c == '#':
                    self.pixel_on(y, x)
                else:
                    self.pixel_off(y, x)


class Font:
    WIDTH = 4
    HEIGHT = 6

    LETTERS = {
        'A': '.##.\n#..#\n#..#\n####\n#..#\n#..#',
        'B': '###.\n#..#\n###.\n#..#\n#..#\n###.',
        'C': '.##.\n#..#\n#...\n#...\n#..#\n.##.',
        'D': None,
        'E': None,
        'F': '####\n#...\n###.\n#...\n#...\n#...',
        'G': None,
        'H': None,
        'I': None,
        'J': '..##\n...#\n...#\n...#\n#..#\n.##.',
        'K': '#..#\n#.#.\n##..\n#.#.\n#.#.\n#..#',
        'L': None,
        'M': None,
        'N': None,
        'O': '.##.\n#..#\n#..#\n#..#\n#..#\n.##.',
        'P': '###.\n#..#\n#..#\n###.\n#...\n#...',
        'Q': '.##.\n#..#\n#..#\n#..#\n#.##\n.###',  # TODO: verify
        'R': None,
        'S': None,
        'T': None,
        'U': None,
        'V': None,
        'W': None,
        'Y': None,
        'Z': '####\n...#\n..#.\n.#..\n#...\n####',
    }

    LETTER_MAP = {rendered: letter for letter, rendered in LETTERS.items()}
