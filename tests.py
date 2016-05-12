import unittest

from bits import *


class b4TestCase(unittest.TestCase):
    def test_zero(self):
        self.assertEqual('[0000]', b4(0))

    def test_positive_int(self):
        self.assertEqual('[0001]', b4(1))

    def test_hex(self):
        self.assertEqual('[1111]', b4(0xf))

    def test_overflow(self):
        with self.assertRaises(OverflowError):
            b4(16)


class b8TestCase(unittest.TestCase):
    def test_positive_int(self):
        self.assertEqual('[0001 0000]', b8(16))


class l4TestCase(unittest.TestCase):
    def test_positive_int(self):
        self.assertEqual('[1000]', l4(1))


class bf4TestCase(unittest.TestCase):
    def test_str(self):
        self.assertEqual('[0000]', str(bf4(0)))
        self.assertEqual('[0001]', str(bf4(1)))

    def test_from_binary_0b_style(self):
        """'0b0001' is Python's style"""
        self.assertEqual('[0001]', str(bf4('0b0001')))
        with self.assertRaises(OverflowError):
            bf4('0b10001')

    def test_from_binary_bits_style(self):
        """[0001] is bitsstyle, it should round-trip"""
        self.assertEqual('[0001]', str(bf4('[0001]')))


class bf8TestCase(unittest.TestCase):
    def test_from_binary_bits_style(self):
        """[0001 0000] is bitsstyle, it should round-trip"""
        self.assertEqual('[0001 0000]', str(bf8('[0001 0000]')))


class OperatorTestCase(unittest.TestCase):
    def test_and(self):
        self.assertEqual('[0000]', str(bf4('[0101]') & bf4('[1010]')))

    def test_or(self):
        self.assertEqual('[1111]', str(bf4('[0101]') | bf4('[1010]')))

    def test_xor(self):
        self.assertEqual('[0000]', str(bf4('[0000]') ^ bf4('[0000]')))
        self.assertEqual('[0000]', str(bf4('[1111]') ^ bf4('[1111]')))
        self.assertEqual('[1010]', str(bf4('[0000]') ^ bf4('[1010]')))

    def test_rshift(self):
        self.assertEqual('[0001]', str(bf4('[0010]') >> 1))
        self.assertEqual('[0000]', str(bf4('[0010]') >> 2))

    def test_lshift(self):
        self.assertEqual('[0010]', str(bf4('[0001]') << 1))
        self.assertEqual('[0100]', str(bf4('[0001]') << 2))
        self.assertEqual('[0000]', str(bf4('[1000]') << 1))

    def test_invert(self):
        self.assertEqual('[1111]', str(~bf4('[0000]')))
        self.assertEqual('[0000]', str(~bf4('[1111]')))
        self.assertEqual('[1010]', str(~bf4('[0101]')))
