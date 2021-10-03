import sys
from pprint import pprint


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def epprint(*args, **kwargs):
    pprint(*args, stream=sys.stderr, **kwargs)
