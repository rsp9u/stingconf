import sys


def str_to_type(s):
    t = getattr(sys.modules['builtins'], s, None)
    if isinstance(t, type):
        return t
    else:
        return None


def to_upper_snake(name):
    return name.upper().replace('-', '_')
