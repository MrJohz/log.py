import unittest          # Unittest

import log               # Module under test


class TestHelperFunctions(unittest.TestCase):

    def test_isiterable(self):
        # list?
        self.assertTrue(log._isiterable([]))

        # generator?
        self.assertTrue(log._isiterable((i for i in [])))

        # string?
        self.assertTrue(log._isiterable('string'))

        # number?
        self.assertFalse(log._isiterable(5))

    def test_get_list(self):
        # for iterable?
        self.assertEqual(log._get_list((1, 2)), [1, 2])

        # for non-iterable?
        self.assertEqual(log._get_list(5), [5])

    def test_if_none(self):
        # default sentinel
        self.assertEqual(log._if_none(None, list), [])
        self.assertEqual(log._if_none(45, list), 45)

        # custom sentinel
        sentinel = object()
        self.assertEqual(log._if_none(sentinel, list, sentinel), [])
        self.assertEqual(log._if_none(None, list, sentinel), None)
        self.assertEqual(log._if_none(5, list, sentinel), 5)


if __name__ == "__main__":
    unittest.main()
