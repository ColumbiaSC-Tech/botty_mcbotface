from nose.tools import assert_in
from unittest import TestCase
from test_botty.mocks import MockMessage
from botty_mcbotface.plugins.help import help, help_msg


class TestHelp(TestCase):
    def setUp(self):
        self.message = MockMessage()

    def tearDown(self):
        del self

    def test_arise(self):
        """Test help command response is valid"""
        assert_in(help(self.message), help_msg)
