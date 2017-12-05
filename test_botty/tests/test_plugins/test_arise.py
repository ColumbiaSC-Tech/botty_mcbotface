from nose.tools import assert_in
from unittest import TestCase
from test_botty.mocks import MockMessage
from botty_mcbotface.plugins.arise import arise, responses


class TestArise(TestCase):
    def setUp(self):
        self.message = MockMessage()

    def tearDown(self):
        del self

    def test_arise(self):
        """Test arise command responses are valid"""
        assert_in(arise(self.message), responses)
