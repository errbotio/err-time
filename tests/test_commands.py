# coding=utf-8
from errbot.backends.test import FullStackTest, popMessage


class TestCommands(FullStackTest):
    @classmethod
    def setUpClass(cls, extra=None):
        super(TestCommands, cls).setUpClass(__file__)

    def test_tzlist(self):
        self.assertCommand('!tzlist', 'New York')

    def test_time(self):
        self.assertCommand('!time new york', 'Current time in America/New_York : ')
