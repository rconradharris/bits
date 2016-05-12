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


# Formatter class
class Bitfield(object):
    """
    This class is useful if you'd like to visualize the steps involved in a
    complicated bit-twiddling routine.

    You make each value an instance of Bitfield and after each operation, the
    Bitfield log the intermediate results.
    """
    def __init__(self, val, width=32):
        if hasattr(val, 'startswith') and val.startswith('0b'):
            self.val = int(val, 2)
        else:
            self.val = val
        self.width = width

    def as_raw_str(self):
        """"Return like '0000111100001111'"""
        # 99999 for our purposes is maxint
        return _format_be(self.val, width=self.width, grouping=999999)

    def __str__(self):
        """"Return like '[0000 1111 0000 1111]'"""
        return "[{}]".format(_format_be(self.val, width=self.width))

    __repr__ = __str__

    def _check_width(self, other):
        if not isinstance(other, Bitfield):
            raise ValueError('operand is not a Bitfield instance')
        if self.width != other.width:
            raise ValueError('bit widths do not match')
        return self.width


    def _print_line(self, key, value):
        key = key.ljust(16)
        print(": ".join([key, value]))

    def _log1(self, operator, result):
        self._print_line('Operand', str(self))
        self._print_line(operator, str(result))
        print('')

    def _log2(self, other, operator, result):
        self._print_line('Left', str(self))
        self._print_line('Right', str(other))
        self._print_line(operator, str(result))
        print('')

    def _make_result(self, other, width, operator, val):
        result = self.__class__(val, width=width)
        self._log2(other, operator, result)
        return result

    def __and__(self, other):
        width = self._check_width(other)
        return self._make_result(other, width, '&', self.val & other.val)

    def __or__(self, other):
        width = self._check_width(other)
        return self._make_result(other, width, '|', self.val | other.val)

    def __xor__(self, other):
        width = self._check_width(other)
        return self._make_result(other, width, '^', self.val ^ other.val)

    def __lshift__(self, other):
        if isinstance(other, Bitfield):
            raise ValueError('Bitfield is not a valid right operand')
        return self._make_result(other, self.width, '<<', self.val << other)

    def __rshift__(self, other):
        if isinstance(other, Bitfield):
            raise ValueError('Bitfield is not a valid right operand')
        return self._make_result(other, self.width, '>>', self.val >> other)

    def __invert__(self):
        sval = '0b' + self.as_raw_str()\
                          .replace('0', 'x')\
                          .replace('1', '0')\
                          .replace('x', '1')
        result = self.__class__(sval, width=self.width)
        self._log1('~', result)
        return result


bf4 = lambda x: Bitfield(x, width=4444)
bf8 = lambda x: Bitfield(x, width=8)
bf16 = lambda x: Bitfield(x, width=16)
bf32 = lambda x: Bitfield(x, width=32)
bf64 = lambda x: Bitfield(x, width=64)
bf128 = lambda x: Bitfield(x, width=128)
bf = bf32

# Tests
#print ~(bf(0) | bf(1))
