def _splitn(s, n):
    """Split a string into substrings of size at most n"""
    return [s[i:i+n] for i in range(0, len(s), n)]


def _breakn(s, n, char=' '):
    """Insert a character between every n characters of a string."""
    if n is None:
        return s
    return char.join(_splitn(s, n))


def _reverse_str(s):
    """Return a string in reversed order."""
    return s[::-1]


def _invert_bits(s):
    """Return string with all 0s turned into 1s and vice versa."""
    parts = []
    for c in s:
        if c == '0':
            c = '1'
        elif c == '1':
            c = '0'
        parts.append(c)
    return ''.join(parts)


def _format_be(x, width=32, grouping=4, brackets=True, overflow=False):
    """Format big-endian"""
    if x >= 2 ** width and not overflow:
        raise OverflowError
    sval = ('{:0' + str(width) + 'b}').format(x)
    sval = sval[:width]
    sval = _breakn(sval, grouping)
    if brackets:
        sval = "[{}]".format(sval)
    return sval


def _format_le(x, width=32, grouping=4, brackets=True, overflow=False):
    """Format little-endian"""
    sval = _format_be(x, width=width, grouping=grouping, brackets=False,
                      overflow=overflow)
    sval = _reverse_str(sval)
    if brackets:
        sval = "[{}]".format(sval)
    return sval


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
    def __init__(self, val, width=32, overflow=False):
        self.val = self._convert_val(val, width, overflow=overflow)
        self.width = width

    @staticmethod
    def _convert_val(val, width, overflow=False):
        if hasattr(val, 'startswith'):
            if val.startswith('0b'):
                pass
            elif val.startswith('[') and val.endswith(']'):
                val = val.replace('[', '').replace(']', '').replace(' ', '')
            else:
                raise ValueError('Unrecognized binary string')
            val = int(val, 2)
        if val >= 2 ** width:
            if overflow:
                val = val % 2 ** width
            else:
                raise OverflowError
        return val

    def __str__(self):
        """"Return like '[0000 1111 0000 1111]'"""
        return _format_be(self.val, width=self.width)

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

    def _make_result(self, other, width, operator, val, overflow=False):
        result = self.__class__(val, width=width, overflow=overflow)
        self._log2(other, operator, result)
        return result

    # Binary(Bitfield, Bitfield) operators
    def __and__(self, other):
        width = self._check_width(other)
        return self._make_result(other, width, '&', self.val & other.val)

    def __or__(self, other):
        width = self._check_width(other)
        return self._make_result(other, width, '|', self.val | other.val)

    def __xor__(self, other):
        width = self._check_width(other)
        return self._make_result(other, width, '^', self.val ^ other.val)

    # Binary(Bitfield, int) operators
    def __lshift__(self, other):
        if isinstance(other, Bitfield):
            raise ValueError('Bitfield is not a valid right operand')
        return self._make_result(other, self.width, '<<', self.val << other,
                                 overflow=True)

    def __rshift__(self, other):
        if isinstance(other, Bitfield):
            raise ValueError('Bitfield is not a valid right operand')
        return self._make_result(other, self.width, '>>', self.val >> other)

    # Unary(Bitfield) operators
    def __invert__(self):
        sval = _format_be(self.val, width=self.width, grouping=None,
                          brackets=False)
        sval = _invert_bits(sval)
        sval = '0b' + sval
        result = self.__class__(sval, width=self.width)
        self._log1('~', result)
        return result


bf4 = lambda x: Bitfield(x, width=4)
bf8 = lambda x: Bitfield(x, width=8)
bf16 = lambda x: Bitfield(x, width=16)
bf32 = lambda x: Bitfield(x, width=32)
bf64 = lambda x: Bitfield(x, width=64)
bf128 = lambda x: Bitfield(x, width=128)
bf = bf32
