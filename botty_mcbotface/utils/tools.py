from random import choice
from requests import request
from bs4 import BeautifulSoup
import re


# *** General Methods *** #

def soup(html):
    """
    Get a BeautifulSoup object from html
    :param html: HTML string
    :return: BeautifulSoup object
    """
    bs = BeautifulSoup(html, 'lxml')
    return bs


def get_html(url):
    """
    Return a BeautifulSoup
    :param url: URL to get HTML from
    :return: HTML string
    """
    # FIXME: Figure out the 'white people' URL response
    res = request('get', url)
    return soup(res.text)


def random_response(responses):
    """
    Return a random response given a list of responses
    :param responses: List of response strings
    :return: A random response string
    """
    def test_1d(res):

        if isinstance(res, list):
            return True if True not in [isinstance(r, (list or set or tuple)) for r in res] else False

        return False

    if test_1d(responses):
        return choice(responses)

    raise TypeError
