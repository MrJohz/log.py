import unittest          # Unittest

import log               # Module under test


class TestLogger(unittest.TestCase):

    def test_creating_same(self):
        self.assertIs(log.Logger('hello'), log.Logger('hello'))

    def test_creating_different(self):
        self.assertIsNot(log.Logger('hello'), log.Logger('goodbye'))

    @unittest.skip("Haven't implemented this yet.")
    def test_creating_default(self):
        self.assertIsNot(log.Logger(), log.Logger())