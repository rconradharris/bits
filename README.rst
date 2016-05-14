====
bits
====

Python script that lets you play around with bit fields and see the results.

Run 
===

::

    python -i bits.py

Examples
========

The ``Bitfield`` class is what performs the bitwise operations and
pretty-prints the results.

Convenience functions exists for common sizes, like a nibble (``b4``), byte
(``b8``), 16-bit word (``b16``), 32-bit doubleword (``b32``), a 64-bit
quadword (``b64``), and 128-bit double quadword (``b128``).

::

    >>> ((~b32(0x32)) | b32(0x63)) ^ b32(0x22)
    Operand         : [0000 0000 0000 0000 0000 0000 0011 0010]
    ~               : [1111 1111 1111 1111 1111 1111 1100 1101]

    Left            : [1111 1111 1111 1111 1111 1111 1100 1101]
    Right           : [0000 0000 0000 0000 0000 0000 0110 0011]
    |               : [1111 1111 1111 1111 1111 1111 1110 1111]

    Left            : [1111 1111 1111 1111 1111 1111 1110 1111]
    Right           : [0000 0000 0000 0000 0000 0000 0010 0010]
    ^               : [1111 1111 1111 1111 1111 1111 1100 1101]

    [1111 1111 1111 1111 1111 1111 1100 1101]


Operations
==========

* AND (``&``)
* OR (``|``)
* XOR (``^``)
* NOT (``~``)
* LEFT SHIFT (``<<``)
* RIGHT SHIFT (``>>``); zero-fill


Ways to specify a value
=======================

A variety of different data-types can be used as input values for the
``Bitfield`` class including:

* Decimal (base 10)::

    >>> b4(3)
    [0011]

* Hexadecimal (base 16)::

    >>> b4(0xa)
    [1010]

* Octal (base 8)::

    >>> b4(011)
    [1001]

* Binary, Python format (base 2)::

    >>> b4(0b0110)
    [0110]

* Binary, bits string format (base 2)::

    >>> b8('[0001 1010]')
    [0001 1010]

* Negative decimal yielding two's complement::

    >>> b4(-6)
    [1010]
