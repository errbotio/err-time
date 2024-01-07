# coding=utf-8
from errbot.backends.test import testbot


class TestTimeBot:
    extra_plugin_dir = "."

    def test_tzlist(self, testbot):
        testbot.push_message("!tzlist")
        assert "New York" in testbot.pop_message()

    def test_time(self, testbot):
        testbot.push_message("!time new york")
        assert "Current time in America/New_York: " in testbot.pop_message()

    def test_time_not_found(self, testbot):
        testbot.push_message("!time new errbot")
        assert "cannot find this city" in testbot.pop_message()
