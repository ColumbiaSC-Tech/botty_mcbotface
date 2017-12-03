from unittest import TestCase
from bs4 import BeautifulSoup
from nose.tools import assert_in, assert_true, assert_raises, assert_is_instance
import botty_mcbotface.utils.tools as tools
import os.path
import requests_mock
import warnings


class TestTools(TestCase):
    def setUp(self):

        # lxml module throws warnings only relevant in production
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=ResourceWarning)
        self.test_html = os.path.abspath('test_botty/mocks/google_test.html')

    def tearDown(self):
        del self

    def test_soup_returns_html(self):
        """Test soup utility fn returns a BeautifulSoup object"""
        with open(self.test_html) as html:
            assert_is_instance(tools.soup(html), BeautifulSoup)

    def test_get_html_returns_soup_html(self):
        """Test get_html returns soup html object"""
        with requests_mock.Mocker() as m:
            with open(self.test_html) as html:
                m.get('http://test.com', text=str(html))
                res = tools.get_html('http://test.com')
                assert_is_instance(res, BeautifulSoup)

    def test_random_choice_mechanism(self):
        """Test random_response utility fn returns random response"""
        test_list = [1, 2, 3, 4, 5]

        # Loop just to run it a few times
        for _ in test_list:
            assert_in(tools.random_response(test_list), test_list)

    def test_random_choice_requires_flat_list_or_tuple(self):
        """Test random_response utility fn checks data type before running"""
        test_error_types = [1, 'string', {'test': 'dict', 'key': 'val'}, (1, 2, 'tuple'), ['2d', ['list']]]

        for t in test_error_types:
            with self.assertRaises(TypeError):
                tools.random_response(t)
