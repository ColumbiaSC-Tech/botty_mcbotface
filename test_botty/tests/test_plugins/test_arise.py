from nose.tools import assert_true
from unittest import TestCase
from test_botty.mocks.mocks import MockMessage
from botty_mcbotface.plugins.arise import arise, responses


class TestArise(TestCase):
    def setUp(self):
        self.message = MockMessage()

    def tearDown(self):
        del self

    def test_arise(self):
        assert_true(arise(self.message) in responses)
