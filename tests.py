import unittest

from bits import *


class BaseTestCase(unittest.TestCase):
    def assertResult(self, expected, val):
        self.assertEqual(expected, str(val))


class BitfieldTestCase(BaseTestCase):
    def test_positive_overflow(self):
        self.assertResult('[0000]', Bitfield(16, width=4, overflow=True))

    def test_negative_overflow(self):
        self.assertResult('[0111]', Bitfield(-9, width=4, overflow=True))


class b4TestCase(BaseTestCase):
    def test_zero(self):
        self.assertResult('[0000]', b4(0))

    def test_positive_int(self):
        self.assertResult('[0001]', b4(1))

    def test_negative_int(self):
        self.assertResult('[1111]', b4(-1))
        self.assertResult('[1110]', b4(-2))
        self.assertResult('[1101]', b4(-3))
        self.assertResult('[1000]', b4(-8))
        with self.assertRaises(OverflowError):
            b4(-9)

    def test_hex_input(self):
        self.assertResult('[1111]', b4(0xf))

    def test_overflow(self):
        with self.assertRaises(OverflowError):
            b4(16)

    def test_str(self):
        self.assertResult('[0000]', b4(0))
        self.assertResult('[0001]', b4(1))

    def test_from_binary_0b_style(self):
        """'0b0001' is Python's style"""
        self.assertResult('[0001]', b4('0b0001'))
        with self.assertRaises(OverflowError):
            b4('0b10001')

    def test_from_binary_bits_style(self):
        """[0001] is bitsstyle, it should round-trip"""
        self.assertResult('[0001]', b4('[0001]'))

    def test_from_other_bitfield(self):
        self.assertResult('[0001]', b4(b4('[0001]')))


class b8TestCase(BaseTestCase):
    def test_positive_int(self):
        self.assertResult('[0001 0000]', b8(16))

    def test_from_binary_bits_style(self):
        """[0001 0000] is bitsstyle, it should round-trip"""
        self.assertResult('[0001 0000]', b8('[0001 0000]'))


class OperatorTestCase(BaseTestCase):
    def test_and(self):
        self.assertResult('[0000]', b4('[0101]') & b4('[1010]'))

    def test_or(self):
        self.assertResult('[1111]', b4('[0101]') | b4('[1010]'))

    def test_xor(self):
        self.assertResult('[0000]', b4('[0000]') ^ b4('[0000]'))
        self.assertResult('[0000]', b4('[1111]') ^ b4('[1111]'))
        self.assertResult('[1010]', b4('[0000]') ^ b4('[1010]'))

    def test_rshift(self):
        self.assertResult('[0001]', b4('[0010]') >> 1)
        self.assertResult('[0000]', b4('[0010]') >> 2)

    def test_lshift(self):
        self.assertResult('[0010]', b4('[0001]') << 1)
        self.assertResult('[0100]', b4('[0001]') << 2)
        self.assertResult('[0000]', b4('[1000]') << 1)

    def test_invert(self):
        self.assertResult('[1111]', ~b4('[0000]'))
        self.assertResult('[0000]', ~b4('[1111]'))
        self.assertResult('[1010]', ~b4('[0101]'))
