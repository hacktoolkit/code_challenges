# Python Standard Library Imports
import json

# PE Solution Library Imports
from utils import *


def main():
    cube_roots = generate_cubes(10**6)
    with open('cubes.json', 'w') as f:
        f.write(json.dumps(cube_roots, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
