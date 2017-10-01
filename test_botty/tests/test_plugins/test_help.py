from unittest import TestCase
from test_botty.mocks.mocks import MockMessage
from botty_mcbotface.plugins.help import help, help_msg


class TestHelp(TestCase):
    def setUp(self):
        self.message = MockMessage()

    def tearDown(self):
        del self

    def test_arise(self):
        self.assertTrue(help(self.message) in help_msg)
