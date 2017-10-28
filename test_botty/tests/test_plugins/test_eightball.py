from nose.tools import assert_in, assert_raises
from unittest import TestCase
from test_botty.mocks.mocks import MockMessage
from botty_mcbotface.plugins.eightball import eightball, responses


class TestEightBall(TestCase):
    def setUp(self):
        self.message = MockMessage()

    def tearDown(self):
        del self

    def test_eightball_requires_input(self):
        """Test eightball raises TypeError when no input given"""
        with assert_raises(TypeError):
            eightball(self.message)

    def test_eightball(self):
        """Test eightball command responses are valid"""
        assert_in(eightball(self.message, 'MESSAGE'), responses)
