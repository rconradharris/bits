# Utility functions
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


# Formatter class
class Bitfield(object):
    """
    This class is useful if you'd like to visualize the steps involved in a
    complicated bit-twiddling routine.

    You make each value an instance of Bitfield and after each operation, the
    Bitfield log the intermediate results.
    """
    def __init__(self, val, width=32, overflow=False):
        if isinstance(val, Bitfield):
            other = val
            self.val = other.val
            self.width = other.width
            self.overflow = other.overflow
        else:
            self.val = self._convert_val(val, width, overflow=overflow)
            self.width = width
            self.overflow = overflow

    @classmethod
    def _convert_val(cls, val, width, overflow=False):
        if hasattr(val, 'startswith'):
            if val.startswith('0b'):
                pass
            elif val.startswith('[') and val.endswith(']'):
                val = val.replace('[', '').replace(']', '').replace(' ', '')
            else:
                raise ValueError('Unrecognized binary string')
            val = int(val, 2)
        if overflow:
            if val >= 2 ** width:
                val = val % 2 ** width
            # TODO: do the same wrap around for negative numbers
        else:
            cls._check_overflow(val, width)
        return val

    @classmethod
    def _check_overflow(cls, val, width):
        """Check to see whether a particular value can be represented given this
        width of bits.

        For negative values, we represent the value in two's complement so we know
        exactly how large (in the negative direction) it can be.

        A positive value, however, could be a signed or an unsigned int so we
        assume the latter since it represents more values.

        If it doesn't fit, an OverflowError is raised.
        """
        if val >= 2 ** width:
            raise OverflowError
        if val < -(2 ** (width - 1)):
            raise OverflowError

    def rawstr(self):
        val = self.val
        if val < 0:
            # Two's complement
            val += 2 ** self.width
        sval = ('{:0' + str(self.width) + 'b}').format(val)
        sval = sval[:self.width]
        return sval

    @staticmethod
    def _format_pretty_bit_string(sval, grouping=4, brackets=True):
        """Take a string like 11110000 and make it [1111 0000]"""
        sval = _breakn(sval, grouping)
        if brackets:
            sval = "[{}]".format(sval)
        return sval

    def be(self, grouping=4, brackets=True):
        """Return as string in big-endian format."""
        sval = self.rawstr()
        return self._format_pretty_bit_string(
                sval, grouping=grouping, brackets=brackets)

    def le(self, grouping=4, brackets=True):
        """Return as a string in little-endian format."""
        sval = self.rawstr()
        sval = _reverse_str(sval)
        return self._format_pretty_bit_string(
                sval, grouping=grouping, brackets=brackets)

    def __str__(self):
        """"Return like '[0000 1111 0000 1111]'"""
        return self.be()

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
        sval = '0b' + _invert_bits(self.rawstr())
        result = self.__class__(sval, width=self.width)
        self._log1('~', result)
        return result


# Convenience functions
b4 = lambda x: Bitfield(x, width=4)
b8 = lambda x: Bitfield(x, width=8)
b16 = lambda x: Bitfield(x, width=16)
b32 = lambda x: Bitfield(x, width=32)
b64 = lambda x: Bitfield(x, width=64)
b128 = lambda x: Bitfield(x, width=128)
