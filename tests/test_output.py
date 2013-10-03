import unittest          # Unittest

from log import five
import re

import log               # Module under test


class TestOutputs(unittest.TestCase):

    def setUp(self):
        self.message1 = log.Message('TAGGED: \'test\'',
                                    level='INFO', tags=['test'])
        self.message2 = log.Message('TAGGED: \'test\', \'notest\'',
                                    level='INFO', tags=['test', 'notest'])
        self.message3 = log.Message('NO TAGS', level=17)
        self.messages = [self.message1, self.message2, self.message3]

    def test_filter(self):
        # DAMN YOU PY3!
        if five.PY3:
            self.assertItemsEqual = self.assertCountEqual

        # should accept all messages
        output1 = log.Output(five.cStringIO())

        # should deny all messages
        output2 = log.Output(five.cStringIO(),
                             filter=lambda x: False)

        output3 = log.Output(five.cStringIO(),
                             filter=lambda x: 'test' in x.tags)
        output4 = log.Output(five.cStringIO(),
                             filter=lambda x: 'test' not in x.tags)

        self.assertEqual(
            len(list(filter(output1.check_valid, self.messages))), 3)
        self.assertEqual(
            len(list(filter(output2.check_valid, self.messages))), 0)
        self.assertItemsEqual(
            list(filter(output3.check_valid, self.messages)),
            [self.message1, self.message2])
        self.assertItemsEqual(
            list(filter(output4.check_valid, self.messages)), [self.message3])

    def test_filters(self):
        if five.PY3:
            self.assertItemsEqual = self.assertCountEqual

        # Should refuse all messages
        output1 = log.Output(
            five.cStringIO(), filters=[lambda x: False, lambda x: True])

        self.assertEqual(
            len(list(filter(output1.check_valid, self.messages))), 0)

    def test_writing(self):
        op = five.cStringIO()
        output = log.Output(op)
        output.write(self.message1)

        message = r"\[.*?\] {level}: {message}".format(
            level=self.message1.level, message=self.message1.message)
        error = op.getvalue() + " != " + message
        self.assertTrue(re.match(message, op.getvalue()), error)
                        # I can't work out a cross-platform regexpMatches()
