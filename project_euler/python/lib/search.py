def binary_search(items, value, exact=True, ascending=True, initial_guess=None):
    """Performs binary search for an item matching `value`
    in a list of `items`.

    Finds an exact match if `exact is True`, else as close as possible without crossing `value`
    `items` sorted in ascending order if `ascending is True`

    Optionally takes in `initial_guess`, an index `k` between
    `0 <= k <= len(items)`

    Returns the `index` of the matching item

    Test Cases:
    - 745
    """
    index = None
    lower = 0
    upper = len(items) - 1

    def _update_guess():
        return int((lower + upper) / 2.0)

    if initial_guess is not None:
        k = initial_guess
    else:
        k = _update_guess()

    while index is None and lower <= upper:
        # loop until item is found, or lower cross upper
        item = items[k]
        next_item = items[k + 1] if k + 1 < len(items) else None

        if exact:
            criteria = item == value
        elif ascending:
            criteria = (
                item <= value
                and (
                    next_item is None
                    or next_item > value
                )
            )
        else:
            # `items` are in descending order
            criteria = (
                item >= value
                and (
                    next_item is None
                    or next_item < value
                )
            )

        if criteria:
            index = k
        elif ascending:
            if item > value:
                upper = k - 1
                k = _update_guess()
            elif item < value:
                lower = k + 1
                k = _update_guess()
        else:
            # `items` are in descending order
            if item < value:
                upper = k - 1
                k = _update_guess()
            elif item > value:
                lower = k + 1
                k = _update_guess()

    return index
