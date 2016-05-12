====
bits
====

Simple script so you can play around with bit fields and see the results.

Run 
===

::

    python -i bits.py

Examples
========

::

    >>> b(32)
    '0000 0000 0000 0000 0000 0000 0010 0000'

    >>> b(32 << 1)
    '0000 0000 0000 0000 0000 0000 0100 0000'

    >>> l32(0xffff & 0x1f)
    '1111 1000 0000 0000 0000 0000 0000 0000'

Docs
====

b32 prints a 32 bit value in big-endian format
l32 prints a 32 bit value in little-endian format

Strings are broken up into groups of 4 to help translation to and from
hexadecimal.
