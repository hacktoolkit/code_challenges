def ingest(filename, as_groups=False, as_oneline=False):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    if as_groups:
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
    else:
        data = lines

    return data
