# coding=utf-8
from errbot.backends.test import FullStackTest, popMessage


class TestCommands(FullStackTest):

    def test_tzlist(self):
        self.assertCommand('!tzlist', 'New York')

    def test_time(self):
        self.assertCommand('!time new york', 'Current time in America/New_York : ')
