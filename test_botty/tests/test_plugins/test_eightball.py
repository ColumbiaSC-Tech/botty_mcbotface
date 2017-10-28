from nose.tools import assert_true, assert_raises
from unittest import TestCase
from test_botty.mocks.mocks import MockMessage
from botty_mcbotface.plugins.eightball import eightball, responses


class TestEightBall(TestCase):
    def setUp(self):
        self.message = MockMessage()

    def tearDown(self):
        del self

    def test_eightball_requires_input(self):
        with assert_raises(TypeError):
            eightball(self.message)

    def test_eightball(self):
        assert_true(eightball(self.message, 'MESSAGE') in responses)
