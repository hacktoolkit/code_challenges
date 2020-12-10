# Python Standard Library Imports
import json


def ingest(filename, as_json=False, as_groups=False, as_oneline=False, as_table=False, cell_func=None):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    if as_json:
        data = json.loads(''.join(lines))
    elif as_groups:
        data = []

        group = None
        for line in lines:
            if group is None:
                group = []
            if line:
                group.append(line)
            else:
                data.append(group)
                group = None

        if group:
            data.append(group)
    elif as_oneline:
        data = ''.join(lines)
    elif as_table:
        data = []

        for line in lines:
            cells = list(filter(lambda x: x is not None, line.split()))

            if cell_func:
                cells = [cell_func(value) for value in cells]

            data.append(cells)
    else:
        data = lines

    return data
