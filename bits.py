def _splitn(s, n):
    """Split a string into substrings of size at most n"""
    return [s[i:i+n] for i in range(0, len(s), n)]


def _breakn(s, n, char=' '):
    """Insert a character between every n characters of a string."""
    return char.join(_splitn(s, n))


def _reverse_str(s):
    return s[::-1]


def _format_be(x, width=32, grouping=4):
    """Format a number in base 2 using big-endian represpentation.
    This number is 32 bits wide.
    """
    return _breakn(('{:0' + str(width) + 'b}').format(x), grouping)


def _format_le(x, width=32, grouping=4):
    """Little-endian 32-bit value"""
    return _reverse_str(_format_be(x, width=width, grouping=grouping))


# Big endian
b4 = lambda x: _format_be(x, width=4)
b8 = lambda x: _format_be(x, width=8)
b16 = lambda x: _format_be(x, width=16)
b32 = lambda x: _format_be(x, width=32)
b64 = lambda x: _format_be(x, width=64)
b128 = lambda x: _format_be(x, width=128)
b = b32

# Little endian
l4 = lambda x: _format_le(x, width=4)
l8 = lambda x: _format_le(x, width=8)
l16 = lambda x: _format_le(x, width=16)
l32 = lambda x: _format_le(x, width=32)
l64 = lambda x: _format_le(x, width=64)
l128 = lambda x: _format_be(x, width=128)
l = l32
