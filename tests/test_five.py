import unittest          # Unittest
import sys               # For version purposes

from log import five     # Module under test


def version_skip(version):
    message = "test only applies to Python {0}".format(version)
    return unittest.skipUnless(sys.version_info[0] == version, message)


class TestFiveShim(unittest.TestCase):

    @version_skip(2)
    def test_string_classes_py2(self):
        self.assertEqual(five.str, basestring)

    @version_skip(3)
    def test_string_classes_py3(self):
        self.assertEqual(five.str, str)

    @version_skip(2)
    def test_is_py2(self):
        self.assertTrue(five.PY2)

    @version_skip(3)
    def test_is_py3(self):
        self.assertTrue(five.PY3)

if __name__ == "__main__":
    unittest.main()