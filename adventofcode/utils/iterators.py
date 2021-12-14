# Python Standard Library Imports
import itertools


def pairwise(iterable):
    """Returns successive overlapping pairs taken from the input `iterable`.

    From: https://docs.python.org/3/library/itertools.html#itertools.pairwise

    (Only available in Python >= 3.10)
    """
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)
