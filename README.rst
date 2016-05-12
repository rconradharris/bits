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
