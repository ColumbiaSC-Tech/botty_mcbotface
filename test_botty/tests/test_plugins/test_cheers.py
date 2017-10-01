from unittest import TestCase
from test_botty.mocks.mocks import MockMessage
from botty_mcbotface.plugins.cheers import cheers, responses


class TestCheers(TestCase):
    def setUp(self):
        self.message = MockMessage()

    def tearDown(self):
        del self

    def test_cheers(self):
        self.assertTrue(cheers(self.message) in responses)
