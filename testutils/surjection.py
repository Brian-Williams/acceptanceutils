"""
Minimal surjective tools for testing.

For everywhere in this file surjective/surjection implies the minimally required number of mappings to be considered
surjective.

The primary use of these tools is when you want to test many options, but don't have the time to test every combination
of said options.

Wrote specifically for a test that had >20 options with several valid parameters for each option. Running every
combination in smoke testing took too long. This provides acceptable general coverage for most smoke tests. I would
strongly suggest any set of release tests does not use these tools unless absolutely required.
"""
from __future__ import absolute_import
from itertools import chain, repeat
import random
# try:
#     from itertools import izip_longest as zip_longest
# except ImportError:
#     from itertools import zip_longest


class NonLocals(object):
    """
    Helper class to implement nonlocal names in Python 2.x

    You would rewrite this py3 code:
    NL = 8675309
    def inner()
        nonlocal NL
        if NL:
            pass

    As the following py2/3 code:
    NL = NonLocal(c=8675309)
    def inner()
        if NL.c:
            pass
    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class OuterZipStopIteration(Exception):
    pass


def zip_longest_defaults(*args):
    """
    Same logic as zip_longest, but allows fillvalues per item instead of a global fillvalue.

    http://stackoverflow.com/questions/13085861/outerzip-zip-longest-function-with-multiple-fill-values
    """
    count = len(args) - 1
    count = NonLocals(c=count)

    def sentinel(default):
        # nonlocal count
        if not count.c:
            raise OuterZipStopIteration
        count.c -= 1
        yield default

    iters = [chain(p, sentinel(default), repeat(default)) for p, default in args]
    try:
        while iters:
            yield tuple(map(next, iters))
    except OuterZipStopIteration:
        pass


def surjective_options(*options):
    """
    Give several options and return a list of options that includes every option at least once.

    If a test takes a while to complete and it has several options many valid inputs that need to be tested running
    every iteration could extend past a reasonable runtime. This will ensure every option is tested at least once. No
    matter the number of input lists the returned list will be the length of the list with the most parameters.

    :param options: Tuple with (<list>, fill value)
    :return: List of shuffled surjective options
    """
    for p, default in options:
        try:
            random.shuffle(p)
        # allow non-lists to be passed in, this allows direct bindings of certain parameters easily
        # ex. two settings are dependant on each other where it is invalid for both to be False:
        # ((True, False), True), ((False, True), True)
        # The above would never produce a list where both options are False.
        except TypeError:
            pass
    surjective_list = list(zip_longest_defaults(*options))
    return surjective_list
