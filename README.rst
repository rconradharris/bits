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

Simple formatting can be done with the ``b()`` and `l()`` series of functions
which print the results in big-endian and little-endian format respectively.

::

    >>> b(32)
    '[0000 0000 0000 0000 0000 0000 0010 0000]'

    >>> b(32 << 1)
    '[0000 0000 0000 0000 0000 0000 0100 0000]'

    >>> l32(0xffff & 0x1f)
    '[1111 1000 0000 0000 0000 0000 0000 0000]'

You can also use the ``Bitfield`` class, aliased as ``bf()`` to evaluate
complex expressions and see the intermediate results.

::

    >>> ((~bf(0x32)) | bf(0x63)) ^ bf(0x22)
    Operand         : [0000 0000 0000 0000 0000 0000 0011 0010]
    ~               : [1111 1111 1111 1111 1111 1111 1100 1101]

    Left            : [1111 1111 1111 1111 1111 1111 1100 1101]
    Right           : [0000 0000 0000 0000 0000 0000 0110 0011]
    |               : [1111 1111 1111 1111 1111 1111 1110 1111]

    Left            : [1111 1111 1111 1111 1111 1111 1110 1111]
    Right           : [0000 0000 0000 0000 0000 0000 0010 0010]
    ^               : [1111 1111 1111 1111 1111 1111 1100 1101]

    [1111 1111 1111 1111 1111 1111 1100 1101]
