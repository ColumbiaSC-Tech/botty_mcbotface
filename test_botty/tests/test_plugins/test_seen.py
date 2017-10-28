import warnings
from nose.tools import assert_in
from unittest import TestCase
from unittest.mock import patch
from test_botty.mocks.mocks import MockMessage, Response
from botty_mcbotface.plugins.seen import seen

# Short-circuit Message object that just returns results
mock_message = MockMessage()

# TODO: Finish


class TestSearches(TestCase):
    def setUp(self):

        # lxml module throws warnings only relevant in production
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=ResourceWarning)

    def tearDown(self):
        del self

    def test_seen_handle_not_a_user_name(self):
        """Test seen command handles when the searched username is invalid"""
        response = seen(mock_message, 'SHOULD NOT MATCH')
        assert_in('Did you search with a username?', response)

    # @patch('botty_mcbotface.botty.api.')
    # def test_seen_find_last_message_by_user(self):
    #     pass
