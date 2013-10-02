import unittest          # Unittest

import log               # Module under test


class TestLevelFunction(unittest.TestCase):
    """
    Testing the log.level() function.
    """

    def test_returnsfunc(self):
        """
        Ensure that log.level() returns a function.
        """
        self.assertTrue(callable(log.level(4)))
        self.assertTrue(callable(log.level("INFO")))

    def test_filter(self):
        """
        Test that the filter returned by log.level works on
        strings and numbers.
        """
        filtr = log.level("INFO")

        self.assertTrue(filtr("INFO"))
        self.assertFalse(filtr("DEBUG"))
        self.assertTrue(filtr("ERROR"))

        self.assertTrue(filtr(20))
        self.assertFalse(filtr(4))
        self.assertTrue(filtr(100))

        filtr2 = log.level(25)
        self.assertTrue(filtr2("NOTICE"))
        self.assertFalse(filtr2("DEBUG"))
        self.assertTrue(filtr2("ERROR"))

        self.assertTrue(filtr2(25))
        self.assertFalse(filtr2(4))
        self.assertTrue(filtr2(100))
