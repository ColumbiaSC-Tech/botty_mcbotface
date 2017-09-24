from unittest import TestCase
from bs4 import BeautifulSoup
import botty_mcbotface.utils.tools as tools
import os.path
import requests_mock


class TestTools(TestCase):
    def setUp(self):
        self.test_html = os.path.abspath('test_botty/mocks/google_test.html')

    def tearDown(self):
        del self

    def test_soup_returns_html(self):
        with open(self.test_html) as html:
            self.assertIsInstance(tools.soup(html), BeautifulSoup)

    def test_get_html_returns_soup_html(self):
        with requests_mock.Mocker() as m:
            with open(self.test_html) as html:
                m.get('http://test.com', text=str(html))
                res = tools.get_html('http://test.com')
                self.assertIsInstance(res, BeautifulSoup)

    def test_random_choice_mechanism(self):
        test_list = [1, 2, 3, 4, 5]

        # Loop just to run it a few times
        for n in test_list:
            self.assertTrue(tools.random_response(test_list) in test_list)

    def test_random_choice_requires_flat_list_or_tuple(self):
        test_error_types = [1, 'string', {'test': 'dict', 'key': 'val'}, (1, 2, 'tuple'), ['2d', ['list']]]

        for t in test_error_types:
            with self.assertRaises(TypeError):
                tools.random_response(t)
