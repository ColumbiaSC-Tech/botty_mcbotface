import os
import warnings
from nose.tools import assert_equals, assert_in, assert_true
from unittest import TestCase
from unittest.mock import patch
from test_botty.mocks.mocks import MockMessage, Response
from botty_mcbotface.plugins.searches import google, youtube

# Short-circuit Message object that just returns results
mock_message = MockMessage()


class TestSearches(TestCase):
    def setUp(self):

        # lxml module throws warnings only relevant in production
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=ResourceWarning)

    def tearDown(self):
        del self

    @patch('requests.get')
    def test_google_search(self, mock_get_html):
        """Test google search retrieves first search result from google"""

        # Path to mock link results data
        curr_dir = os.path.dirname(__file__)
        rel_path = '../../mocks/google_links.html'
        html_path = os.path.join(curr_dir, rel_path)

        mock_response = Response(html_path)
        mock_get_html.return_value = mock_response

        # Call main method
        first_result = google(mock_message, 'testing')

        assert_equals('http://istqbexamcertification.com/what-is-software-testing/', first_result)

    @patch('requests.get')
    def test_youtube_search(self, mock_get_html):
        """Test youtube search retrieves first search result from youtube"""

        # Path to mock link results data
        curr_dir = os.path.dirname(__file__)
        rel_path = '../../mocks/youtube_links.html'
        html_path = os.path.join(curr_dir, rel_path)

        mock_get_html.return_value = Response(html_path)

        # Call main method
        first_result = youtube(mock_message, 'testing')

        assert_in('https://www.youtube.com/watch?v=Bi-v6M4fGbA', first_result)

    @patch('requests.get')
    def test_google_search_handles_no_results(self, mock_get_html):
        """Test google search command can handle no search results"""
        mock_get_html.return_value.text = ''
        response = google(mock_message, 'testing')

        assert_true('No Google results', response)

    @patch('requests.get')
    def test_youtube_search_handles_no_results(self, mock_get_html):
        """Test youtube search command can handle no search results"""
        mock_get_html.return_value.text = ''
        response = youtube(mock_message, 'testing')

        assert_true('No YouTube results', response)
