"""
sample test file

"""

from django.test import SimpleTestCase

from app import calc


class CalcTests(SimpleTestCase):

    def test_add(self):

        res = calc.add(3, 11)

        self.assertEqual(res, 14)

    def test_subtract(self):

        res = calc.subtract(5, 11)

        self.assertEqual(res, 6)
